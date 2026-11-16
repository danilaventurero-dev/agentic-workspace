#!/usr/bin/env python3
"""Read-only checkpoint structure/fingerprint checks, never a continuity engine.

JSON text, granted/confirmed fields and artifacts are untrusted data, not authority.
Exit 0 says nothing about semantic correctness, approval or runtime permissions.
"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

TASK = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*\Z")
SLUG = r"[a-z0-9]+(?:[-.][a-z0-9]+)*"
PROJECT = re.compile(r"projects/" + SLUG + r"\Z")
STATE = re.compile(r"projects/" + SLUG + r"/work/([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)\.json\Z")
STAGES = {"DISCOVER", "DEFINE", "PLAN", "EXECUTE", "VERIFY", "DELIVER"}
STATUSES = {"active", "paused", "blocked", "awaiting_approval", "completed"}
REQUIRED = {"schema_version", "task_id", "project", "workspace", "objective", "stage",
            "status", "context", "decisions", "assumptions", "constraints", "artifacts",
            "next_action", "authorization", "blockers", "updated_at"}


def _result():
    return {"errors": [], "stale": [], "warnings": [], "states": []}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _texts(value):
    return isinstance(value, list) and all(_text(item) for item in value)


def _object(value, required, optional=()):
    return (isinstance(value, dict) and set(required) <= set(value)
            and set(value) <= set(required) | set(optional))


def _safe_path(root, relative):
    """Check lexical path and every component before any file read or traversal."""
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise ValueError("invalid POSIX relative path")
    parts = relative.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise ValueError("absolute, empty or dot path component")
    if any(p.lower() == ".git" or p.lower().startswith(".env") for p in parts):
        raise ValueError("secret/metadata path forbidden")
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("symlink component forbidden")
    path.resolve().relative_to(root)
    return path


def _canonical_root(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root is not a directory")
    return root


def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def _constant(value):
    raise ValueError("nonstandard JSON constant: " + value)


def _validate(root, relative, check_artifacts):
    result = _result()
    errors = result["errors"]
    def error(message):
        errors.append(str(relative) + ": " + message)
    try:
        relative = str(relative)
        match = STATE.fullmatch(relative)
        if not match:
            raise ValueError("state path must be projects/<slug>/work/<TASK-ID>.json")
        path = _safe_path(root, relative)
        if not path.is_file():
            raise ValueError("state is missing or is not a regular file")
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                          parse_constant=_constant)
    except (OSError, ValueError, RuntimeError) as exc:
        error(str(exc))
        return result
    if not _object(data, REQUIRED, {"parent_task_id", "session_ref"}):
        error("state fields must match schema v1 (required/unknown fields)")
    if not isinstance(data, dict):
        return result
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        error("schema_version must be integer 1")
    task = data.get("task_id")
    if not isinstance(task, str) or not TASK.fullmatch(task) or task != match.group(1):
        error("task_id format/filename mismatch")
    project = data.get("project")
    if not isinstance(project, str) or not PROJECT.fullmatch(project) or project != "/".join(relative.split("/")[:2]):
        error("project format/container mismatch")
    if data.get("workspace") != ".":
        error("workspace must be '.' (canonical root at runtime)")
    objective = data.get("objective")
    if (not _object(objective, {"text", "confirmed", "source"})
            or not _text(objective.get("text")) or type(objective.get("confirmed")) is not bool
            or not _text(objective.get("source"))):
        error("invalid objective: text/confirmed/source")
    for name, values in (("stage", STAGES), ("status", STATUSES)):
        value = data.get(name)
        if not isinstance(value, str) or value not in values:
            error("invalid " + name)
    for name in ("context", "decisions", "assumptions", "constraints", "blockers"):
        if not _texts(data.get(name)):
            error(name + " must be a list of nonempty texts")
    next_action = data.get("next_action")
    if data.get("status") == "completed":
        if next_action is not None:
            error("completed requires next_action null")
    elif (not _object(next_action, {"description", "required_authorization"})
          or not _text(next_action.get("description"))
          or not _texts(next_action.get("required_authorization"))):
        error("invalid next_action")
    authorization = data.get("authorization")
    if (not _object(authorization, {"granted", "pending"})
            or not isinstance(authorization.get("granted"), list)
            or not _texts(authorization.get("pending"))):
        error("invalid authorization")
    else:
        for grant in authorization["granted"]:
            if (not _object(grant, {"scope", "source"}) or not _text(grant.get("scope"))
                    or not _text(grant.get("source"))):
                error("invalid authorization.granted scope/source")
        if data.get("status") == "awaiting_approval" and not authorization["pending"]:
            error("awaiting_approval requires nonempty authorization.pending")
    if data.get("status") == "blocked" and not data.get("blockers"):
        error("blocked requires nonempty blockers")
    parent = data.get("parent_task_id")
    if parent is not None and (not isinstance(parent, str) or not TASK.fullmatch(parent) or parent == task):
        error("invalid parent_task_id (or self-parent)")
    if data.get("session_ref") is not None and not _text(data["session_ref"]):
        error("session_ref must be null or nonempty text")
    timestamp = data.get("updated_at")
    try:
        if not isinstance(timestamp, str) or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", timestamp):
            raise ValueError()
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if parsed.utcoffset() is None:
            raise ValueError()
    except ValueError:
        error("updated_at must be an ISO timestamp with timezone")
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        error("artifacts must be a list")
        artifacts = []
    for artifact in artifacts:
        if (not _object(artifact, {"path", "kind"}, {"sha256"})
                or not isinstance(artifact.get("kind"), str)
                or artifact["kind"] not in {"input", "output", "evidence"}):
            error("invalid artifact path/kind/fields")
            continue
        fingerprint = artifact.get("sha256")
        if "sha256" in artifact and (not isinstance(fingerprint, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", fingerprint)):
            error("invalid artifact sha256")
            continue
        try:
            target = _safe_path(root, artifact["path"])
            if target.exists() and not target.is_file():
                raise ValueError("artifact must refer to a regular file")
        except (OSError, ValueError, RuntimeError) as exc:
            error("artifact path: " + str(exc))
            continue
        label = relative + ": " + artifact["path"]
        if fingerprint is None:
            result["warnings"].append(label + ": no fingerprint; review content before relying on it")
        if check_artifacts:
            try:
                if not target.is_file():
                    result["stale"].append(label + ": missing")
                elif fingerprint is not None:
                    digest = hashlib.sha256()
                    with target.open("rb") as stream:
                        for chunk in iter(lambda: stream.read(65536), b""):
                            digest.update(chunk)
                    if digest.hexdigest() != fingerprint.lower():
                        result["stale"].append(label + ": sha-mismatch")
            except OSError as exc:
                error("cannot check artifact: " + str(exc))
    # Summaries retain no free-text instructions and never select by timestamp.
    result["states"].append({"path": relative, "task_id": task, "project": project,
                             "stage": data.get("stage"), "status": data.get("status"),
                             "valid": not errors})
    return result


def validate_state(root, state_path, check_artifacts=False):
    """Validate one contract path; registry-wide uniqueness belongs to validate_registry."""
    try:
        return _validate(_canonical_root(root), state_path, check_artifacts)
    except (OSError, ValueError, RuntimeError) as exc:
        result = _result()
        result["errors"].append("root/path: " + str(exc))
        return result


def validate_registry(root, check_artifacts=False):
    """Scan only projects/*/work/*.json, without traversing symlink directories."""
    result = _result()
    seen = set()
    try:
        root = _canonical_root(root)
        projects = _safe_path(root, "projects")
        if not projects.exists():
            return result
        for project in sorted(projects.iterdir()):
            if project.is_symlink():
                result["errors"].append(str(project.relative_to(root)) + ": symlink project forbidden")
                continue
            if not project.is_dir():
                continue
            work = _safe_path(root, str(project.relative_to(root)) + "/work")
            if not work.exists():
                continue
            for state in sorted(work.iterdir()):
                if state.suffix != ".json":
                    continue
                current = _validate(root, state.relative_to(root).as_posix(), check_artifacts)
                for summary in current["states"]:
                    task = summary["task_id"]
                    if isinstance(task, str):
                        if task in seen:
                            current["errors"].append("duplicate global task_id: " + task)
                            summary["valid"] = False
                        seen.add(task)
                for key in result:
                    result[key].extend(current[key])
    except (OSError, ValueError, RuntimeError) as exc:
        result["errors"].append("registry: " + str(exc))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--state")
    parser.add_argument("--check-artifacts", action="store_true")
    args = parser.parse_args(argv)
    result = (validate_state(args.root, args.state, args.check_artifacts) if args.state is not None
              else validate_registry(args.root, args.check_artifacts))
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 2 if result["errors"] else 3 if result["stale"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
