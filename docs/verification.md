# Verificación y alcance de v1.1.0

“Baseline estable” se limita a los documentos/estructura y mecanismo local probados. No equivale a PROMOTE general, estabilidad universal ni validación runtime de todos los motores/modelos. Las comprobaciones locales siguientes no acreditan que un commit o tag se haya publicado: la verificación remota es una etapa posterior separada, descrita en [release](release.md).

## Comprobaciones reproducibles
Desde la raíz, con Python 3 y `/tmp/opencode` autorizado para fixtures:
```sh
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_work_state.py --root . --check-artifacts
```

- El validador general comprueba archivos requeridos, JSON de configuración, frontmatter/description y estructura del registry. No prueba compatibilidad runtime con OpenCode.
- Los 18 unitarios comprueban contrato de estado, invariantes, rutas y huellas mediante fixtures temporales. No son 18 sesiones conversacionales end-to-end.
- `--check-artifacts` contrasta referencias y huellas declaradas. Artefactos sin huella requieren revisión de contenido; un registry vacío no prueba continuidad.
- La integridad local de interview-me se contrasta con tamaños, SHA-256 y Git blob SHA-1 declarados en `ORIGIN.json`. Es corroboración contra la procedencia registrada, no una nueva descarga/verificación de upstream en red.

## Evidencia histórica resumida
Los informes originales son privados y no forman parte del paquete público. Se conserva aquí el alcance, no las conversaciones ni identificadores personales/de sesión.

| Dimensión | Estado histórico y límite |
|---|---|
| Delegación real y handoff | Observados entre Orchestrator, Researcher, Specialist y Reviewer para investigación, producción y revisión con retorno de artefactos/evidencia. La preparación de este candidato también ejercitó esas delegaciones; no equivale a un scheduler ni a validación universal de cualquier tarea. |
| Descubrimiento y carga de skills | Descubrimiento y carga nativa de interview-me observados en el entorno probado, distintos de leer SKILL.md o comprobar su presencia en disco. No se garantiza precedencia, recarga o compatibilidad en todos los hosts. |
| Continuidad local | Estructura y 18 unitarios PASS; consumidores delegados demostraron recuperación, desambiguación, blocked/completed y stale en escenarios acotados. |
| interview-me | Integridad/carga y un caso humano español con confirmación, STOP y guardado posterior PASS acotado; no todas las ramas ni UX general. |
| Ciclo integrado real, mismo contexto | PASS hasta PLAN: aclaración, confirmación, STOP con cero herramientas y persistencia/retorno posteriores autorizados. Es evidencia histórica del ciclo real, no funcionamiento del producto solicitado. |
| T2 cross-session | **UNKNOWN**: no se acreditó cierre/apertura de sesión primaria y recuperación sin historia inyectada. Un subagente limpio no sustituye esa prueba. |
| Routing y generalización | **UNKNOWN** fuera de casos observados; no se garantiza invocación automática, hotreload ni precedencia universal. |

## Gates todavía abiertos
1. T2 en una sesión primaria realmente nueva sin inyectar el historial del trabajo.
2. Cobertura adicional de ramas de interview-me, exclusiones, routing y errores de carga; no simular respuestas humanas para cerrar gates.
3. Compatibilidad runtime de otros hosts/versiones y enforcement de permisos: no certificada por los scripts.
4. Verificación posterior de distribución: contrastar el commit de `main` y el tag remoto `v1.1.0` con los objetos locales aprobados después de la publicación. La licencia MIT propia está adoptada; aprobar una operación no demuestra que haya concluido.

El validador no certifica semántica de objetivos, legitimidad de autorizaciones, ausencia de secretos ni locks/concurrencia hostil. Fallos de proveedor/permisos no justifican cambiar configuración global ni eludir límites. Una revisión documental favorable no transforma UNKNOWN en PASS.
