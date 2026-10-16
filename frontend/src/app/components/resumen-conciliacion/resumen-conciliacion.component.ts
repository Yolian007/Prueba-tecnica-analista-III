import { Component, Input } from '@angular/core';
import { ResumenConciliacion } from '../../models/conciliacion.model';

@Component({
  selector: 'app-resumen-conciliacion',
  standalone: true,
  templateUrl: './resumen-conciliacion.component.html',
  styleUrl: './resumen-conciliacion.component.scss'
})
export class ResumenConciliacionComponent {
  @Input({ required: true }) resumen!: ResumenConciliacion;

  porcentaje(cantidad: number): string {
    if (!this.resumen.total_facturas) {
      return '0%';
    }
    return `${Math.round((cantidad / this.resumen.total_facturas) * 100)}%`;
  }
}
