import { Component, Input } from '@angular/core';
import { EstadoFactura, ResultadoFactura } from '../../models/conciliacion.model';
import { MonedaCopPipe } from '../../pipes/moneda-cop.pipe';

export type FiltroEstado = 'Todos' | EstadoFactura;

@Component({
  selector: 'app-tabla-resultados',
  standalone: true,
  imports: [MonedaCopPipe],
  templateUrl: './tabla-resultados.component.html',
  styleUrl: './tabla-resultados.component.scss'
})
export class TablaResultadosComponent {
  readonly opcionesFiltro: FiltroEstado[] = ['Todos', 'Correcta', 'Con inconsistencia'];

  filtro: FiltroEstado = 'Todos';
  private todos: ResultadoFactura[] = [];

  @Input({ required: true })
  set resultados(valor: ResultadoFactura[]) {
    this.todos = valor ?? [];
    this.filtro = 'Todos';
  }

  get resultados(): ResultadoFactura[] {
    return this.todos;
  }

  get filtrados(): ResultadoFactura[] {
    return this.filtro === 'Todos'
      ? this.todos
      : this.todos.filter(r => r.estado === this.filtro);
  }

  cambiarFiltro(event: Event): void {
    this.filtro = (event.target as HTMLSelectElement).value as FiltroEstado;
  }
}
