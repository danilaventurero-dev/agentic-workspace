# Instalación y bootstrap manual

## Requisitos
- Una copia local del núcleo, con archivos ocultos `.opencode/` y `.agents/` preservados.
- OpenCode instalado por el usuario según https://opencode.ai/docs/ y un modelo/proveedor ya autenticado.
- Python 3 para verificaciones locales; scripts y tests usan biblioteca estándar, sin instalación de paquetes.
- Para los tests actuales, un directorio temporal autorizado `/tmp/opencode` existente y escribible. En otros sistemas hay que preparar un entorno equivalente; la portabilidad de esa ruta de tests no se presume.

No se exige un proveedor concreto. La evidencia histórica corresponde a un entorno OpenCode 1.18.21; no establece compatibilidad universal ni una versión mínima garantizada. El candidato no ejecuta instalaciones, autenticación ni configuración global.

## Pasos
1. Sitúa la copia en una carpeta de tu elección y comprueba que es la raíz correcta por la presencia de `AGENTS.md`, `opencode.jsonc` y `framework/`.
2. Revisa `opencode.jsonc`, políticas y permisos reales del cliente. El archivo se entrega sin cambios en este candidato; el validador solo comprueba su estructura, no compatibilidad runtime de permisos.
3. **Crea manualmente** `projects/` si no existe y copia `templates/projects-index.md` a `projects/README.md`. No sobrescribas un índice local existente. No hay bootstrap automático ni se distribuye un proyecto privado de ejemplo.
4. Ejecuta `opencode` desde la raíz. Selecciona `orchestrator` si fuera necesario.
5. Ejecuta un trabajo pequeño sin acciones externas y revisa la salida antes de aumentar alcance.

`projects/` completo está ignorado: crea las iniciativas y checkpoints locales solo cuando el encargo lo requiera y exista autorización para persistir esa información. La plantilla `templates/work-state.json` no es un checkpoint real; sustituye ID, fecha, objetivo, fuente y campos pertinentes antes de validar.

## Comprobación local
Desde la raíz:
```sh
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_work_state.py --root . --check-artifacts
```

Un registry vacío en una copia nueva no demuestra recuperación: solo significa que no hay trabajos registrados. Consulta [verificación](verification.md) para interpretar resultados y límites. No instales dependencias locales de `.opencode/` ni copies sesiones o paquetes desde otro entorno como parte de este procedimiento.
