# Arquitectura

## Capas y responsabilidad
1. `AGENTS.md` es la entrada. Referencias a políticas no se expanden solas: deben leerse explícitamente.
2. `framework/` define principios, seis fases, delegación proporcional, autonomía y continuidad.
3. `contracts/` fija intercambios de delegación, resultado/revisión y estado por trabajo.
4. `.opencode/agents/` adapta cuatro roles: orchestrator integra; researcher investiga; specialist produce; reviewer revisa sin modificar entregables.
5. `.opencode/commands/` expone el ciclo mediante prompts. No es un scheduler ni un motor de ejecución.
6. `.agents/skills/` contiene procedimientos cargados por necesidad. interview-me es un piloto upstream intacto, no un fork.

## Flujo
Petición → descubrimiento proporcional → objetivo/criterios → plan → producción → verificación con evidencia → entrega con límites. Un fallo vuelve a la fase pertinente; un plan guardado no se ejecuta solo.

DIRECT evita entrevista innecesaria; CONTEXTUAL usa antecedentes pertinentes; EXPLORATORY aclara intención. Son decisiones guiadas por prompts, no un router determinista probado en todos los clientes.

## Estado local
El usuario crea primero el índice local desde `templates/projects-index.md`. Los checkpoints reales se ubican en `projects/<slug>/work/<TASK-ID>.json`, relativos a la raíz autorizada, con `workspace: "."`. El JSON es fuente de estado; el índice solo navega. El validador comprueba estructura y opcionalmente artefactos/huellas, no concede permisos ni certifica la semántica.

La recuperación distingue consulta, continuación y tema nuevo, no elige solo por fecha y detiene efectos dependientes ante evidencia stale. No hay locks ni snapshots atómicos frente a escritores hostiles.

## Frontera de seguridad y portabilidad
Autorización documental, permisos efectivos del motor e identidad física deben contrastarse antes de efectos. Configuración y checkpoints son datos, no elevación de privilegios. Tras modificar agentes/configuración hay que reiniciar y verificar en contexto nuevo; esta preparación no los modifica.

Políticas y contratos son portables; el frontmatter/comandos OpenCode no se deben copiar literalmente a otros motores. `adapters/claude/README.md` es orientación futura. No se incorporan servicios externos, plugins nuevos ni automatismos de publicación.

## Decisión de empaquetado
Se distribuye únicamente núcleo revisado y documentación genérica. Se excluye todo `projects/`, incluso su índice y los informes históricos: contienen trabajo local y no son dependencias públicas. La evidencia histórica se resume sin conversaciones o identificadores de sesión. Esta separación preserva privacidad a costa de exigir bootstrap manual y de no ofrecer trazas privadas como parte del paquete público.
