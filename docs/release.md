# Release v1.1.0: procedimiento controlado

## Alcance y evidencia
`VERSION` identifica 1.1.0 y el tag previsto es `v1.1.0`. Ni esos textos ni el changelog demuestran existencia de commit, tag o publicación remota. El estado de distribución debe comprobarse en Git; no se infiere de un checkpoint o de una autorización.

Solo núcleo y documentación genérica se distribuyen. No se incluye `projects/`, su índice, sesiones, exportaciones, checkpoints, dependencias ni caches. El baseline conserva políticas/contratos/implementaciones y resume evidencia acotada; no declara PROMOTE global de interview-me/routing/continuidad. Ver [verificación](verification.md).

## Antes del commit
1. Revisar inventario exacto con `git diff --cached --name-only` y contenido con `git diff --cached`; contrastar la allowlist final de 48 archivos.
2. Revisar privacidad, enlaces, integridad upstream y resultados reales de validadores/18 unitarios. `.gitignore` no elimina archivos ya staged ni sustituye la revisión.
3. Conservar la [licencia MIT propia](../LICENSE) y los [avisos upstream separados](../THIRD_PARTY_NOTICES.md). No sustituir copyright ni licencia de interview-me.
4. Confirmar autorización específica del usuario sobre el delta final. La preparación del índice no ejecuta commit. El responsable de integración revisa y realiza commit/tag/publicación, no los especialistas encargados de documentación.

## Distribución autorizada y verificación posterior
Destino acordado: `https://github.com/danilaventurero-dev/agentic-workspace.git`, repositorio público existente. No crear otro repositorio ni cambiar visibilidad. La autorización para publicar `main` y el tag `v1.1.0` no acredita que esas operaciones hayan ocurrido.

El responsable de integración debe comprobar el estado local/remoto vigente antes de conectar o publicar, sin sobreescribir historia ajena ni usar force push. Tras el commit aprobado, crear el tag anotado previsto y publicar únicamente las referencias autorizadas. No guardar credenciales ni cambiar configuración Git global como parte del procedimiento.

Después de publicar, contrastar `refs/heads/main` con el commit local aprobado y el objeto tag/commit resuelto de `refs/tags/v1.1.0` con el tag local. Comprobar el contenido público desde esas referencias: la existencia previa de un repositorio vacío no demuestra distribución de esta versión. Informar PASS, FAIL o UNKNOWN según evidencia obtenida; no anunciar publicación exitosa antes de verificarla.

## Privacidad y reversibilidad
El registro privado de preparación conserva inventario/evidencia, pero no es dependencia de esta documentación pública. Los proyectos se inicializan manualmente desde `templates/projects-index.md`, según [instalación](installation.md).

Se conserva una copia privada byte a byte del README anterior y no se borran proyectos originales. Toda limpieza o retirada posterior del índice/repositorio es una acción separada y revisada; no hay rollback destructivo automático.
