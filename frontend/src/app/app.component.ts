import { Component } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { finalize } from 'rxjs';
import { ConciliacionService } from './services/conciliacion.service';
import { ArchivosConciliacion, RespuestaConciliacion } from './models/conciliacion.model';
import { CargaArchivosComponent } from './components/carga-archivos/carga-archivos.component';
import { ResumenConciliacionComponent } from './components/resumen-conciliacion/resumen-conciliacion.component';
import { TablaResultadosComponent } from './components/tabla-resultados/tabla-resultados.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CargaArchivosComponent, ResumenConciliacionComponent, TablaResultadosComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  cargando = false;
  mensajeError: string | null = null;
  resultados: RespuestaConciliacion | null = null;

  constructor(private conciliacionService: ConciliacionService) {}

  limpiarResultados(): void {
    this.resultados = null;
    this.mensajeError = null;
  }

  procesar({ facturas, contabilidad }: ArchivosConciliacion): void {
    this.cargando = true;
    this.limpiarResultados();

    this.conciliacionService.procesarArchivos(facturas, contabilidad)
      .pipe(finalize(() => (this.cargando = false)))
      .subscribe({
        next: respuesta => (this.resultados = respuesta),
        error: (err: HttpErrorResponse) => (this.mensajeError = this.describirError(err))
      });
  }

  private describirError(err: HttpErrorResponse): string {
    if (err.status === 0) {
      return 'No se pudo conectar con el servidor. Verifique que el backend esté en ejecución en ' +
        'http://localhost:8000.';
    }
    if (typeof err.error?.detail === 'string') {
      return err.error.detail;
    }
    return 'Error al procesar los archivos. Intente de nuevo.';
  }
}
