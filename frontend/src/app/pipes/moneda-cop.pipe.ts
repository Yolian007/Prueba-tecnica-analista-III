import { Pipe, PipeTransform } from '@angular/core';

const FORMATO_COP = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  minimumFractionDigits: 0,
  maximumFractionDigits: 2
});

@Pipe({
  name: 'monedaCop',
  standalone: true
})
export class MonedaCopPipe implements PipeTransform {
  transform(valor: string | null | undefined): string {
    if (!valor) {
      return '—';
    }
    const numero = Number(valor);
    return Number.isNaN(numero) ? valor : FORMATO_COP.format(numero);
  }
}
