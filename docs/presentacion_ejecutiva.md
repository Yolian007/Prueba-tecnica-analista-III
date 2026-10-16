# Presentación Ejecutiva: Prototipo Conciliador de Facturas y Retenciones
**Gerencia de Evolución Contable y Tributaria**  
**Prueba Técnica – Analista III**  

---

## Diapositiva 1: Problema y Objetivo de Negocio

### El Desafío Actual
- **Proceso Manual y Disperso:** El cruce mensual entre las facturas emitidas por proveedores y los registros contables se realiza manualmente por analistas contables.
- **Riesgos Identificados:**
  - Alto consumo de tiempo y esfuerzo operativo redundante.
  - Vulnerabilidad a inconsistencias de redondeo y tarifas tributarias erróneas.
  - Falta de trazabilidad formal sobre por qué una factura difiere de la contabilidad.
  - Retrasos en el cierre contable mensual y posibles sanciones por retenciones mal practicadas.

### El Objetivo del Prototipo
Desarrollar una solución web automatizada, reproducible y confiable que:
1. Reciba los archivos mensuales de `facturas.csv` y `contabilidad.csv`.
2. Aplique reglas tributarias y contables estrictas de validación.
3. Clasifique cada factura con precisión y exponga las inconsistencias con sus causas exactas.
4. Reduzca el tiempo de conciliación de horas a segundos con total transparencia.

---

## Diapositiva 2: Solución Propuesta

### Arquitectura de la Solución
Un prototipo desacoplado de dos capas diseñado con altos estándares de ingeniería:

- **Frontend Interactivo (Angular 17):**
  - Carga intuitiva con validación previa de archivos CSV.
  - Indicadores ejecutivos en tiempo real (Tarjetas de métricas).
  - Tabla dinámica de detalle con filtrado instantáneo por estado.
  - Alerta visual en celdas con valores divergentes (IVA, Total).

- **Backend de Procesamiento (FastAPI + Pandas + Decimal):**
  - API REST asíncrona de alto rendimiento.
  - Validación de esquemas con Pydantic y tipado estricto.
  - **Aritmética monetaria exacta con `Decimal` (ROUND_HALF_UP a 2 decimales)**, erradicando los desbordamientos de coma flotante (`float`).

---

## Diapositiva 3: Flujo de Conciliación y Reglas de Negocio

```
[facturas.csv] + [contabilidad.csv]
                 │
                 ▼
       ┌───────────────────┐
       │ Ingesta & Limpieza│ -> Normalización de IDs, control de encoding
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ Detección Cruce   │ -> ¿Identificador repetido? (Factura duplicada)
       │                   │ -> ¿Existe en contabilidad? (Factura sin registro contable)
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ Cálculos Fiscales │ -> IVA esperado = Base Gravable × Tarifa IVA
       │                   │ -> Total esperado = Base Gravable + IVA esperado - Retención
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ Clasificación     │ -> "Correcta" (0 inconsistencias)
       │                   │ -> "Con inconsistencia" (Lista de causas trazables)
       └─────────┬─────────┘
                 │
                 ▼
      [Resumen + Detalle JSON -> Frontend Angular]
```

### Reglas Clave Implementadas
1. **Regla de No Propagación:** El total esperado se calcula sumando el `IVA esperado` (no el reportado). Si el proveedor reportó mal el IVA, se aíslan ambas fallas sin distorsionar el cálculo.
2. **Duplicidad Transparente:** Todas las instancias repetidas son marcadas para revisión sin supresión silenciosa.
3. **Validación de Integridad:** Se señalan campos vacíos indispensables (NIT, Concepto, Fecha).

---

## Diapositiva 4: Resultados Obtenidos en el Lote de Prueba

Al procesar los archivos de prueba entregados (50 facturas analizadas), el sistema arrojó los siguientes hallazgos:

| Métrica | Valor | Porcentaje |
|---|:---:|:---:|
| **Total Facturas Procesadas** | **50** | **100%** |
| **Facturas Correctas** | **35** | **70%** |
| **Facturas con Inconsistencias** | **15** | **30%** |

### Distribución de Inconsistencias Identificadas

| Causa de Inconsistencia | Facturas Afectadas | Ejemplo |
|---|:---:|---|
| **Diferencia en IVA** | 2 | FAC-0006 ($215.000 vs $190.000 esp.), FAC-0018 |
| **Diferencia en Total** | 3 | FAC-0009, FAC-0023, FAC-0036 |
| **Facturas Duplicadas** | 4 | FAC-0004 (2 registros), FAC-0015 (2 registros) |
| **Sin Registro Contable** | 4 | FAC-0007, FAC-0021, FAC-0034, FAC-0042 |
| **Campos Obligatorios Vacíos** | 3 | FAC-0013 (sin NIT), FAC-0029 (sin concepto), FAC-0042 (sin fecha) |

*Nota: FAC-0042 presentó múltiples causas simultáneas (sin registro contable y fecha vacía).*

---

## Diapositiva 5: Beneficios, Conclusiones y Próximos Pasos

### Beneficios Inmediatos
- **Ahorro Operativo:** Reducción del tiempo de cruce de ~2 horas a **< 1 segundo**.
- **Cero Errores de Redondeo:** Precisión contable garantizada mediante `Decimal`.
- **Trazabilidad Total:** Cada inconsistencia describe con precisión su causa contable/fiscal.
- **Experiencia de Usuario Intuitiva:** Interfaz en español adaptada al analista contable.

### Líneas de Evolución Futura (Fase Productiva)
1. **Exportación de Hallazgos:** Generación de informe ejecutivo en formato Excel/CSV para auditoría.
2. **Conciliación a Nivel de Cuentas Contables:** Comparación de saldo crédito/débito contra total de factura y validación de cuentas de retención en la fuente (e.g., cuenta 2365).
3. **Persistencia e Historial:** Registro histórico de lotes conciliados por mes y analista.
4. **Reglas Configurables:** Catálogo parametrizable de tarifas y umbrales de tolerancia de redondeo.
