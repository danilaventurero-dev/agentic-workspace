# Contrato de resultado (v1)

```yaml
task_id: T-001
status: completed | blocked | failed | needs_review
summary: "Qué se hizo y qué no"
artifacts: ["rutas o enlaces"]
evidence: ["comprobaciones reales con resultado"]
assumptions: ["supuestos y grado de confianza"]
limitations: ["riesgos o pruebas pendientes"]
open_decisions: ["decisiones para el líder o usuario"]
```

`completed` solo significa tarea realizada; el orquestador decide si el proyecto superó los gates. Prohibido inventar evidencias.
