#!/usr/bin/env python3
"""Generic Product composition checker with explicit native-check execution."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


class UsageError(RuntimeError):
    pass


class InspectionError(RuntimeError):
    pass


class ExecutionContextError(RuntimeError):
    pass


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


@dataclass(frozen=True)
class Identity:
    path: str
    resolved: str
    device: int
    inode: int
    node_type: int
    mode: int
    digest: str | None


@dataclass(frozen=True)
class PreparedCheck:
    machine_id: str
    argv: tuple[str, ...]
    cwd_relative: str
    cwd: Path
    executable: Path
    bare_executable: bool
    root_identity: Identity
    profile_identity: Identity
    product_identity: Identity
    cwd_identity: Identity
    executable_identity: Identity


def _raw_sorted(values):
    return sorted(values, key=lambda value: str(value).encode("utf-8"))


def _identity(path: Path, *, digest=False) -> Identity:
    info = path.lstat()
    resolved = path.resolve(strict=True)
    value = hashlib.sha256(path.read_bytes()).hexdigest() if digest else None
    return Identity(
        str(path.absolute()), str(resolved), info.st_dev, info.st_ino,
        stat.S_IFMT(info.st_mode), stat.S_IMODE(info.st_mode), value,
    )


def _regular_directory(path: Path, label: str) -> Path:
    try:
        info = path.lstat()
    except OSError as error:
        raise InspectionError(f"{label} отсутствует или недоступен") from error
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise InspectionError(f"{label} должен быть обычным каталогом без symlink")
    return path.resolve(strict=True)


def _load_profile_module(workspace: Path):
    expected_checker = workspace / "tools/check_product.py"
    try:
        checker_info = Path(__file__).lstat()
    except OSError as error:
        raise UsageError("checker origin недоступен") from error
    if stat.S_ISLNK(checker_info.st_mode) or Path(__file__).resolve() != expected_checker.resolve(strict=True):
        raise UsageError("checker origin должен быть exact Workspace tools/check_product.py")
    parser_path = workspace / "tools/project_profile.py"
    try:
        parser_info = parser_path.lstat()
    except OSError as error:
        raise UsageError("co-located project_profile.py отсутствует") from error
    if stat.S_ISLNK(parser_info.st_mode) or not stat.S_ISREG(parser_info.st_mode):
        raise UsageError("co-located project_profile.py имеет недопустимый тип")
    try:
        parser_path.resolve(strict=True).relative_to(workspace)
    except (OSError, ValueError) as error:
        raise UsageError("project_profile.py выходит за Workspace") from error
    name = "_deployed_product_profile"
    spec = importlib.util.spec_from_file_location(name, parser_path)
    if spec is None or spec.loader is None:
        raise UsageError("project_profile.py нельзя загрузить")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    if Path(module.__file__).resolve() != parser_path.resolve(strict=True):
        raise UsageError("project_profile module origin mismatch")
    return module


def _contained(root: Path, candidate: Path, label: str) -> Path:
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise ExecutionContextError(f"{label} выходит за Product root") from error
    return resolved


def _resolve_executable(command: str, cwd: Path, product_root: Path) -> tuple[Path, bool]:
    if "/" not in command and "\\" not in command:
        value = shutil.which(command)
        if value is None:
            raise ExecutionContextError(f"executable не найден: {command}")
        candidate = Path(value)
        bare = True
    else:
        if "\\" in command:
            raise ExecutionContextError("relative executable должен использовать POSIX separators")
        pure = PurePosixPath(command)
        if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != command:
            raise ExecutionContextError("absolute/unnormalized executable path запрещён")
        candidate = cwd.joinpath(*pure.parts)
        candidate = _contained(product_root, candidate, "executable")
        bare = False
    try:
        canonical = candidate.resolve(strict=True)
        info = canonical.stat()
    except OSError as error:
        raise ExecutionContextError(f"executable недоступен: {command}") from error
    if not stat.S_ISREG(info.st_mode) or not os.access(canonical, os.X_OK):
        raise ExecutionContextError(f"executable не является исполняемым regular file: {command}")
    if not bare:
        _contained(product_root, canonical, "executable")
    return canonical, bare


def _prepare(profile, machine_id: str, product_root: Path) -> PreparedCheck:
    declaration = profile.product_native_checks[machine_id]
    relative = declaration.working_directory
    cwd = product_root.joinpath(*PurePosixPath(relative).parts).resolve(strict=True)
    _contained(product_root, cwd, f"product_native_checks.{machine_id}.working_directory")
    if not cwd.is_dir():
        raise ExecutionContextError(f"working_directory не является каталогом: {machine_id}")
    executable, bare = _resolve_executable(declaration.command[0], cwd, product_root)
    return PreparedCheck(
        machine_id=machine_id,
        argv=tuple(declaration.command),
        cwd_relative=relative,
        cwd=cwd,
        executable=executable,
        bare_executable=bare,
        root_identity=_identity(profile.workspace_root),
        profile_identity=_identity(profile.profile_path, digest=True),
        product_identity=_identity(product_root),
        cwd_identity=_identity(cwd),
        executable_identity=_identity(executable, digest=True),
    )


def _revalidate_context(item: PreparedCheck, profile) -> None:
    product_root = profile.product_root.resolve(strict=True)
    current_cwd = product_root.joinpath(*PurePosixPath(item.cwd_relative).parts).resolve(strict=True)
    _contained(product_root, current_cwd, "working_directory")
    if current_cwd != item.cwd:
        raise ExecutionContextError("working_directory resolution changed after validation")
    expected = (
        (item.root_identity, _identity(profile.workspace_root)),
        (item.profile_identity, _identity(profile.profile_path, digest=True)),
        (item.product_identity, _identity(product_root)),
        (item.cwd_identity, _identity(current_cwd)),
        (item.executable_identity, _identity(item.executable, digest=True)),
    )
    if any(before != after for before, after in expected):
        raise ExecutionContextError("execution context changed after validation")
    current, _bare = _resolve_executable(item.argv[0], item.cwd, product_root)
    if current != item.executable:
        raise ExecutionContextError("executable resolution changed after validation")


def _result_row(item: PreparedCheck, status: str, *, exit_code=None, stdout=b"", stderr=b""):
    return {
        "id": item.machine_id,
        "status": status,
        "argv": list(item.argv),
        "resolved_executable": str(item.executable),
        "working_directory": item.cwd_relative,
        "exit_code": exit_code,
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
    }


def _not_run(item: PreparedCheck):
    return _result_row(item, "NOT_RUN")


def _execute(prepared: list[PreparedCheck], profile, timeout: int):
    rows = []
    outcome = 0
    for index, item in enumerate(prepared):
        try:
            _revalidate_context(item, profile)
        except (ExecutionContextError, OSError) as error:
            row = _result_row(item, "CONTEXT_CHANGED", stderr=(str(error) + "\n").encode())
            rows.append(row)
            rows.extend(_not_run(later) for later in prepared[index + 1:])
            return rows, 2
        argv = [str(item.executable), *item.argv[1:]]
        try:
            process = subprocess.Popen(
                argv,
                cwd=item.cwd,
                env=os.environ.copy(),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
            )
        except OSError as error:
            rows.append(_result_row(item, "EXECUTABLE_NOT_FOUND", stderr=(str(error) + "\n").encode()))
            rows.extend(_not_run(later) for later in prepared[index + 1:])
            return rows, 2
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            rows.append(_result_row(item, "TIMEOUT", exit_code=None, stdout=stdout, stderr=stderr))
            outcome = max(outcome, 1)
            continue
        except KeyboardInterrupt:
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=1)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            rows.append(_result_row(item, "INTERRUPTED", exit_code=None, stdout=stdout, stderr=stderr))
            rows.extend(_not_run(later) for later in prepared[index + 1:])
            return rows, 130
        status = "PASS" if process.returncode == 0 else "FAIL"
        rows.append(_result_row(item, status, exit_code=process.returncode, stdout=stdout, stderr=stderr))
        if process.returncode != 0:
            outcome = max(outcome, 1)
    return rows, outcome


def inspect_product(workspace_value, *, run_native_checks=False, native_check=None, timeout_seconds=None):
    workspace = _regular_directory(Path(workspace_value), "Workspace root")
    module = _load_profile_module(workspace)
    try:
        profile = module.load_project_profile(workspace)
    except module.ProjectProfileError as error:
        return {
            "schema": "generic.product-check.v1", "status": "FAIL", "mode": "composition-only",
            "composition": [{"id": "project-composition", "status": "FAIL", "message": str(error)}],
            "native_validation": [], "native_execution": [], "fail_count": 1, "warn_count": 0,
        }, 1
    composition = [{"id": "product-composition", "status": "PASS"}]
    native_validation = [
        {"id": machine_id, "status": "PASS"}
        for machine_id in _raw_sorted(profile.product_native_checks)
    ]
    mode = "native-execution" if run_native_checks else "composition-only"
    if not run_native_checks:
        return {
            "schema": "generic.product-check.v1", "status": "PASS", "mode": mode,
            "composition": composition, "native_validation": native_validation,
            "native_execution": [], "fail_count": 0, "warn_count": 0,
        }, 0
    if timeout_seconds is None or type(timeout_seconds) is not int or timeout_seconds <= 0:
        raise UsageError("--run-native-checks требует positive --timeout-seconds")
    if native_check is not None and native_check not in profile.product_native_checks:
        raise UsageError(f"unknown --native-check: {native_check}")
    selected = [native_check] if native_check is not None else _raw_sorted(profile.product_native_checks)
    try:
        prepared = [_prepare(profile, machine_id, profile.product_root.resolve(strict=True)) for machine_id in selected]
    except (ExecutionContextError, OSError) as error:
        return {
            "schema": "generic.product-check.v1", "status": "STOP", "mode": mode,
            "composition": composition, "native_validation": native_validation,
            "native_execution": [], "fail_count": 1, "warn_count": 0, "error": str(error),
        }, 2
    rows, code = _execute(prepared, profile, timeout_seconds)
    status = "PASS" if code == 0 else "INTERRUPTED" if code == 130 else "STOP" if code == 2 else "FAIL"
    return {
        "schema": "generic.product-check.v1", "status": status, "mode": mode,
        "composition": composition, "native_validation": native_validation,
        "native_execution": rows,
        "fail_count": sum(item["status"] not in {"PASS", "NOT_RUN"} for item in rows),
        "warn_count": 0,
    }, code


def _error_result(message):
    return {
        "schema": "generic.product-check.v1", "status": "STOP", "mode": "not-started",
        "composition": [], "native_validation": [], "native_execution": [],
        "fail_count": 1, "warn_count": 0, "error": str(message),
    }


def main(argv=None) -> int:
    parser = JsonArgumentParser(description="Generic Product composition and native-check verifier", add_help=True)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--run-native-checks", action="store_true")
    parser.add_argument("--native-check")
    parser.add_argument("--timeout-seconds", type=int)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    output_format = "text"
    try:
        args = parser.parse_args(argv)
        output_format = args.format
        if args.native_check is not None and not args.run_native_checks:
            raise UsageError("--native-check допустим только с --run-native-checks")
        if args.timeout_seconds is not None and not args.run_native_checks:
            raise UsageError("--timeout-seconds допустим только с --run-native-checks")
        result, code = inspect_product(
            args.workspace,
            run_native_checks=args.run_native_checks,
            native_check=args.native_check,
            timeout_seconds=args.timeout_seconds,
        )
    except (UsageError, InspectionError, OSError, ValueError) as error:
        result, code = _error_result(error), 2
    if output_format == "json" or (argv is not None and "--format" in argv and "json" in argv):
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"PRODUCT_CHECK: {result['status']}")
        print(f"FAIL: {result['fail_count']}")
        print("WARN: 0")
        for row in result.get("native_execution", []):
            print(f"NATIVE {row['id']}: {row['status']}")
        if "error" in result:
            print(f"ERROR: {result['error']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
