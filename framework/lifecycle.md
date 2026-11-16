# Ciclo de vida estándar

1. **DISCOVER**: reunir antecedentes, aclarar necesidades y separar hechos, supuestos y fuentes. Salida: contexto suficiente.
2. **DEFINE**: objetivo, fuera de alcance, restricciones, usuario destinatario, artefacto y criterios de aceptación. Salida: brief aprobado o supuesto documentado.
3. **PLAN**: pasos, dependencias, agentes/skills, riesgos, verificaciones y puntos de autorización. Salida: plan accionable.
4. **EXECUTE**: construir el artefacto del dominio. Salida: versión revisable y traza de decisiones.
5. **VERIFY**: revisar cumplimiento, hechos, calidad, seguridad y pruebas propias del dominio. Salida: informe con PASS / FAIL / UNKNOWN y evidencia.
6. **DELIVER**: consolidar los artefactos, explicar limitaciones y pendientes. Salida: entregable final con resumen.

**Bucles**: un fallo en VERIFY devuelve al paso apropiado; una nueva necesidad puede devolver a DISCOVER o DEFINE. No repetir ciclos sin aportar evidencia nueva.

**Tareas sencillas**: se puede comprimir el ciclo y resolver sin convocar subagentes; no se eliminan las obligaciones de claridad y honestidad.

**Quality gates**: antes de EXECUTE, criterios de aceptación presentes; antes de DELIVER, resultado de VERIFY documentado (incluido UNKNOWN cuando corresponda).
