# Declaración del Uso de Inteligencia Artificial Generativa
**Prueba Técnica – Analista III**  
**Gerencia de Evolución Contable y Tributaria**  
**Proyecto: Conciliador de Facturas y Retenciones**  

---

En cumplimiento de las pautas de transparencia, ética y rigor técnico de la evaluación, se declara formalmente el uso, alcance y mecanismos de control humano aplicados sobre herramientas de Inteligencia Artificial Generativa durante el ciclo de vida de este proyecto.

---

### 1. Herramientas y Modelos Utilizados
- **Entorno:** Google Antigravity (Entorno de desarrollo agéntico avanzado).
- **Modelos:** Gemini 3.8 / Claude Opus.
- **Modalidad de Trabajo:** Pair programming interactivo (programación en parejas asistida por IA) guiado y validado en cada iteración por el desarrollador.

---

### 2. Ámbitos de Aplicación Específicos

#### A. Arquitectura y Diseño de Software
- Apoyo en la modularización de la arquitectura hacia Clean Architecture y principios SOLID:
  - Desacoplamiento del motor de reglas mediante el patrón de Reglas de Negocio (`ReglaConciliacion` y `MotorReglasConciliacion`).
  - Definición de esquemas de datos tipados con Pydantic (`ModeloBase`, `ResultadoFactura`, `RespuestaConciliacion`).
  - Creación del servicio de aplicación (`ServicioConciliacion`) e inyección de dependencias con `Depends()`.

#### B. Generación y Refactorización de Código
- **Backend (Python 3.13 / FastAPI):**
  - Asistencia en la implementación de la lectura flexible de archivos CSV con autodetección de delimitadores (`,`, `;`, `\t`) y codificaciones (`utf-8`, `latin-1`).
  - Refactorización para unificación 100% en español de identificadores, rutas (`/salud`) y módulos (`validaciones.py`).
  - Incorporación de middleware para medición del tiempo de procesamiento (`X-Process-Time`) y captura centralizada de excepciones.
- **Frontend (Angular 17 Standalone):**
  - Estructuración de componentes autónomos sin dependencias externas pesadas.
  - Maquetación y estilos responsivos en SCSS siguiendo tokens de diseño corporativo.
  - Migración completa de clases CSS al español (`.seccion-carga`, `.seccion-resumen`, `.tabla-resultados`, `.etiqueta-inconsistencia`, etc.).

#### C. Batería de Pruebas Automatizadas
- Aceleración en la formulación de casos de prueba exhaustivos:
  - **43 pruebas unitarias y de integración en backend con `pytest`** (validaciones numéricas con `Decimal`, reglas tributarias aisladas, delimitadores CSV, respuestas HTTP y control de errores 400/422).
  - **21 pruebas unitarias en frontend con Jasmine y Karma en ChromeHeadless** (ciclo de carga, deshabilitación condicional, filtros interactivos, cálculo de porcentajes y formato de moneda COP).

---

### 3. Verificación, Auditoría y Control Humano

El uso de IA generativa se limitó a tareas de aceleración, ideación y refactorización sintáctica. Toda decisión crítica fue auditada y verificada manualmente:

1. **Aritmética Financiera y Redondeo:**
   - Se verificó que ninguna operación tributaria dependiera de coma flotante binaria (`float`). Se exigió el uso estricto de `Decimal` con redondeo bancario/financiero `ROUND_HALF_UP` a dos decimales.
2. **Auditoría de Reglas Contables Colombianas:**
   - Se validaron manualmente los 50 registros del lote oficial de prueba (`facturas.csv` y `contabilidad.csv`), confirmando la detección exacta de las 18 inconsistencias (errores en cálculo de IVA, total facturado, duplicidades con valores cruzados, facturas ausentes en contabilidad y registros contables en estado "Pendiente").
3. **Cero Alucinaciones y Estabilidad de Entorno:**
   - Se inspeccionaron todas las dependencias del proyecto (`requirements.txt` y `package.json`), garantizando versiones fijas y compatibles con los entornos de ejecución requeridos (Python 3.11–3.13 y Node 18+).
   - Se comprobó la ejecución local exitosa de todas las pruebas automatizadas (43/43 en backend y 21/21 en frontend) y de la compilación de producción de Angular (`ng build` en 0 errores).
