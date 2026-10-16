# Conciliador de Facturas y Retenciones
**Prueba Técnica – Analista III**  
**Gerencia de Evolución Contable y Tributaria**

Aplicación web integral para la conciliación mensual automatizada entre el archivo de facturación de proveedores (`facturas.csv`) y los registros contabilizados (`contabilidad.csv`), detectando inconsistencias en valores monetarios, impuestos (IVA), retenciones, estados de contabilización, duplicidades e integridad de datos.

---

## 1. Descripción del Proyecto

El proceso manual de cruce de facturas consume horas de trabajo por parte de los analistas contables, está expuesto a imprecisiones por redondeo y dificulta la trazabilidad de discrepancias. Este prototipo resuelve dicho problema proveyendo:
1. Una interfaz web moderna en **Angular 17** para cargar los dos archivos y visualizar resultados en tiempo real.
2. Un motor analítico en **Python con FastAPI y Pandas**, que realiza cálculos monetarios de precisión estricta utilizando el tipo `Decimal`.
3. Trazabilidad completa por factura, indicando si es **Correcta** o **Con inconsistencia**, detallando todas las causas específicas encontradas.

---

## 2. Funcionalidades Implementadas

### Funcionalidades Principales
- **Carga de Archivos Dual:** Carga independiente de `facturas.csv` y `contabilidad.csv` con validación previa de selección.
- **Validación Estructural:** Verificación de encabezados, columnas requeridas, no vacuidad y compatibilidad de codificación (UTF-8, Latin-1, CP1252).
- **Cálculo de IVA Esperado:** `base_gravable × tarifa_iva` con redondeo estándar financiero (`ROUND_HALF_UP` a 2 decimales).
- **Cálculo de Total Esperado:** `base_gravable + iva_esperado − valor_retencion` (utilizando el IVA esperado para evitar arrastre de errores tributarios).
- **Detección de Facturas Duplicadas:** Identificación de identificadores repetidos en el archivo de facturación manteniendo todas las filas visibles.
- **Detección de Facturas sin Registro Contable:** Identificación de facturas ausentes en el archivo contable.
- **Validación de Integridad:** Reporte explícito de campos obligatorios vacíos (`nit_proveedor`, `fecha_factura`, `concepto`, etc.).
- **Resumen Ejecutivo:** Tarjetas con conteo total de facturas, cantidad de facturas correctas y cantidad con inconsistencias.
- **Tabla Detallada:** Visualización completa de cada factura (incluida la retención aplicada) con resaltado cromático de celdas divergentes (valores reportados vs. calculados) y etiquetas de estado.
- **Mensajes de Carga y Error:** Indicador de procesamiento, validación de extensión `.csv` en el navegador y presentación de los errores devueltos por la API (columnas faltantes, archivo vacío, backend no disponible).
- **Filtrado Dinámico:** Selector interactivo para filtrar por estado (`Todos`, `Correcta`, `Con inconsistencia`) con contador de registros mostrados.
- **Formateo Monetario:** Presentación de cifras en formato estándar de moneda colombiana (COP).

---

## 3. Arquitectura del Sistema

La solución adopta una arquitectura limpia y desacoplada de dos capas:

```
┌────────────────────────────────────────────────────────┐
│                   Frontend (Angular 17)                │
│  - AppComponent: orquesta estado y llamada a la API    │
│      * CargaArchivosComponent: selección y validación  │
│      * ResumenConciliacionComponent: tarjetas resumen  │
│      * TablaResultadosComponent: detalle y filtro      │
│  - MonedaCopPipe: formato de moneda COP                │
│  - ConciliacionService (HttpClient, FormData multipart) │
│  - Modelos TypeScript estrictos                        │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP POST /api/conciliacion (JSON)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                    │
│  - Routes & Controller (CORS, validaciones HTTP)       │
│  - Services:                                           │
│      * lector_csv: Lectura resiliente y validación     │
│      * validaciones: Normalización y parseo seguro     │
│      * conciliacion: Motor de reglas contables (Decimal)│
│  - Schemas: Modelos Pydantic tipados                   │
└────────────────────────────────────────────────────────┘
```

---

## 4. Requisitos del Sistema

- **Python:** 3.11, 3.12 o 3.13 (probado y validado en **Python 3.13.1** y **Python 3.12**)
  > ⚠️ **Python 3.14 no es compatible:** las versiones fijadas en `requirements.txt` (p. ej. `pandas==2.2.3`) no publican paquetes precompilados para 3.14 y la instalación falla. Si su `python`/`python3` por defecto es 3.14, cree el entorno virtual con una versión soportada (ver sección 5).
