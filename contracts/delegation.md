# Contrato de delegación (v1)

```yaml
task_id: T-001
owner: orchestrator
assignee: researcher | specialist | reviewer
objective: "Resultado concreto"
context: "Contexto o rutas de referencias"
inputs: ["archivos", "datos"]
constraints: ["límites", "políticas"]
deliverables: ["formato y ubicación"]
acceptance_criteria: ["criterios verificables"]
allowed_actions: ["lectura", "edición local reversible"]
dependencies: []
```

El esquema es un contrato semántico, no un validador automático. Antes de delegar, precisar qué archivo puede editarse; nunca permitir acciones externas implícitamente.
