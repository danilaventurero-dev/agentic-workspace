# Política de delegación híbrida

Equipo base: **orchestrator** (primario), **researcher**, **specialist**, **reviewer** (subagentes).

- Researcher: recupera y sintetiza fuentes y contexto; no edita entregables.
- Specialist: crea artefactos y ejecuta tareas delimitadas, con skills de dominio.
- Reviewer: prueba supuestos, detecta defectos y emite veredicto sin modificar el entregable.

El orquestador decide si invoca agentes. En tareas simples puede asumir investigación, ejecución y comprobación de manera directa. La especialización adicional se logra inicialmente con skills, no con agentes nuevos.

**Delegar si**: requiere investigación independiente, producción sustantiva o revisión crítica que justifique un contexto separado.

**No delegar si**: consulta trivial, cambio menor, costo de coordinación alto o necesidad de acceso sensible no autorizado.

**Paralelismo**: permitido solo para tareas independientes sin editar simultáneamente los mismos archivos. Sin coordinación automática de locks en V1, preferir secuencial para escrituras.

**Hand-off**: usar `contracts/delegation.md`; la respuesta usa `contracts/result.md`. Reintegrar evidencias y declarar bloqueos. No asumir que el subagente completó validaciones no demostradas.