- **Node.js:** 18.x, 20.x, 22.x o 24.x (probado en **Node v24.14.1**)
- **npm:** 9.x o superior (probado en **npm 11.2.0**)
- **Angular CLI:** 17.3.11 (incluido localmente en dependencias del proyecto)

---

## 5. Instalación y Ejecución del Backend

1. **Abrir una terminal en la raíz del repositorio:**
   ```powershell
   cd backend
   ```

2. **Crear y activar el entorno virtual con Python 3.11, 3.12 o 3.13** (indicando la versión explícitamente):
   - En Windows (PowerShell):
     ```powershell
     py -3.13 -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - En Linux / macOS:
     ```bash
     python3.13 -m venv venv
     source venv/bin/activate
     ```
   *Si no tiene 3.13 instalado, reemplace `3.13` por `3.12` o `3.11`.*

   Verificar que el entorno quedó con la versión correcta:
   ```bash
   python --version   # Debe mostrar Python 3.11.x, 3.12.x o 3.13.x
   ```

3. **Instalar dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor FastAPI:**
   ```powershell
   python -m uvicorn app.main:app --reload --port 8000
   ```
   *El backend quedará escuchando en `http://localhost:8000`.*  
   *Documentación interactiva Swagger UI disponible en: `http://localhost:8000/docs`.*

---

## 6. Instalación y Ejecución del Frontend

1. **Abrir una segunda terminal en el directorio `frontend`:**
   ```powershell
   cd frontend
   ```

2. **Instalar las dependencias de Node:**
   ```powershell
   npm install
   ```

3. **Iniciar el servidor de desarrollo de Angular:**
   ```powershell
   npx ng serve --open
   ```
   *La aplicación se compilará y abrirá automáticamente en `http://localhost:4200`.*

---

## 7. Guía de Uso Paso a Paso

1. Iniciar tanto el backend (puerto 8000) como el frontend (puerto 4200).
2. Abrir el navegador en `http://localhost:4200`.
3. En la sección **Cargar Archivos**:
   - Hacer clic en *Seleccionar archivo* bajo la tarjeta **Facturas** y escoger `data/facturas.csv`.
   - Hacer clic en *Seleccionar archivo* bajo la tarjeta **Contabilidad** y escoger `data/contabilidad.csv`.
4. El botón **🔍 Procesar Conciliación** se habilitará automáticamente. Hacer clic sobre él.
5. De inmediato se desplegará:
   - **Resumen:** Total Facturas (50), Correctas (35), Con Inconsistencias (15).
   - **Tabla Detallada:** Listado completo con cada factura, celdas de IVA y Total con alertas visuales de discrepancia, y la lista de causas asociadas.
6. Usar el selector **Filtrar por estado** para visualizar únicamente facturas *Correctas* o *Con inconsistencia*.

---

## 8. Formato y Especificación de Archivos

### `facturas.csv`
Columnas requeridas:
- `id_factura`: Identificador alfanumérico único de la factura (e.g. `FAC-0001`).
- `nit_proveedor`: Identificación tributaria del proveedor.
- `fecha_factura`: Fecha de expedición (formato `YYYY-MM-DD`).
- `concepto`: Descripción del servicio o bien suministrado.
- `base_gravable`: Monto base sobre el que se calculan impuestos.
- `tarifa_iva`: Tarifa en formato decimal (e.g., `0.19` para 19%, `0.05` para 5%, `0.0` para exento).
- `valor_iva`: Valor del IVA reportado por el proveedor.
- `tarifa_retencion`: Tarifa de retención en la fuente (e.g., `0.04`, `0.025`, `0.035`).
- `valor_retencion`: Valor retenido informado en la factura.
- `total_factura`: Valor total a pagar reportado en la factura.

### `contabilidad.csv`
Columnas requeridas:
- `id_factura`: Identificador cruzado con facturas.
- `fecha_contabilizacion`: Fecha de registro contable.
- `cuenta_contable`: Código contable asignado.
- `centro_costo`: Centro de costo imputado.
- `valor_debito`: Débito del registro contable.
- `valor_credito`: Crédito del registro contable.
- `estado`: Estado del registro (`Contabilizada`, `Pendiente`).

---

