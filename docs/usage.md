# Uso

## Ciclo ordinario
- `/define <objetivo>`: audiencia, resultado, restricciones y criterios observables.
- `/plan`: pasos, dependencias, verificaciones y puntos de autorización.
- `/execute`: producción dentro del alcance autorizado.
- `/verify`: evaluación con PASS / FAIL / UNKNOWN y evidencia real.
- `/deliver`: integración, límites y decisiones pendientes.
- `/discover`: antecedentes cuando hagan falta; `/auto` decide la secuencia proporcional, no autoriza acciones externas.

Ejemplo: pedir un guion educativo corto, fijar público y duración, redactarlo y revisar claridad/factualidad. Una tarea sencilla no necesita todos los subagentes. Los resultados siguen `contracts/result.md`; las revisiones siguen `contracts/review.md`.

## Aclarar intención y respetar STOP
No entrevistar otra vez un objetivo confirmado recuperable. Si se usa interview-me, cargar el procedimiento original. Tras confirmar intención, entregar síntesis/opciones y terminar el turno **sin herramientas, todos, archivos, checkpoint, delegación ni downstream**, incluso con autorización previa de guardado.

Solo un turno posterior con autorización aplicable permite persistir esa intención y retornar al padre. “Continuemos” no concede permisos sensibles ni consentimiento genérico para guardar cualquier dato personal. Sin escritura real no afirmar que existe checkpoint durable.

## Trabajos persistentes
Completa primero el bootstrap manual descrito en [instalación](installation.md). Usa el contrato `contracts/work-state.md` y la plantilla `templates/work-state.json`; lee explícitamente `framework/continuity.md` al retomar.

- “¿Dónde quedamos?” consulta estado; no inicia ejecución.
- Una referencia clara/foco vigente tiene prioridad; candidatos comparables requieren desambiguación, no fecha más reciente.
- `awaiting_approval` y `blocked` no se saltan con un “continuemos” genérico.
- `completed` no se reinicia: otra iteración exige alcance nuevo explícito.
- Antes de efectos dependientes, contrastar artefactos/huellas, identidad de raíz y permisos vigentes. Un hash distinto no se actualiza silenciosamente.

El índice local solo navega y los JSON no son autoridad ejecutable. No publiques proyectos, conversaciones, checkpoints, credenciales ni exportaciones de sesiones. El validador ayuda a detectar errores de estructura/stale, no sustituye la revisión de privacidad ni garantiza recuperación cross-session.
