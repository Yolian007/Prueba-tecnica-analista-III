# Conciliador de Facturas y Retenciones
**Prueba Técnica – Analista III**  
**Gerencia de Evolución Contable y Tributaria**

Aplicación web integral para la conciliación mensual automatizada entre el archivo de facturación de proveedores (`facturas.csv`) y los registros contabilizados (`contabilidad.csv`), detectando inconsistencias en valores monetarios, impuestos (IVA), retenciones, estados de contabilización, duplicidades e integridad de datos.

---

## 1. Descripción del Proyecto y Propósito Funcional

El proceso manual de cruce de facturas consume horas de trabajo por parte de los analistas contables, está expuesto a imprecisiones por redondeo y dificulta la trazabilidad de discrepancias tributarias. Este prototipo resuelve dicho problema proveyendo:

1. **Interfaz Web de Auditoría (Angular 17 Standalone):** Permite al analista cargar de forma dual ambos archivos CSV, recibir validación inmediata en el cliente y consultar métricas ejecutivas y detalle tabular interactivo con filtros dinámicos.
2. **Motor Analítico de Alta Precisión (FastAPI + Pandas + Decimal):** Aplica reglas contables modulares con cálculo aritmético financiero estricto mediante la clase estándar `Decimal` (`ROUND_HALF_UP` a 2 decimales), eliminando el error por desbordamiento de coma flotante (`float`).
3. **Trazabilidad Completa y Clasificación Unívoca:** Cada factura es clasificada como **Correcta** o **Con inconsistencia**, detallando todas las causas específicas encontradas para facilitar el plan de acción contable.

---

## 2. Presentación para el Equipo Funcional

### ¿Cómo opera el proceso de conciliación para el analista?

```
    [facturas.csv]                     [contabilidad.csv]
          │                                    │
          └──────────────────┬─────────────────┘
                             ▼
              ┌─────────────────────────────┐
              │    Validación Estructural   │ -> Delimitador (, ; \t) y codificación (UTF-8 / Latin-1)
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │     Auditoría Tributaria    │ -> IVA esperado vs. IVA reportado
              │                             │ -> Retención esperada vs. Retención reportada
              │                             │ -> Total esperado vs. Total reportado
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │     Cruce de Contabilidad   │ -> Existencia en contabilidad (ausencia)
              │                             │ -> Débito contable vs. Total de factura
              │                             │ -> Estado de contabilización ("Contabilizada" vs. "Pendiente")
              │                             │ -> Detección de duplicados sin exclusión de filas
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │  Clasificación y Resumen    │ -> 32 Correctas (64%) | 18 Con inconsistencia (36%)
              └──────────────┬──────────────┘
                             ▼
      [Visualización Ejecutiva y Tabular en Angular 17]
```

### Material de Apoyo para Comités de Negocio
- **Diapositivas Ejecutivas en PowerPoint (.pptx):** [`docs/presentacion_ejecutiva.pptx`](docs/presentacion_ejecutiva.pptx) (Presentación profesional de 6 diapositivas con métricas, arquitectura, reglas de negocio y hoja de ruta).
- **Declaración Formal de Uso de IA:** [`docs/declaracion_ia.md`](docs/declaracion_ia.md).

---

## 3. Matriz de Versiones y Dependencias del Sistema

### Versiones de Entorno Probadas y Validadas

| Componente | Versión Recomendada | Versiones Compatibles | Estado de Verificación |
|---|:---:|:---:|:---:|
| **Python** | **3.13.1** | 3.11.x, 3.12.x, 3.13.x | Validado en local |
| **Node.js** | **v24.14.1** | 18.x, 20.x, 22.x, 24.x | Validado en local |
| **npm** | **11.2.0** | 9.x, 10.x, 11.x | Validado en local |
| **Angular CLI** | **17.3.11** | 17.3.x | Validado en local |

> ⚠️ **Incompatibilidad con Python 3.14:** La versión fijada de `pandas==2.2.3` no provee paquetes precompilados para Python 3.14 (aún en fase alpha). Utilice Python 3.11, 3.12 o 3.13.

### Dependencias Principales del Backend (`backend/requirements.txt`)

