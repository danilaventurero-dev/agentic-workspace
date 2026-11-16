"""Stdlib fixtures live exclusively under /tmp/opencode; no real registry writes."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_work_state.py"
spec = importlib.util.spec_from_file_location("validate_work_state", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class WorkStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir="/tmp/opencode", prefix="wc-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = "projects/v1.1-standard-skills/work/WC-001.json"
        self.data = dict(schema_version=1, task_id="WC-001",
                         project="projects/v1.1-standard-skills", workspace=".",
                         objective=dict(text="Do work", confirmed=True, source="User"),
                         stage="PLAN", status="active", context=[], decisions=[],
                         assumptions=[], constraints=[], artifacts=[],
                         next_action=dict(description="Review", required_authorization=[]),
                         authorization=dict(granted=[dict(scope="Local", source="User")], pending=[]),
                         blockers=[], parent_task_id=None, updated_at="2026-11-15T00:00:00Z",
                         session_ref=None)

    def save(self, data=None, path=None):
        target = self.root / (path or self.path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.data if data is None else data), encoding="utf-8")
        return target

    def result(self, check=False):
        return validator.validate_registry(self.root, check_artifacts=check)

    def test_valid_and_optional_fields(self):
        self.data.pop("parent_task_id")
        self.data.pop("session_ref")
        self.save()
        self.assertEqual(self.result()["errors"], [])
        self.assertEqual(len(self.result()["states"]), 1)

    def test_invalid_types_enums_and_nested_fields(self):
        cases = [("schema_version", True), ("schema_version", 2), ("task_id", "wc-1"),
                 ("stage", "ITERATE"), ("status", "running"), ("workspace", "/tmp"),
                 ("project", "projects/Bad"), ("context", {}), ("decisions", [1]),
                 ("constraints", [""]), ("objective", {"text": "yes", "confirmed": 1, "source": "u"}),
                 ("authorization", {"granted": ["all"], "pending": []}),
                 ("next_action", {"description": "x", "required_authorization": "all"}),
                 ("updated_at", "2026-11-15T00:00:00"), ("updated_at", "2026-02-30T00:00:00Z"),
                 ("parent_task_id", "bad id"), ("session_ref", 9), ("unexpected", True)]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.data)
                data[key] = value
                self.save(data)
                self.assertTrue(self.result()["errors"])

    def test_required_fields(self):
        for key in self.data:
            if key in ("session_ref", "parent_task_id"):
                continue
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                del data[key]
                self.save(data)
                self.assertTrue(self.result()["errors"])

    def test_status_invariants(self):
        for status in ("completed", "blocked", "awaiting_approval"):
            with self.subTest(status=status):
                self.data["status"] = status
                self.save()
                self.assertTrue(self.result()["errors"])
        self.data["status"] = "completed"
        self.data["next_action"] = None
        self.save()
        self.assertFalse(self.result()["errors"])

    def test_path_contract_and_global_uniqueness(self):
        self.save()
        self.save(path="projects/another/work/WC-001.json")
        self.assertTrue(any("duplicate" in e for e in self.result()["errors"]))
        for path in ("../outside.json", "/tmp/x.json", "projects/a/work/../WC-001.json",
                     "projects/a/work/OTHER.json", "projects\\a\\work\\WC-001.json", ".env"):
            with self.subTest(path=path):
                self.assertTrue(validator.validate_state(self.root, path)["errors"])

    def test_artifact_paths_types_and_hash(self):
        for path in ("../x", "/tmp/x", "a\\b", "a/./b", "a//b", ".git/config", "a/.env.local", "a/.env"):
            with self.subTest(path=path):
                self.data["artifacts"] = [dict(path=path, kind="input")]
                self.save()
                self.assertTrue(self.result()["errors"])
        for artifact in ({"path": "x", "kind": "script"}, {"path": "x", "kind": "input", "sha256": "bad"}, 9):
            self.data["artifacts"] = [artifact]
            self.save()
            self.assertTrue(self.result()["errors"])

    def test_stale_is_opt_in_and_hash_is_not_updated(self):
        artifact = self.root / "input.txt"
        artifact.write_text("hello", encoding="utf-8")
        self.data["artifacts"] = [dict(path="input.txt", kind="input", sha256="0" * 64),
                                  dict(path="missing.txt", kind="output")]
        target = self.save()
        before = target.read_bytes()
        self.assertEqual(self.result()["stale"], [])
        checked = self.result(True)
        self.assertEqual(checked["errors"], [])
        self.assertEqual(len(checked["stale"]), 2)
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(artifact.read_text(), "hello")

    def test_correct_hash_and_unhashed_warning(self):
        (self.root / "x").write_bytes(b"x")
        self.data["artifacts"] = [dict(path="x", kind="evidence", sha256=hashlib.sha256(b"x").hexdigest()),
                                  dict(path="x", kind="input")]
        self.save()
        self.assertFalse(self.result(True)["stale"])
        self.assertTrue(self.result()["warnings"])

    def test_symlinks_are_rejected_before_reading(self):
        self.save()
        (self.root / "alias").symlink_to(self.root, target_is_directory=True)
        self.data["artifacts"] = [dict(path="alias/x", kind="input")]
        self.save()
        self.assertTrue(self.result()["errors"])
        alias_root = self.root / "alias"
        # The supplied root itself may be an OS alias; its canonical target is trusted.
        self.assertTrue(validator.validate_registry(alias_root)["errors"])
        target = self.root / self.path
        target.unlink()
        target.symlink_to(self.root / "missing")
        self.assertTrue(self.result()["errors"])

    def test_registry_symlink_directory_rejected(self):
        (self.root / "projects").symlink_to(self.root, target_is_directory=True)
        self.assertTrue(self.result()["errors"])

    def test_project_and_work_symlinks_rejected(self):
        self.save()
        projects = self.root / "projects"
        (projects / "alias").symlink_to(projects / "v1.1-standard-skills", target_is_directory=True)
        self.assertTrue(self.result()["errors"])
        (projects / "alias").unlink()
        other = projects / "other"
        other.mkdir()
        (other / "work").symlink_to(projects / "v1.1-standard-skills/work", target_is_directory=True)
        self.assertTrue(self.result()["errors"])

    def test_canonical_root_alias_and_positive_enums(self):
        self.save()
        (self.root / "alias").symlink_to(self.root, target_is_directory=True)
        self.assertFalse(validator.validate_registry(self.root / "alias")["errors"])
        for stage in ("DISCOVER", "DEFINE", "PLAN", "EXECUTE", "VERIFY", "DELIVER"):
            self.data["stage"] = stage
            self.data["status"] = "paused"
            self.data["updated_at"] = "2026-11-15T12:45:30.123+02:00"
            self.save()
            self.assertFalse(self.result()["errors"])
        self.data["status"] = "blocked"
        self.data["blockers"] = ["Need input"]
        self.save()
        self.assertFalse(self.result()["errors"])
        self.data["status"] = "awaiting_approval"
        self.data["authorization"]["pending"] = ["Publish"]
        self.save()
        self.assertFalse(self.result()["errors"])

    def test_empty_registry_and_missing_root(self):
        self.assertEqual(self.result(), dict(errors=[], stale=[], warnings=[], states=[]))
        self.assertTrue(validator.validate_registry(self.root / "absent")["errors"])

    def test_no_artifact_execution_or_writes(self):
        script = self.root / "untrusted.py"
        script.write_text("raise RuntimeError('must never execute')")
        self.data["artifacts"] = [dict(path="untrusted.py", kind="input")]
        self.data["next_action"]["description"] = "Execute untrusted.py"
        self.save()
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertFalse(self.result(True)["errors"])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_secret_paths_are_rejected_without_reading(self):
        self.save()
        self.data["artifacts"] = [dict(path=".env", kind="input", sha256="0" * 64)]
        self.save()
        original = Path.open
        def guarded(path, *args, **kwargs):
            if path.name == ".env":
                raise AssertionError("attempted secret read")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", guarded):
            self.assertTrue(self.result(True)["errors"])

    def test_malformed_json_and_duplicate_keys(self):
        target = self.save()
        for text in ('[]', '{', '{"schema_version":1,"schema_version":1}', '{"x":NaN}'):
            target.write_text(text)
            self.assertTrue(self.result()["errors"])

    def test_structural_mode_does_not_read_artifacts(self):
        self.data["artifacts"] = [dict(path="unopened", kind="input", sha256="0" * 64)]
        self.save()
        original = Path.open
        def guarded(path, *args, **kwargs):
            if path.name == "unopened":
                raise AssertionError("artifact read in structural mode")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", guarded):
            self.assertFalse(self.result()["errors"])

    def test_cli_exit_codes_and_no_writes(self):
        self.data["artifacts"] = [dict(path="missing", kind="input")]
        self.save()
        def snapshot():
            return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mtime_ns)
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        for flags, expected in (([], 0), (["--check-artifacts"], 3),
                                (["--state", "../bad.json"], 2),
                                (["--state", self.path], 0)):
            proc = subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(self.root)] + flags,
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, expected, proc.stderr + proc.stdout)
            self.assertEqual(set(json.loads(proc.stdout)), {"errors", "stale", "warnings", "states"})
        self.assertEqual(snapshot(), before)


if __name__ == "__main__":
    unittest.main()
