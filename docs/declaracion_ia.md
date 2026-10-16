# Declaración del Uso de Inteligencia Artificial Generativa
**Prueba Técnica – Analista III**  
**Proyecto: Conciliador de Facturas y Retenciones**  

---

En cumplimiento de las pautas de transparencia de la prueba técnica, se declara formalmente el uso y alcance de herramientas de Inteligencia Artificial Generativa durante la concepción, desarrollo y documentación de este proyecto.

### 1. Herramientas Utilizadas
- **Modelo:** Gemini 3.8 / Claude Opus vía entorno de agente de desarrollo autónomo (Google Antigravity).
- **Rol:** Asistente de arquitectura, aceleración en generación de código base y elaboración de casos de prueba exhaustivos.

### 2. Ámbitos de Aplicación
- **Planificación y Estructuración:** Apoyo en el desglose de fases de trabajo, definición del contrato de API REST y esquemas Pydantic.
- **Backend (Python / FastAPI):**
  - Generación de la plantilla base de rutas, middleware CORS y servicios modulares (`lector_csv.py`, `validaciones.py`, `conciliacion.py`).
  - Creación de la suite de pruebas unitarias con `pytest` que evalúa 24 escenarios críticos (casos límite, archivos vacíos, codificación Latin-1, discrepancias aritméticas).
- **Frontend (Angular 17):**
  - Estructuración inicial de componentes standalone, servicios con `HttpClient`, tipado de interfaces TypeScript y maquetación SCSS responsiva sin dependencias externas.
- **Documentación y Presentación:**
  - Redacción preliminar del archivo `README.md` y estructura de la presentación ejecutiva de 5 diapositivas.

### 3. Verificación, Auditoría y Control Humano
- **Lógica Contable y Tributaria:** Cada una de las fórmulas de negocio (cálculo de IVA esperado con `ROUND_HALF_UP`, total esperado aislado de arrastres de error, regla de detección de duplicados sin exclusión y correspondencia con el archivo de contabilidad) fue analizada, verificada y auditada contra los datos reales entregados.
- **Pruebas de Ejecución:** Se ejecutaron pruebas reales de extremo a extremo comprobando el 100% de éxito en los 24 tests de pytest, la compilación de Angular 17 (`ng build` en 0 errores) y el cruce completo sobre el conjunto de 50 facturas entregadas en `facturas.csv` y `contabilidad.csv`.
- **Integridad del Código:** Todo el código generado fue inspeccionado para asegurar la ausencia de dependencias innecesarias, credenciales quemadas o código muerto.