| Paquete | Versión Fijada | Propósito |
|---|:---:|---|
| `fastapi` | `0.115.6` | Framework asíncrono para la API REST |
| `uvicorn` | `0.34.0` | Servidor ASGI de alto rendimiento |
| `pydantic` | `2.10.4` | Validación de esquemas, tipado y contratos JSON |
| `pandas` | `2.2.3` | Procesamiento vectorial y manipulación estructurada de DataFrames |
| `python-multipart`| `0.0.20` | Procesamiento seguro de cargas `multipart/form-data` |
| `python-dotenv` | `1.0.1` | Carga de variables de entorno desde `.env` |
| `pytest` | `8.3.3` | Framework de pruebas automatizadas |
| `pytest-asyncio` | `0.25.0` | Soporte para pruebas unitarias de corrutinas asíncronas |
| `httpx` | `0.28.1` | Cliente HTTP de pruebas (`TestClient`) |

---

## 4. Configuración y Variables de Entorno

El backend soporta configuración mediante variables de entorno y archivos `.env`. Se provee una plantilla en [`.env.example`](.env.example) y [`backend/.env.example`](backend/.env.example):

```bash
# Servidor HTTP
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

# Metadatos del servicio
TITULO_PROYECTO="Conciliador de Facturas y Retenciones"
VERSION_PROYECTO="1.0.0"
DESCRIPCION_PROYECTO="Servicio backend para conciliación automática de facturas y registros contables."

# Seguridad y CORS (separados por coma si son múltiples)
ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200

# Nivel de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

---

## 5. Guía de Instalación y Ejecución Reproducible

### Paso 1: Configurar y Ejecutar el Backend

1. **Abrir una terminal en el directorio `backend`:**
   ```powershell
   cd backend
   ```

2. **Crear y activar el entorno virtual:**
   - En Windows (PowerShell):
     ```powershell
     py -3.13 -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - En Linux / macOS (Bash):
     ```bash
     python3.13 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias fijadas:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Copiar configuración de entorno (opcional):**
   ```powershell
   cp .env.example .env
   ```

5. **Iniciar el servidor de desarrollo:**
   ```powershell
   python -m uvicorn app.main:app --reload --port 8000
   ```
   - El servicio quedará escuchando en: `http://localhost:8000`
   - Endpoint de salud: `http://localhost:8000/salud`
   - Documentación Swagger interactiva: `http://localhost:8000/docs`

---

### Paso 2: Configurar y Ejecutar el Frontend

1. **Abrir una segunda terminal en el directorio `frontend`:**
   ```powershell
   cd frontend
   ```

2. **Instalar dependencias de Node:**
   ```powershell
   npm install
   ```

3. **Iniciar el servidor de Angular:**
   ```powershell
   npx ng serve --open
   ```
   - La aplicación compilará y se abrirá automáticamente en: `http://localhost:4200`

---

### Paso 3: Guía de Uso del Prototipo

1. Con ambos servicios activos, ingresar a `http://localhost:4200`.
2. En la sección **Cargar archivos**:
   - Seleccionar `data/facturas.csv` en la tarjeta **Facturas**.
   - Seleccionar `data/contabilidad.csv` en la tarjeta **Contabilidad**.
3. El botón **Procesar conciliación** se habilitará automáticamente.
4. Al hacer clic, el sistema procesará la conciliación en menos de 1 segundo y desplegará:
   - **Tarjetas de Resumen:** Total facturas (50), Correctas (32, 64%), Con inconsistencias (18, 36%).
   - **Tabla de Resultados:** Visualización exhaustiva con celdas discrepantes resaltadas cromáticamente en rojo y desglose de causales en la columna *Causas*.
   - **Selector de Filtro:** Permite filtrar instantáneamente por `Todos`, `Correcta` o `Con inconsistencia`.

---

## 6. Reglas de Negocio y Fórmulas Contables

Todas las operaciones monetarias se realizan con `Decimal` y redondeo `ROUND_HALF_UP` a 2 decimales:

1. **IVA Esperado:**
   > `IVA Esperado = base_gravable × tarifa_iva`
   
   Si `|valor_iva - IVA Esperado| > 0.01`, se marca la inconsistencia **"Diferencia en IVA"**.