## 9. Reglas de Negocio y Fórmulas Contables

1. **IVA Esperado:**
   $$\text{IVA Esperado} = \text{base\_gravable} \times \text{tarifa\_iva}$$
   Si el valor absoluto de la diferencia entre `valor_iva` y el IVA Esperado supera $0.01, se registra la inconsistencia **"Diferencia en IVA"**.

2. **Retención Esperada:**
   $$\text{Retención Esperada} = \text{base\_gravable} \times \text{tarifa\_retencion}$$
   Si el valor informado en `valor_retencion` difiere del cálculo teórico con base en la tarifa aplicada, se reporta la inconsistencia **"Diferencia en retención"**.

3. **Total Esperado:**
   $$\text{Total Esperado} = \text{base\_gravable} + \text{IVA Esperado} - \text{valor\_retencion}$$
   *Decisión de diseño:* Se utiliza el **IVA esperado** en el cálculo del total para evitar que un IVA erróneo reportado por el emisor enmascare o compense una discrepancia en el total facturado. Si el total reportado difiere del esperado, se registra la inconsistencia **"Diferencia en total"**.

4. **Detección de Duplicados:**
   Se evalúa la frecuencia de cada `id_factura`. Si un identificador aparece en más de una fila del archivo de facturación, cada una de sus ocurrencias es marcada como **"Factura duplicada"**.

5. **Factura sin Registro Contable:**
   Se contrasta el conjunto de `id_factura` de facturación contra los identificadores presentes en el archivo contable. Si no existe asiento para dicha factura, se reporta **"Factura sin registro contable"**.

6. **Estados de Contabilización (Auditoría Contable):**
   Se examina el estado del registro contable asociado. Si una factura figura en contabilidad con estado **"Pendiente"** (asiento no asentado en firme), se reporta **"Registro contable en estado Pendiente"**.

7. **Cruce de Valores Contables:**
   Se confronta el `total_factura` contra el importe debitado en contabilidad (`valor_debito`). Si el asiento no coincide con el total facturado, se anota **"Diferencia con valor en contabilidad"**.

8. **Campos Obligatorios Vacíos:**
   Si se detecta ausencia o vacuidad en campos indispensables (`nit_proveedor`, `fecha_factura`, `concepto`), se anota **"Campo obligatorio vacío: [nombre_campo]"**.

9. **Clasificación:**
   Una factura se clasifica como **"Correcta"** si y sólo si la lista de inconsistencias está vacía. En caso contrario se clasifica como **"Con inconsistencia"**.

---

## 10. Pruebas Automatizadas

El backend incluye una batería completa de **43 pruebas automatizadas con `pytest`** que verifican lectura de CSV (con detección de delimitadores `,`, `;` y `\t`), validaciones numéricas con `Decimal`, reglas de negocio contables desacopladas, servicio de aplicación, middleware y respuestas HTTP de la API REST.

Para ejecutar todas las pruebas (con el entorno virtual de la sección 5 ya creado):
- En Windows (PowerShell):
  ```powershell
  cd backend
  .\venv\Scripts\python.exe -m pytest tests -v
  ```
- En Linux / macOS:
  ```bash
  cd backend
  ./venv/bin/python -m pytest tests -v
  ```

### Cobertura de las Pruebas Backend:
- `tests/test_lector_csv.py`: Verificación de archivos válidos, archivos vacíos, columnas faltantes, tolerancia a columnas adicionales, detección automática de delimitadores (soporte para `;` y `,`) y codificaciones (UTF-8 / Latin-1).
- `tests/test_validaciones.py`: Conversión de números a Decimal, tipos inválidos, normalización de identificadores y rangos de tarifas.
- `tests/test_reglas.py`: Pruebas aisladas para cada regla de negocio (IVA, retenciones, totales, duplicados, ausencia contable, estado pendiente, diferencias de valor débito).
- `tests/test_conciliacion.py`: Facturas correctas, acumulación de múltiples fallas simultáneas y consistencia global del resumen.
- `tests/test_servicio_conciliacion.py`: Pruebas de integración de la capa de aplicación con inyección de dependencias.
- `tests/test_api.py`: Integración HTTP con `TestClient` sobre `/health`, `/` y `POST /api/conciliacion` (casos de éxito, error 400 por archivo faltante o corrupto, cabecera `X-Process-Time`).

### Pruebas del Frontend

