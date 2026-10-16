export type EstadoFactura = 'Correcta' | 'Con inconsistencia';

export interface ResultadoFactura {
  id_factura: string;
  nit_proveedor: string;
  fecha_factura: string;
  concepto: string;
  base_gravable: string;
  iva_reportado: string;
  iva_esperado: string;
  total_reportado: string;
  total_esperado: string;
  retencion_reportada: string;
  estado: EstadoFactura;
  inconsistencias: string[];
}

export interface ResumenConciliacion {
  total_facturas: number;
  correctas: number;
  con_inconsistencia: number;
}

export interface RespuestaConciliacion {
  resumen: ResumenConciliacion;
  resultados: ResultadoFactura[];
}

export interface ArchivosConciliacion {
  facturas: File;
  contabilidad: File;
}