2. **Retención Esperada:**
   > `Retención Esperada = base_gravable × tarifa_retencion`
   
   Si `|valor_retencion - Retención Esperada| > 0.01`, se marca la inconsistencia **"Diferencia en retención"**.

3. **Total Esperado (Aislamiento de Errores):**
   > `Total Esperado = base_gravable + IVA Esperado − valor_retencion`
   
   *Decisión de diseño:* Se utiliza el **IVA esperado** para calcular el total a pagar teórico, evitando que un error de IVA enmascare o compense una discrepancia en el total facturado. Si `|total_factura - Total Esperado| > 0.01`, se anota **"Diferencia en total"**.

4. **Detección de Duplicados:**
   Si un `id_factura` aparece repetido en el archivo de facturas, cada una de sus apariciones es marcada como **"Factura duplicada"** para auditoría completa sin descartar filas.

5. **Cruce de Existencia Contable:**
   Si la factura no tiene ningún asiento en `contabilidad.csv`, se marca como **"Factura sin registro contable"**.

6. **Auditoría de Estado de Contabilización:**
   Si el asiento contable figura con estado `"Pendiente"` (no asentado en firme), se reporta **"Registro contable en estado Pendiente"**.

7. **Cruce de Débito Contable:**
   Si el importe debitado en contabilidad (`valor_debito`) difiere del `total_factura`, se anota **"Diferencia con valor en contabilidad"**.

8. **Campos Obligatorios:**
   Si faltan datos indispensables (`nit_proveedor`, `fecha_factura`, `concepto`), se anota **"Campo obligatorio vacío: [campo]"**.

---

## 7. Resultados Obtenidos con los Datos de Prueba Oficiales

Sobre el lote oficial (`data/facturas.csv` y `data/contabilidad.csv`), los resultados arrojados son:

```json
{
  "total_facturas": 50,
  "correctas": 32,
  "con_inconsistencia": 18
}
```

### Detalle de Facturas con Inconsistencias:

| Factura | Estado | Causas Identificadas |
|---|:---:|---|
| `FAC-0004` | Con inconsistencia | Factura duplicada · Diferencia con valor en contabilidad (Fila 50: \$2.213.500 vs. débito \$3.659.250) |
| `FAC-0006` | Con inconsistencia | Diferencia en IVA (Reportado: \$215.000 vs. Esperado: \$190.000) |
| `FAC-0007` | Con inconsistencia | Factura sin registro contable |
| `FAC-0009` | Con inconsistencia | Diferencia en total (Reportado: \$4.484.000 vs. Esperado: \$4.524.000) |
| `FAC-0011` | Con inconsistencia | Registro contable en estado Pendiente |
| `FAC-0013` | Con inconsistencia | Campo obligatorio vacío: nit_proveedor |
| `FAC-0015` | Con inconsistencia | Factura duplicada · Diferencia con valor en contabilidad (Fila 51: \$3.425.100 vs. débito \$3.603.250) |
| `FAC-0018` | Con inconsistencia | Diferencia en IVA (Reportado: \$645.500 vs. Esperado: \$655.500) |
| `FAC-0021` | Con inconsistencia | Factura sin registro contable |
| `FAC-0023` | Con inconsistencia | Diferencia en total (Reportado: \$7.483.000 vs. Esperado: \$7.363.000) |
| `FAC-0027` | Con inconsistencia | Registro contable en estado Pendiente |
| `FAC-0029` | Con inconsistencia | Campo obligatorio vacío: concepto |
| `FAC-0034` | Con inconsistencia | Factura sin registro contable |
| `FAC-0036` | Con inconsistencia | Diferencia en total (Reportado: \$2.144.250 vs. Esperado: \$2.096.250) |
| `FAC-0039` | Con inconsistencia | Registro contable en estado Pendiente |
| `FAC-0042` | Con inconsistencia | Factura sin registro contable · Campo obligatorio vacío: fecha_factura |

---

## 8. Batería de Pruebas Automatizadas (64 Pruebas Totales)

