# Contrato de revisión

Entrada: objetivo, criterios de aceptación, artefacto, fuentes y límites declarados.

Salida:
- `verdict`: PASS / FAIL / UNKNOWN
- `findings`: severidad (critical/high/medium/low), ubicación, observación, impacto, acción sugerida
- `acceptance_matrix`: criterio → PASS/FAIL/UNKNOWN → evidencia
- `untested`: elementos no verificados
- `recommendation`: aprobar / corregir / escalar al usuario

Reviewer debe mantener independencia crítica, no modificar el trabajo que audita y no asumir que una ejecución exitosa equivale a valor de negocio.
