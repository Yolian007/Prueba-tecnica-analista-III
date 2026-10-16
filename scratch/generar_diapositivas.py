"""Script para generar la presentación ejecutiva en formato PowerPoint (.pptx)."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Dimensiones 16:9 panorámica
ANCHO = Inches(13.333)
ALTO = Inches(7.5)

# Paleta corporativa
COLOR_NEGRO = RGBColor(44, 42, 41)       # #2C2A29
COLOR_AMARILLO = RGBColor(253, 218, 36)  # #FDDA24
COLOR_BLANCO = RGBColor(255, 255, 255)   # #FFFFFF
COLOR_GRIS_FONDO = RGBColor(247, 247, 247)# #F7F7F7
COLOR_GRIS_BORDE = RGBColor(227, 227, 227)# #E3E3E3
COLOR_TEXTO_MUTED = RGBColor(107, 107, 107) # #6B6B6B
COLOR_EXITO = RGBColor(0, 135, 90)       # #00875A
COLOR_PELIGRO = RGBColor(200, 16, 46)    # #C8102E


def crear_diapositiva_base(prs, titulo, subtitulo_seccion="GERENCIA DE EVOLUCIÓN CONTABLE Y TRIBUTARIA"):
    """Crea una diapositiva con cabecera estándar institucional."""
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
    
    # Fondo general
    fondo = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, ANCHO, ALTO)
    fondo.fill.solid()
    fondo.fill.fore_color.rgb = COLOR_GRIS_FONDO
    fondo.line.fill.background()

    # Barra de cabecera oscura
    cabecera = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, ANCHO, Inches(1.3))
    cabecera.fill.solid()
    cabecera.fill.fore_color.rgb = COLOR_NEGRO
    cabecera.line.fill.background()

    # Línea amarilla decorativa
    linea = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.3), ANCHO, Inches(0.08))
    linea.fill.solid()
    linea.fill.fore_color.rgb = COLOR_AMARILLO
    linea.line.fill.background()

    # Texto en cabecera
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.18), Inches(11.5), Inches(0.95))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p_sub = tf.paragraphs[0]
    p_sub.text = subtitulo_seccion
    p_sub.font.size = Pt(11)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_AMARILLO
    
    p_tit = tf.add_paragraph()
    p_tit.text = titulo
    p_tit.font.size = Pt(22)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_BLANCO

    # Pie de diapositiva
    pie = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.5), Inches(0.35))
    p_pie = pie.text_frame.paragraphs[0]
    p_pie.text = "Conciliador de Facturas y Retenciones · Prueba Técnica Analista III"
    p_pie.font.size = Pt(10)
    p_pie.font.color.rgb = COLOR_TEXTO_MUTED

    return slide


def agregar_tarjeta(slide, x, y, ancho, alto, titulo="", bg_color=COLOR_BLANCO, borde_color=COLOR_GRIS_BORDE):
    """Agrega un contenedor tipo tarjeta en la diapositiva."""
    forma = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, ancho, alto)
    forma.fill.solid()
    forma.fill.fore_color.rgb = bg_color
    forma.line.color.rgb = borde_color
    forma.line.width = Pt(1)

    if titulo:
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), ancho - Inches(0.4), Inches(0.45))
        p = tb.text_frame.paragraphs[0]
        p.text = titulo
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEGRO

    return forma


def generar_presentacion(ruta_salida):
    prs = Presentation()
    prs.slide_width = ANCHO
    prs.slide_height = ALTO

    # ==========================================
    # DIAPOSITIVA 1: PORTADA
    # ==========================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, ANCHO, ALTO)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NEGRO
    bg1.line.fill.background()

    # Franja amarilla central
    franja = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.2), Inches(3.8))
    franja.fill.solid()
    franja.fill.fore_color.rgb = COLOR_AMARILLO
    franja.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(11.0), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "GERENCIA DE EVOLUCIÓN CONTABLE Y TRIBUTARIA"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMARILLO

    p = tf1.add_paragraph()
    p.text = "Conciliador de Facturas y Retenciones"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLANCO
    p.space_before = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Automatización y Cruce Mensual entre Proveedores y Registros Contables"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(220, 220, 220)
    p.space_before = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Prueba Técnica – Analista III · Prototipo Funcional de Alta Precisión"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_AMARILLO
    p.space_before = Pt(28)

    # ==========================================
    # DIAPOSITIVA 2: EL PROBLEMA Y EL OBJETIVO
    # ==========================================
    s2 = crear_diapositiva_base(prs, "1. Desafío Operativo y Objetivo de Negocio")
    
    # Tarjeta Izquierda: Problema
    agregar_tarjeta(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9), "El Problema Actual")
    tb2_izq = s2.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.1))
    tf2_izq = tb2_izq.text_frame
    tf2_izq.word_wrap = True

    items_problema = [
        ("Proceso Manual y Disperso:", "El cruce mensual entre facturación de proveedores y libros contables demanda horas de trabajo manual repetitivo."),
        ("Riesgo de Redondeo Financiero:", "Uso de hojas de cálculo o tipos coma flotante (float) que generan descuadres de centavos en cifras monetarias."),
        ("Dificultad de Trazabilidad:", "Falta de un reporte unificado que aísle con precisión la causal exacta de cada diferencia."),
        ("Exposición Tributaria:", "Riesgo de sanciones por inconsistencias en la liquidación de retenciones en la fuente y desajustes en el débito.")
    ]
    for i, (tit, desc) in enumerate(items_problema):
        p = tf2_izq.paragraphs[0] if i == 0 else tf2_izq.add_paragraph()
        p.text = f"•  {tit} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PELIGRO
        p.space_before = Pt(8) if i > 0 else Pt(0)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_NEGRO

    # Tarjeta Derecha: Objetivo
    agregar_tarjeta(s2, Inches(6.8), Inches(1.7), Inches(5.6), Inches(4.9), "El Objetivo del Prototipo")
    tb2_der = s2.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.2), Inches(4.1))
    tf2_der = tb2_der.text_frame
    tf2_der.word_wrap = True

    items_objetivo = [
        ("Conciliación Automatizada:", "Carga dual de facturas.csv y contabilidad.csv con procesamiento analítico en menos de 1 segundo."),
        ("Precisión Matemática Estricta:", "Uso exclusivo de Decimal y redondeo financiero ROUND_HALF_UP a dos decimales en todos los cálculos."),
        ("Auditoría Granular de Causales:", "Identificación independiente de errores en IVA, total, duplicados, ausencia contable y estado pendiente."),
        ("Interfaz Intuitiva en Español:", "Panel interactivo adaptado para el analista tributario con filtros dinámicos y alertas cromáticas.")
    ]
    for i, (tit, desc) in enumerate(items_objetivo):
        p = tf2_der.paragraphs[0] if i == 0 else tf2_der.add_paragraph()
        p.text = f"✔  {tit} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_EXITO
        p.space_before = Pt(8) if i > 0 else Pt(0)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_NEGRO

    # ==========================================
    # DIAPOSITIVA 3: ARQUITECTURA DEL SISTEMA
    # ==========================================
    s3 = crear_diapositiva_base(prs, "2. Arquitectura de Solución Desacoplada (Clean Code & SOLID)")

    # 3 Tarjetas Verticales
    tarjetas_arq = [
        ("Frontend (Angular 17)", Inches(0.8), [
            ("Arquitectura Standalone:", "Componentes modernos e independientes sin ngModules."),
            ("Carga y Validación:", "Filtro previo en navegador de formato .csv y tamaño."),
            ("Dashboard Ejecutivo:", "Métricas porcentuales y tabla interactiva con filtros dinámicos."),
            ("Diseño Corporativo:", "Tokens SCSS en paleta institucional, accesible y responsivo.")
        ]),
        ("Backend (Python / FastAPI)", Inches(4.8), [
            ("API REST Asíncrona:", "Controladores desacoplados con validación Pydantic."),
            ("Servicio de Aplicación:", "Inyección de dependencias mediante Depends()."),
            ("Ingesta Resiliente:", "Autodetección de delimitadores (',', ';', '\\t') y encoding UTF-8/Latin-1."),
            ("Observabilidad:", "Middleware de tiempos X-Process-Time y logging estructurado.")
        ]),
        ("Motor de Reglas Contables", Inches(8.8), [
            ("Patrón de Reglas Modulares:", "Cada regla contable encapsulada bajo Principio Abierto/Cerrado."),
            ("Aritmética Exacta:", "Uso de Decimal con ROUND_HALF_UP financiero."),
            ("No Propagación:", "Cálculo de total con IVA esperado para aislar distorsiones."),
            ("Batería de Pruebas:", "43 tests en Pytest y 21 en Jasmine/Karma (100% de éxito).")
        ])
    ]

    for tit, pos_x, items in tarjetas_arq:
        agregar_tarjeta(s3, pos_x, Inches(1.7), Inches(3.7), Inches(4.9), tit)
        tb = s3.shapes.add_textbox(pos_x + Inches(0.2), Inches(2.35), Inches(3.3), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, (subtit, txt) in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"• {subtit} "
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_NEGRO
            p.space_before = Pt(8) if i > 0 else Pt(0)
            run = p.add_run()
            run.text = txt
            run.font.bold = False
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_TEXTO_MUTED

    # ==========================================
    # DIAPOSITIVA 4: FLUJO Y REGLAS DE NEGOCIO
    # ==========================================
    s4 = crear_diapositiva_base(prs, "3. Reglas de Negocio y Auditoría Contable")

    tabla_shape = s4.shapes.add_table(6, 3, Inches(0.8), Inches(1.7), Inches(11.7), Inches(4.9))
    tabla = tabla_shape.table
    tabla.columns[0].width = Inches(2.8)
    tabla.columns[1].width = Inches(3.9)
    tabla.columns[2].width = Inches(5.0)

    encabezados = ["Regla Contable", "Fórmula / Criterio Aplicado", "Propósito de Auditoría Tributaria"]
    for j, enc in enumerate(encabezados):
        cell = tabla.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NEGRO
        p = cell.text_frame.paragraphs[0]
        p.text = enc
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_AMARILLO

    filas_reglas = [
        ("1. IVA Esperado", "Base Gravable × Tarifa IVA\n|IVA rep - IVA esp| > 0.01", "Detecta tarifas erróneas o cálculos imprecisos del proveedor."),
        ("2. Retención y Total", "Total = Base + IVA esp - Retención\n(Usa IVA teórico para no arrastrar error)", "Garantiza que errores en IVA no maquillen ni compensen el total facturado."),
        ("3. Detección de Duplicados", "Frecuencia > 1 en id_factura\n(Sin exclusión silenciosa de filas)", "Evita dobles pagos y permite auditar ambas apariciones repetidas."),
        ("4. Cruce Contable y Débito", "Cruce id_factura en contabilidad y\nTotal Factura == Valor Débito", "Detecta facturas sin contabilizar o con descuadre en el débito registrado."),
        ("5. Estado de Contabilización", "Auditoría de estado == 'Pendiente'", "Alerta sobre asientos contables en borrador que impiden el cierre fiscal.")
    ]

    for i, fila in enumerate(filas_reglas):
        for j, val in enumerate(fila):
            cell = tabla.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BLANCO if (i % 2 == 0) else RGBColor(240, 240, 240)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_NEGRO
            if j == 0:
                p.font.bold = True

    # ==========================================
    # DIAPOSITIVA 5: RESULTADOS DEL LOTE DE PRUEBA
    # ==========================================
    s5 = crear_diapositiva_base(prs, "4. Resultados Obtenidos en el Lote de Prueba (50 Facturas)")

    # 3 Tarjetas de métricas
    # Total
    c_tot = agregar_tarjeta(s5, Inches(0.8), Inches(1.6), Inches(3.6), Inches(1.3), "", COLOR_NEGRO)
    tb = s5.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(3.4), Inches(1.1))
    p = tb.text_frame.paragraphs[0]
    p.text = "TOTAL ANALIZADAS: 50"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_AMARILLO
    p2 = tb.text_frame.add_paragraph()
    p2.text = "100% de registros procesados"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_BLANCO

    # Correctas
    c_cor = agregar_tarjeta(s5, Inches(4.8), Inches(1.6), Inches(3.6), Inches(1.3), "", COLOR_BLANCO, COLOR_EXITO)
    tb = s5.shapes.add_textbox(Inches(4.9), Inches(1.7), Inches(3.4), Inches(1.1))
    p = tb.text_frame.paragraphs[0]
    p.text = "CORRECTAS: 32 (64%)"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_EXITO
    p2 = tb.text_frame.add_paragraph()
    p2.text = "Cero inconsistencias detectadas"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXTO_MUTED

    # Inconsistencias
    c_inc = agregar_tarjeta(s5, Inches(8.8), Inches(1.6), Inches(3.6), Inches(1.3), "", COLOR_BLANCO, COLOR_PELIGRO)
    tb = s5.shapes.add_textbox(Inches(8.9), Inches(1.7), Inches(3.4), Inches(1.1))
    p = tb.text_frame.paragraphs[0]
    p.text = "CON DISCREPANCIA: 18 (36%)"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_PELIGRO
    p2 = tb.text_frame.add_paragraph()
    p2.text = "Requieren plan de acción contable"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXTO_MUTED

    # Tabla resumen de causas
    tb_shape5 = s5.shapes.add_table(7, 3, Inches(0.8), Inches(3.1), Inches(11.7), Inches(3.6))
    t5 = tb_shape5.table
    t5.columns[0].width = Inches(3.2)
    t5.columns[1].width = Inches(1.5)
    t5.columns[2].width = Inches(7.0)

    encs5 = ["Causa de Inconsistencia", "Afectadas", "Ejemplos y Facturas Detectadas"]
    for j, enc in enumerate(encs5):
        cell = t5.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NEGRO
        p = cell.text_frame.paragraphs[0]
        p.text = enc
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_AMARILLO

    filas_resumen = [
        ("Diferencia en IVA", "2 facturas", "FAC-0006 ($215.000 reportado vs $190.000 esperado), FAC-0018 ($645.500 vs $655.500)."),
        ("Diferencia en Total Facturado", "3 facturas", "FAC-0009 ($4.484.000 vs $4.524.000), FAC-0023, FAC-0036."),
        ("Facturas Duplicadas / Cruce Débito", "4 filas (2 IDs)", "FAC-0004 (Fila 50: $2.213.500 vs débito $3.659.250), FAC-0015 (Fila 51 vs débito)."),
        ("Sin Registro en Contabilidad", "4 facturas", "FAC-0007, FAC-0021, FAC-0034, FAC-0042 (sin asiento registrado)."),
        ("Registro Contable en Estado 'Pendiente'", "3 facturas", "FAC-0011, FAC-0027, FAC-0039 (asientos no asentados definitivamente)."),
        ("Campos Obligatorios Vacíos", "3 facturas", "FAC-0013 (sin NIT), FAC-0029 (sin concepto), FAC-0042 (sin fecha).")
    ]

    for i, fila in enumerate(filas_resumen):
        for j, val in enumerate(fila):
            cell = t5.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BLANCO if (i % 2 == 0) else RGBColor(245, 245, 245)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_NEGRO
            if j == 0:
                p.font.bold = True
            if j == 1:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True

    # Nota de auditoría contable al pie de la tabla
    tb_nota = s5.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.4))
    p_nota = tb_nota.text_frame.paragraphs[0]
    p_nota.text = "* Nota de auditoría: La suma de causales (19) difiere del total de facturas físicas con discrepancia (18) porque la factura FAC-0042 presenta dos inconsistencias simultáneas (sin asiento contable y fecha de factura vacía)."
    p_nota.font.size = Pt(9.5)
    p_nota.font.italic = True
    p_nota.font.color.rgb = COLOR_TEXTO_MUTED

    # ==========================================
    # DIAPOSITIVA 6: BENEFICIOS Y HOJA DE RUTA
    # ==========================================
    s6 = crear_diapositiva_base(prs, "5. Beneficios de Negocio y Hoja de Ruta Productiva")

    # Tarjeta Izquierda: Beneficios
    agregar_tarjeta(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.9), "Beneficios Inmediatos de Negocio")
    tb6_izq = s6.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.1))
    tf6_izq = tb6_izq.text_frame
    tf6_izq.word_wrap = True

    items_ben = [
        ("Eficiencia Operativa Extrema:", "Reducción del tiempo de cruce mensual de ~2 horas a menos de 1 segundo por lote."),
        ("Cero Descuadres de Redondeo:", "Cálculo tributario exacto con Decimal, evitando diferencias acumuladas de centavos."),
        ("Trazabilidad y Calidad:", "Exposición unívoca de causales y 64 pruebas automatizadas (43 backend + 21 frontend)."),
        ("Reducción de Riesgo Fiscal:", "Mitigación proactiva de sanciones por retenciones o IVA no concordante con contabilidad.")
    ]
    for i, (tit, desc) in enumerate(items_ben):
        p = tf6_izq.paragraphs[0] if i == 0 else tf6_izq.add_paragraph()
        p.text = f"✔  {tit} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_EXITO
        p.space_before = Pt(8) if i > 0 else Pt(0)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_NEGRO

    # Tarjeta Derecha: Hoja de Ruta
    agregar_tarjeta(s6, Inches(6.8), Inches(1.7), Inches(5.6), Inches(4.9), "Hoja de Ruta para Fase Productiva")
    tb6_der = s6.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.2), Inches(4.1))
    tf6_der = tb6_der.text_frame
    tf6_der.word_wrap = True

    items_futuro = [
        ("Paginación y Virtual Scrolling:", "Soporte escalable para volúmenes superiores a 100.000 facturas mediante Server-Side Pagination."),
        ("Persistencia Relacional:", "Almacenamiento de cierres históricos en PostgreSQL o SQL Server con trazabilidad por analista."),
        ("Exportación de Reportes:", "Generación de informe de auditoría en Excel (.xlsx con formato corporativo) y PDF legal."),
        ("Seguridad Empresarial:", "Integración con Directorio Activo y Single Sign-On (SSO) bancario con perfiles de aprobación.")
    ]
    for i, (tit, desc) in enumerate(items_futuro):
        p = tf6_der.paragraphs[0] if i == 0 else tf6_der.add_paragraph()
        p.text = f"➔  {tit} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_NEGRO
        p.space_before = Pt(8) if i > 0 else Pt(0)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXTO_MUTED

    prs.save(ruta_salida)
    print(f"Presentación generada exitosamente en: {ruta_salida}")


if __name__ == "__main__":
    import os
    os.makedirs("docs", exist_ok=True)
    generar_presentacion("docs/presentacion_ejecutiva.pptx")