### Pruebas de Backend (43 pruebas con Pytest)
Ejecutables con:
```powershell
cd backend
.\venv\Scripts\python.exe -m pytest tests -v
```
- `test_api.py` (7 tests): Integración HTTP sobre `/salud`, `/`, `POST /api/conciliacion` (éxito, archivos faltantes, CSV inválidos, cabecera `X-Process-Time`).
- `test_lector_csv.py` (8 tests): Lectura tolerante, delimitadores `,`, `;` y `\t`, codificaciones UTF-8 y Latin-1, columnas extra y validación de faltantes.
- `test_validaciones.py` (5 tests): Conversión de cadenas y números a `Decimal`, manejo seguro de nulos y validación de tarifas porcentuales.
- `test_reglas.py` (11 tests): Pruebas aisladas para cada regla modular del motor de conciliación.
- `test_servicio_conciliacion.py` (4 tests): Pruebas de la capa de aplicación con inyección de dependencias.
- `test_conciliacion.py` (8 tests): Casos de negocio combinados y consistencia de resumen global.

### Pruebas de Frontend (21 pruebas con Jasmine/Karma)
Ejecutables en modo headless:
```powershell
cd frontend
npx ng test --watch=false --browsers=ChromeHeadless
```
- `carga-archivos.component.spec.ts` (4 tests): Validación de archivos `.csv`, deshabilitación condicional del botón de envío y estados de carga.
- `resumen-conciliacion.component.spec.ts` (3 tests): Renderizado visual de tarjetas y cálculo porcentual exacto sobre totales analizados.
- `tabla-resultados.component.spec.ts` (5 tests): Filtro dinámico por estado, persistencia ante nuevas cargas y visualización del estado vacío.
- `app.component.spec.ts` (4 tests): Orquestación del estado, captura de errores 400/422 y desconexión del servidor.
- `conciliacion.service.spec.ts` (2 tests): Petición multipart con FormData y consumo del endpoint en español `/salud`.
- `moneda-cop.pipe.spec.ts` (3 tests): Formateo de moneda colombiana COP y manejo de valores nulos.

---

## 9. Identificación de Funcionalidades Incompletas y Limitaciones Técnicas

En apego al criterio de transparencia técnica y para evitar cualquier sobrepromesa funcional, se identifican las siguientes limitaciones del prototipo y su plan de mitigación productivo:

| Dimensión | Estado en el Prototipo Actual | Limitación / Funcionalidad Incompleta | Solución Propuesta para Producción |
|---|---|---|---|
| **Paginación y Volumen** | Renderizado en memoria del cliente Angular | Diseñado para lotes medianos (<5.000 filas). Para volúmenes empresariales (>100.000 registros), el renderizado DOM se degradaría. | Implementar paginación desde el servidor (`limit`/`offset` o cursor) y virtual scrolling (`cdk-virtual-scroll-viewport`). |
| **Persistencia de Datos** | Sin base de datos (procesamiento en memoria) | Los resultados de la conciliación viven en la sesión HTTP y se pierden al recargar la página. | Incorporar base de datos relacional (PostgreSQL / SQL Server) mediante SQLAlchemy para conservar el historial de cierres mensuales. |
| **Seguridad y Acceso** | Sin autenticación | No cuenta con control de acceso, inicio de sesión ni perfiles de usuario. | Integrar OAuth2 / OpenID Connect con Azure AD o Single Sign-On (SSO) bancario y control de roles (RBAC). |
| **Procesamiento Asíncrono** | Petición HTTP síncrona | La petición espera la respuesta del motor. Con archivos de gigabytes causaría un HTTP Timeout. | Implementar cola de tareas asíncronas con Celery / Redis y notificación de finalización vía WebSockets o polling. |
| **Exportación de Informes** | Filtrado e inspección en pantalla | No cuenta con botón de descarga en formatos de reporte para auditoría externa. | Agregar exportador a Excel (`openpyxl`) con formato corporativo y generación de informe ejecutivo en PDF. |
| **Cruce Multidireccional** | Facturas hacia débito contable | No concilia notas crédito, devoluciones, cuentas por pagar pasivas ni extractos bancarios de tesorería. | Extender el motor de reglas para cruces de 3 y 4 vías (Factura vs. Orden de Compra vs. Recepción vs. Asiento Contable). |

