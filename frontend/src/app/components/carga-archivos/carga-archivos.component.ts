import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ArchivosConciliacion } from '../../models/conciliacion.model';

type TipoArchivo = keyof ArchivosConciliacion;

interface TarjetaCarga {
  tipo: TipoArchivo;
  titulo: string;
  icono: string;
  archivoEsperado: string;
}

@Component({
  selector: 'app-carga-archivos',
  standalone: true,
  templateUrl: './carga-archivos.component.html',
  styleUrl: './carga-archivos.component.scss'
})
export class CargaArchivosComponent {
  @Input() cargando = false;
  @Input() mensajeError: string | null = null;
  @Output() archivosCambiados = new EventEmitter<void>();
  @Output() procesar = new EventEmitter<ArchivosConciliacion>();

  readonly tarjetas: TarjetaCarga[] = [
    { tipo: 'facturas', titulo: 'Facturas', icono: '📄', archivoEsperado: 'facturas.csv' },
    { tipo: 'contabilidad', titulo: 'Contabilidad', icono: '📊', archivoEsperado: 'contabilidad.csv' }
  ];

  archivos: Partial<ArchivosConciliacion> = {};
  errorLocal: string | null = null;

  get puedeProcesar(): boolean {
    return !!this.archivos.facturas && !!this.archivos.contabilidad && !this.cargando;
  }

  get error(): string | null {
    return this.errorLocal ?? this.mensajeError;
  }

  seleccionar(tipo: TipoArchivo, event: Event): void {
    const input = event.target as HTMLInputElement;
    const archivo = input.files?.[0];
    // Limpiar el input permite volver a seleccionar el mismo archivo tras corregirlo
    input.value = '';
    if (!archivo) {
      return;
    }

    if (!archivo.name.toLowerCase().endsWith('.csv')) {
      this.errorLocal = `El archivo "${archivo.name}" no es un CSV. Seleccione un archivo con extensión .csv.`;
      return;
    }

    this.errorLocal = null;
    this.archivos = { ...this.archivos, [tipo]: archivo };
    this.archivosCambiados.emit();
  }

  enviar(): void {
    const { facturas, contabilidad } = this.archivos;
    if (facturas && contabilidad && !this.cargando) {
      this.procesar.emit({ facturas, contabilidad });
    }
  }
}
