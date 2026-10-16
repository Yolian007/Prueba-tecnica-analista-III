import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ResumenConciliacionComponent } from './resumen-conciliacion.component';
import { ResumenConciliacion } from '../../models/conciliacion.model';

describe('ResumenConciliacionComponent', () => {
  let fixture: ComponentFixture<ResumenConciliacionComponent>;
  let componente: ResumenConciliacionComponent;

  const resumenPrueba: ResumenConciliacion = {
    total_facturas: 50,
    correctas: 32,
    con_inconsistencia: 18
  };

  beforeEach(() => {
    fixture = TestBed.createComponent(ResumenConciliacionComponent);
    componente = fixture.componentInstance;
    fixture.componentRef.setInput('resumen', resumenPrueba);
    fixture.detectChanges();
  });

  it('calcula correctamente los porcentajes de facturas correctas e inconsistentes', () => {
    expect(componente.porcentaje(32)).toBe('64%');
    expect(componente.porcentaje(18)).toBe('36%');
    expect(componente.porcentaje(0)).toBe('0%');
  });

  it('muestra 0% cuando el total de facturas es cero', () => {
    fixture.componentRef.setInput('resumen', { total_facturas: 0, correctas: 0, con_inconsistencia: 0 });
    fixture.detectChanges();
    expect(componente.porcentaje(0)).toBe('0%');
  });

  it('renderiza las tarjetas con los valores correctos en el DOM', () => {
    const texto = fixture.nativeElement.textContent;
    expect(texto).toContain('50');
    expect(texto).toContain('32');
    expect(texto).toContain('18');
    expect(texto).toContain('Resumen de conciliación');
  });
});
