# Agentic Workspace — v1.1.0

Framework multidisciplinario para equipos de agentes: un orquestador responsable y especialistas bajo demanda. Sirve para producir software, textos, estrategias, análisis y otros entregables verificables.

v1.1.0 identifica un baseline estable únicamente del alcance documental y estructural probado; no certifica estabilidad universal del runtime ni PROMOTE global de interview-me, routing o continuidad entre sesiones. Consulta [verificación y límites](docs/verification.md). La disponibilidad remota de esta versión se comprueba mediante el tag `v1.1.0`, según el [procedimiento de release](docs/release.md); este documento por sí solo no acredita publicación.

## Principios
- Objetivo, audiencia y criterios de aceptación antes de elegir herramientas.
- Agentes = roles; skills = procedimientos; MCP = herramientas.
- Autonomía local proporcional; acciones externas, sensibles o irreversibles requieren autorización específica.
- Evidencia antes que confianza: separar entregado, validado, supuesto y pendiente.
- Delegar por necesidad, no por rutina.

## Inicio rápido
1. Prepara OpenCode y un proveedor/modelo autenticado siguiendo su documentación oficial. No se instala ni autentica nada automáticamente.
2. Abre una copia de este workspace en una ubicación de tu elección.
3. Antes del primer trabajo persistente, crea manualmente `projects/README.md` a partir de [la plantilla genérica](templates/projects-index.md). `projects/` es local y está excluido de Git; no se distribuye el índice privado original.
4. Ejecuta `opencode` desde la raíz y selecciona `orchestrator` si la sesión conserva otro agente.
5. Prueba `/define Diseñar un guion breve de vídeo educativo sobre MCP para principiantes`, luego `/plan` y `/execute`. `/auto` permite decidir pasos, no concede autorización para acciones externas.

Consulta [instalación](docs/installation.md) y [uso](docs/usage.md) antes de trabajar con permisos o estado persistente.

## Estructura
| Ruta | Función |
|---|---|
| `AGENTS.md`, `framework/` | Entrada, principios, ciclo, autonomía y continuidad |
| `contracts/` | Delegación, resultados, revisión y esquema de estado |
| `templates/` | Brief, entrega, índice local y checkpoint de ejemplo |
| `.opencode/agents/`, `.opencode/commands/` | Roles y comandos específicos de OpenCode |
| `.agents/skills/` | Tres procedimientos propios y piloto externo interview-me intacto |
| `scripts/`, `tests/` | Validación estructural y 18 pruebas unitarias de estado |
| `adapters/claude/` | Orientación futura; no adaptador ejecutable |

## Documentación
- [Arquitectura](docs/architecture.md)
- [Verificación y limitaciones](docs/verification.md)
- [Procedimiento de release](docs/release.md)
- [Cambios](CHANGELOG.md) y [avisos de terceros](THIRD_PARTY_NOTICES.md)

Los contratos generales son Markdown y requieren juicio contextual; el contrato de estado sí tiene un validador JSON local. No hay motor externo de workflows, locks, sandbox nuevo, garantía de routing/invocación, paralelismo garantizado ni observabilidad de costos. La configuración no presupone proveedor y no sustituye los permisos reales del cliente.

## Licencia
El material propio se distribuye bajo [licencia MIT](LICENSE), copyright (c) 2026 Agentic Workspace contributors. El componente externo interview-me conserva su licencia MIT y copyright originales de Addy Osmani, separados y sin modificar; consulta los [avisos de terceros](THIRD_PARTY_NOTICES.md).

## Referencias oficiales
Referencias informativas; no implican consulta de red en esta preparación:
- https://opencode.ai/docs/
- https://opencode.ai/docs/agents
- https://opencode.ai/docs/commands
- https://opencode.ai/docs/skills
- https://opencode.ai/docs/permissions