El frontend incluye **17 pruebas unitarias con Jasmine/Karma** (ejecutables con Google Chrome o ChromeHeadless):
```bash
cd frontend
npx ng test --watch=false --browsers=ChromeHeadless
```
- `carga-archivos.component.spec.ts`: habilitación del botón, rechazo de archivos no CSV, emisión de archivos y estado de carga.
- `tabla-resultados.component.spec.ts`: filtro por estado, reinicio del filtro con nuevos resultados y mensaje sin coincidencias.
- `app.component.spec.ts`: resumen tras éxito y mensajes de error (400, 422 y backend no disponible).
- `conciliacion.service.spec.ts`: envío multipart con los campos que espera la API.
- `moneda-cop.pipe.spec.ts`: formato de moneda COP.

---

## 11. Resultados Obtenidos con los Datos de Prueba

Sobre el lote de prueba oficial (`data/facturas.csv` y `data/contabilidad.csv`), los resultados arrojados bajo la conciliación integral profunda son:

```json
{
  "total_facturas": 50,
  "correctas": 32,
  "con_inconsistencia": 18
}
```

### Detalle de Inconsistencias Detectadas:
- `FAC-0004`: **Factura duplicada** (filas 5 y 50) y **Diferencia con valor en contabilidad** (segunda ocurrencia por $2.213.500 vs. débito $3.659.250).
- `FAC-0006`: **Diferencia en IVA** (IVA reportado: $215.000 vs. Esperado: $190.000).
- `FAC-0007`: **Factura sin registro contable** (no figura en contabilidad).
- `FAC-0009`: **Diferencia en total** (Total reportado difiere de base + IVA esp. - ret).
- `FAC-0011`: **Registro contable en estado Pendiente** (registro contable no asentado en firme).
- `FAC-0013`: **Campo obligatorio vacío: nit_proveedor**.
- `FAC-0015`: **Factura duplicada** (filas 16 y 51) y **Diferencia con valor en contabilidad** (segunda ocurrencia por $3.425.100 vs. débito $3.603.250).
- `FAC-0018`: **Diferencia en IVA** (IVA reportado: $645.500 vs. Esperado: $655.500).
- `FAC-0021`: **Factura sin registro contable**.
- `FAC-0023`: **Diferencia en total**.
- `FAC-0027`: **Registro contable en estado Pendiente**.
- `FAC-0029`: **Campo obligatorio vacío: concepto**.
- `FAC-0034`: **Factura sin registro contable**.
- `FAC-0036`: **Diferencia en total**.
- `FAC-0039`: **Registro contable en estado Pendiente**.
- `FAC-0042`: **Factura sin registro contable** y **Campo obligatorio vacío: fecha_factura**.

---

## 12. Supuestos y Decisiones Técnicas

- **Uso de `Decimal`:** En lugar de `float`, todos los cálculos monetarios se realizan con la clase estándar `Decimal` y cuantización a dos decimales con `ROUND_HALF_UP`, evitando imprecisiones de coma flotante binaria.
- **Normalización de Identificadores:** Se aplica `.strip()` a los IDs para evitar que espacios en blanco accidentales (`"FAC-0001 "` vs `"FAC-0001"`) produzcan falsos negativos en el cruce.
- **Tratamiento de Duplicados:** No se descartan registros duplicados; se marcan explícitamente para permitir la auditoría de cada aparición.
- **Identidad Visual:** La interfaz usa una paleta inspirada en los colores institucionales del banco (amarillo `#FDDA24`, negro `#2C2A29` y blanco) definida en `frontend/src/styles/_variables.scss`. No se incluyen logotipos ni marcas registradas; la tipografía es Open Sans (Google Fonts), con fuentes del sistema como respaldo si no hay conexión a internet.
- **Registros Contables con Múltiples Líneas:** Para verificar la existencia de la factura en contabilidad se verifica si el identificador existe en el conjunto de registros contables.

---

## 13. Entregables Complementarios

- **Presentación Ejecutiva:** Disponible en formato Markdown en [`docs/presentacion_ejecutiva.md`](docs/presentacion_ejecutiva.md) y en formato interactivo listo para navegador en [`docs/presentacion_ejecutiva.html`](docs/presentacion_ejecutiva.html).
- **Declaración de Uso de IA:** Documento formal disponible en [`docs/declaracion_ia.md`](docs/declaracion_ia.md).
- **Archivos de Prueba:** Disponibles en la carpeta [`data/`](data/).
