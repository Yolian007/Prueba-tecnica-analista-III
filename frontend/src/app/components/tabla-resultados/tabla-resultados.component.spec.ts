import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TablaResultadosComponent } from './tabla-resultados.component';
import { ResultadoFactura } from '../../models/conciliacion.model';

function factura(id: string, estado: ResultadoFactura['estado'], inconsistencias: string[] = []): ResultadoFactura {
  return {
    id_factura: id,
    nit_proveedor: '900123456',
    fecha_factura: '2026-01-15',
    concepto: 'Servicio',
    base_gravable: '1000000.00',
    iva_reportado: '190000.00',
    iva_esperado: '190000.00',
    total_reportado: '1150000.00',
    total_esperado: '1150000.00',
    retencion_reportada: '40000.00',
    estado,
    inconsistencias
  };
}

describe('TablaResultadosComponent', () => {
  let fixture: ComponentFixture<TablaResultadosComponent>;
  let componente: TablaResultadosComponent;

  const datos = [
    factura('FAC-0001', 'Correcta'),
    factura('FAC-0002', 'Con inconsistencia', ['Diferencia en IVA']),
    factura('FAC-0003', 'Correcta')
  ];

  beforeEach(() => {
    fixture = TestBed.createComponent(TablaResultadosComponent);
    componente = fixture.componentInstance;
    fixture.componentRef.setInput('resultados', datos);
    fixture.detectChanges();
  });

  function filasVisibles(): number {
    return fixture.nativeElement.querySelectorAll('tbody tr:not(:has(.empty-state))').length;
  }

  function seleccionarFiltro(valor: string): void {
    const select: HTMLSelectElement = fixture.nativeElement.querySelector('select');
    select.value = valor;
    select.dispatchEvent(new Event('change'));
    fixture.detectChanges();
  }

  it('muestra todas las facturas por defecto', () => {
    expect(filasVisibles()).toBe(3);
  });

  it('filtra por estado Correcta', () => {
    seleccionarFiltro('Correcta');
    expect(filasVisibles()).toBe(2);
  });

  it('filtra por estado Con inconsistencia y muestra la causa', () => {
    seleccionarFiltro('Con inconsistencia');
    expect(filasVisibles()).toBe(1);
    expect(fixture.nativeElement.textContent).toContain('Diferencia en IVA');
  });

  it('reinicia el filtro cuando llegan nuevos resultados', () => {
    seleccionarFiltro('Correcta');
    fixture.componentRef.setInput('resultados', [...datos]);
    fixture.detectChanges();
    expect(componente.filtro).toBe('Todos');
    expect(filasVisibles()).toBe(3);
  });

  it('muestra un mensaje cuando el filtro no tiene coincidencias', () => {
    fixture.componentRef.setInput('resultados', [factura('FAC-0001', 'Correcta')]);
    fixture.detectChanges();
    seleccionarFiltro('Con inconsistencia');
    expect(fixture.nativeElement.querySelector('.empty-state')).not.toBeNull();
  });
});
