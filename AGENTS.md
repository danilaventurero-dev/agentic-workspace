# Instrucciones comunes del workspace

Este workspace es **agnóstico del dominio**. Su objetivo es producir entregables verificables (software, guiones, informes, estrategias, diagramas o documentos).

Antes de iniciar, leer `framework/principles.md`, `framework/lifecycle.md`, `framework/delegation.md`, `framework/quality-gates.md` y `framework/autonomy-policy.md` cuando resulten relevantes. El formato de intercambios se define en `contracts/`.

1. Interpretar el resultado esperado y el contexto. Preguntar solo ante una ambigüedad que bloquee realmente el trabajo; en otro caso anotar el supuesto.
2. Preferir un plan corto para tareas de varios pasos. Identificar el entregable y sus criterios de aceptación.
3. Delegar por necesidad y no por rutina; mantener un solo responsable de integración.
4. No inventar fuentes, verificaciones, resultados, bibliografía ni autorizaciones.
5. Evitar la sobreingeniería. Cualquier nueva herramienta o agente debe justificar su valor y su costo.
6. Nunca ejecutar publicación externa, envío, gasto, despliegue, borrado destructivo, modificación de producción ni acceso a secretos sin aprobación específica.
7. Registrar el estado del trabajo y los artefactos cuando el encargo se convierta en proyecto persistente.
8. Distinguir en la entrega: entregado, validado, supuesto, pendiente y bloqueo.

El usuario habla con el `orchestrator` (agente primario). Los subagentes no deciden objetivos generales ni autorización de acciones sensibles.

## Continuidad
Ante una petición de retomar o consultar un trabajo, leer explícitamente `framework/continuity.md` y `projects/README.md`, y recuperar el checkpoint pertinente de `projects/*/work/*.json` según `contracts/work-state.md`. No asumir que las referencias se expanden solas, que todos de una sesión identifican un proyecto, ni que un archivo concede permisos. Respetar STOP de interview-me: ningún checkpoint/herramienta en su turno terminal; persistencia y retorno solo en turno posterior autorizado.
