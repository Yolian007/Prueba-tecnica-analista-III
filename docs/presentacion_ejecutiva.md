# Presentación Ejecutiva: Prototipo Conciliador de Facturas y Retenciones
**Gerencia de Evolución Contable y Tributaria**  
**Prueba Técnica – Analista III**  

---

## Diapositiva 1: Problema y Objetivo de Negocio

### El Desafío Actual
- **Proceso Manual y Disperso:** El cruce mensual entre las facturas emitidas por proveedores y los registros contables se realiza manualmente por analistas contables.
- **Riesgos Identificados:**
  - Alto consumo de tiempo y esfuerzo operativo redundante en tareas de revisión mecánica.
  - Vulnerabilidad a inconsistencias de redondeo y tarifas tributarias erróneas.
  - Falta de trazabilidad formal sobre por qué una factura difiere de la contabilidad.
  - Riesgo de sanciones tributarias por retenciones en la fuente mal liquidadas o descuadres entre el débito contable y el total a pagar.

### El Objetivo del Prototipo
Desarrollar una solución web automatizada, reproducible y confiable que:
1. Reciba los archivos mensuales de `facturas.csv` y `contabilidad.csv`.
2. Aplique un motor modular de reglas tributarias y contables estrictas con precisión monetaria (`Decimal`).
3. Clasifique cada factura con precisión y exponga las inconsistencias con sus causas exactas e individualizadas.
4. Reduzca el tiempo de conciliación de horas a menos de 1 segundo con total transparencia para el analista.

---

## Diapositiva 2: Solución Propuesta

### Arquitectura de la Solución
Un prototipo desacoplado de dos capas diseñado bajo principios de Clean Code y SOLID:

- **Frontend Interactivo (Angular 17 Standalone):**
  - Carga dual intuitiva con validación previa de extensión y contenido.
  - Indicadores ejecutivos en tiempo real (Tarjetas métricas con barras de porcentaje).
  - Tabla dinámica de detalle con filtrado instantáneo por estado (`Todos`, `Correcta`, `Con inconsistencia`).
  - Alerta cromática en celdas con valores divergentes (IVA, Total) e identificación explícita de inconsistencias.
  - 100% en español y con diseño corporativo responsivo.

- **Backend de Procesamiento (FastAPI + Pandas + Decimal):**
  - API REST asíncrona de alto rendimiento con validación mediante Pydantic.
  - **Aritmética monetaria exacta con `Decimal` (ROUND_HALF_UP a 2 decimales)**, erradicando los desbordamientos de coma flotante (`float`).
  - **Motor Modular de Reglas (`MotorReglasConciliacion`):** cada validación contable es una clase independiente que cumple el principio de Responsabilidad Única y Abierto/Cerrado.
  - Detección inteligente de delimitadores CSV (`,`, `;`, `\t`) y codificaciones (`utf-8`, `latin-1`).

---

## Diapositiva 3: Flujo de Conciliación y Reglas de Negocio

```
[facturas.csv] + [contabilidad.csv]
                 │
                 ▼
       ┌───────────────────┐
       │ Ingesta & Limpieza│ -> Normalización de IDs, detección inteligente de delimitador
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
       │                   │ -> Retención esperada = Base Gravable × Tarifa Retención
       │                   │ -> Total esperado = Base + IVA esperado − Retención
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ Auditoría Contable│ -> ¿Estado en contabilidad == "Pendiente"?
       │                   │ -> ¿Valor débito contable != Total factura?
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
2. **Auditoría de Retenciones y Débitos:** Verificación matemática de la tarifa de retención aplicada y cruce contra el débito contable asentado.
3. **Auditoría de Estado Contable:** Detección de registros contables en estado "Pendiente" que impiden el cierre definitivo.
4. **Duplicidad Transparente:** Todas las instancias repetidas son marcadas para revisión sin supresión silenciosa.
5. **Validación de Integridad:** Se señalan campos vacíos indispensables (NIT, Concepto, Fecha).

---

## Diapositiva 4: Resultados Obtenidos en el Lote de Prueba

Al procesar los archivos oficiales de prueba entregados (50 facturas analizadas contra 50 registros contables), el sistema arrojó los siguientes hallazgos:

| Métrica | Valor | Porcentaje |
|---|:---:|:---:|
| **Total Facturas Procesadas** | **50** | **100%** |
| **Facturas Correctas** | **32** | **64%** |
| **Facturas con Inconsistencias** | **18** | **36%** |

### Distribución Detallada de Inconsistencias Identificadas

| Causa de Inconsistencia | Facturas Afectadas | Ejemplos Detectados |
|---|:---:|---|
| **Diferencia en IVA** | 2 | `FAC-0006` ($215.000 reportado vs. $190.000 esperado), `FAC-0018` |
| **Diferencia en Total Facturado** | 3 | `FAC-0009`, `FAC-0023`, `FAC-0036` |
| **Facturas Duplicadas con Cruce Débito** | 2 IDs (4 filas) | `FAC-0004` (filas 5 y 50; monto $2.213.500 vs. débito $3.659.250), `FAC-0015` |
| **Sin Registro en Contabilidad** | 4 | `FAC-0007`, `FAC-0021`, `FAC-0034`, `FAC-0042` |
| **Registro Contable en Estado "Pendiente"** | 3 | `FAC-0011`, `FAC-0027`, `FAC-0039` (asientos contables no legalizados) |
| **Campos Obligatorios Vacíos** | 3 | `FAC-0013` (sin NIT), `FAC-0029` (sin concepto), `FAC-0042` (sin fecha) |

*Nota: Facturas como `FAC-0004`, `FAC-0015` y `FAC-0042` acumulan múltiples inconsistencias simultáneas, todas expuestas con precisión.*

---

## Diapositiva 5: Beneficios, Conclusiones y Próximos Pasos

### Beneficios Inmediatos
- **Ahorro Operativo:** Reducción del tiempo de cruce de ~2 horas a **< 1 segundo**.
- **Cero Errores de Redondeo:** Precisión monetaria garantizada mediante el tipo estándar `Decimal`.
- **Trazabilidad Total:** Cada inconsistencia describe con claridad contable su causal específica.
- **Calidad y Cobertura:** **43 pruebas unitarias y de integración en backend** y **21 pruebas unitarias en frontend** (100% exitosas).

### Líneas de Evolución Futura (Fase Productiva)
1. **Paginación en Servidor y Procesamiento por Lotes:** Adaptación para archivos masivos (>50.000 facturas) con colas asíncronas (Celery/Redis).
2. **Persistencia e Historial en Base de Datos:** Guardado relacional en PostgreSQL/SQL Server con trazabilidad por analista y período fiscal.
3. **Exportación de Informes de Auditoría:** Generación automática de reportes en Excel (.xlsx) y PDF para radicación tributaria.
4. **Módulo de Autenticación y Autorización:** Integración con Directorio Activo / Single Sign-On (SSO) bancario.