---

## 10. Declaración Específica del Uso de Inteligencia Artificial Generativa

En cumplimiento de las directrices de integridad técnica de la prueba:

- **Herramientas Utilizadas:** Modelos avanzados de lenguaje (Gemini 3.8 y Claude Opus) a través del entorno de desarrollo agéntico Google Antigravity.
- **Alcance de la Asistencia:**
  1. *Pair Programming y Refactorización:* Apoyo en la modularización hacia principios SOLID, desacoplamiento del motor de reglas y unificación de clases e identificadores 100% al español.
  2. *Formulación de Pruebas Unitarias:* Generación de casos límite para delimitar errores numéricos, codificaciones de archivo atípicas y respuestas de error HTTP.
  3. *Aceleración de Plantillas SCSS:* Creación de estilos responsivos basados en la paleta corporativa sin recurrir a bibliotecas de componentes externas.
- **Control y Auditoría Humana Estricta:**
  - Todas las fórmulas financieras fueron formuladas y auditadas manualmente exigiendo el uso de `Decimal`.
  - Cada una de las 18 inconsistencias fue cotejada contra los registros crudos de `facturas.csv` y `contabilidad.csv`.
  - Todas las 64 pruebas automatizadas fueron ejecutadas y verificadas localmente sin admitir código muerto o dependencias ficticias.

---

## 11. Estructura del Repositorio

```
Prueba-tecnica-analista-III/
├── .env.example                               # Plantilla de configuración de entorno global
├── README.md                                  # Documentación técnica y funcional principal
├── data/                                      # Archivos de prueba oficiales
│   ├── contabilidad.csv                       # 50 registros contables
│   └── facturas.csv                           # 50 facturas de proveedores
├── docs/                                      # Documentación ejecutiva complementaria
│   ├── declaracion_ia.md                      # Declaración formal de uso de IA
│   └── presentacion_ejecutiva.pptx            # Diapositivas ejecutivas en PowerPoint (16:9)
├── backend/                                   # Servicio API REST en Python
│   ├── .env.example                           # Configuración local del backend
│   ├── requirements.txt                       # Dependencias fijas de Python
│   ├── pytest.ini                             # Configuración del ejecutor de pruebas
│   ├── app/
│   │   ├── main.py                            # Punto de entrada FastAPI y middlewares
│   │   ├── api/routes.py                      # Rutas HTTP (/salud, /api/conciliacion)
│   │   ├── core/                              # Configuración y logger estructurado
│   │   ├── schemas/conciliacion.py            # Modelos y esquemas Pydantic
│   │   └── services/                          # Lógica de negocio y reglas desacopladas
│   │       ├── lector_csv.py                  # Ingesta resiliente de CSV
│   │       ├── validaciones.py                # Parseo y validaciones numéricas
│   │       ├── servicio_conciliacion.py       # Servicio de orquestación (Application Service)
│   │       ├── conciliacion.py                # Pipeline principal de conciliación
│   │       └── reglas/                        # Motor modular de reglas contables (SOLID)
│   └── tests/                                 # 43 pruebas automatizadas con pytest
└── frontend/                                  # Aplicación web en Angular 17 Standalone
    ├── package.json                           # Dependencias de npm y scripts
    ├── angular.json                           # Configuración del workspace de Angular
    ├── karma.conf.js                          # Configuración de pruebas Jasmine/Karma
    └── src/
        ├── styles.scss                        # Estilos globales y reset
        ├── styles/_variables.scss             # Tokens de diseño y variables corporativas
        └── app/
            ├── app.component.ts               # Orquestador principal de estado
            ├── components/
            │   ├── carga-archivos/            # Componente de subida y validación
            │   ├── resumen-conciliacion/      # Componente de tarjetas métricas
            │   └── tabla-resultados/          # Componente de detalle tabular y filtros
            ├── services/conciliacion.service.ts # Servicio HTTP cliente
            ├── pipes/moneda-cop.pipe.ts       # Pipe para formateo de moneda COP
            └── models/conciliacion.model.ts   # Contratos e interfaces TypeScript
```
