#!/usr/bin/env python3
"""Validación estructural ligera sin dependencias externas."""
import json
from pathlib import Path
from validate_work_state import validate_registry
root = Path(__file__).resolve().parents[1]
required = ["AGENTS.md", "opencode.jsonc", "framework/principles.md", "contracts/delegation.md", ".opencode/agents/orchestrator.md", ".opencode/agents/researcher.md", ".opencode/agents/specialist.md", ".opencode/agents/reviewer.md"]
for path in required:
    assert (root / path).is_file(), f"Falta {path}"
config = json.loads((root / "opencode.jsonc").read_text())
assert config["default_agent"] == "orchestrator"
for path in (root / ".opencode/agents").glob("*.md"):
    content = path.read_text()
    assert content.startswith("---\n") and "\n---\n" in content[4:], f"Frontmatter ausente: {path}"
for path in (root / ".agents/skills").glob("*/SKILL.md"):
    assert "description:" in path.read_text(), f"Skill sin description: {path}"
work_states = validate_registry(root)  # Structure only; no artifact reads or authorization.
if work_states["errors"]:
    print(json.dumps(work_states, ensure_ascii=True, indent=2))
    raise SystemExit(2)
print("PASS: estructura y JSON de configuración válidos. No prueba compatibilidad en ejecución con OpenCode.")
