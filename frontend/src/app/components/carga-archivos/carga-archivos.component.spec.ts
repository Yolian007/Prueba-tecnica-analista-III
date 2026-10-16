import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CargaArchivosComponent } from './carga-archivos.component';
import { ArchivosConciliacion } from '../../models/conciliacion.model';

describe('CargaArchivosComponent', () => {
  let fixture: ComponentFixture<CargaArchivosComponent>;
  let componente: CargaArchivosComponent;

  beforeEach(() => {
    fixture = TestBed.createComponent(CargaArchivosComponent);
    componente = fixture.componentInstance;
    fixture.detectChanges();
  });

  function eventoCon(archivo: File): Event {
    const input = document.createElement('input');
    input.type = 'file';
    const transferencia = new DataTransfer();
    transferencia.items.add(archivo);
    input.files = transferencia.files;
    return { target: input } as unknown as Event;
  }

  function botonProcesar(): HTMLButtonElement {
    return fixture.nativeElement.querySelector('.boton-procesar');
  }

  it('deshabilita el botón de procesar hasta que se seleccionan ambos archivos', () => {
    expect(botonProcesar().disabled).toBeTrue();

    componente.seleccionar('facturas', eventoCon(new File(['x'], 'facturas.csv')));
    fixture.detectChanges();
    expect(botonProcesar().disabled).toBeTrue();

    componente.seleccionar('contabilidad', eventoCon(new File(['x'], 'contabilidad.csv')));
    fixture.detectChanges();
    expect(botonProcesar().disabled).toBeFalse();
  });

  it('rechaza archivos que no son CSV', () => {
    componente.seleccionar('facturas', eventoCon(new File(['x'], 'facturas.xlsx')));
    fixture.detectChanges();
    expect(componente.archivos.facturas).toBeUndefined();
    expect(fixture.nativeElement.querySelector('.mensaje-error').textContent).toContain('no es un CSV');
  });

  it('emite ambos archivos al procesar', () => {
    let emitido: ArchivosConciliacion | undefined;
    componente.procesar.subscribe(valor => (emitido = valor));

    componente.seleccionar('facturas', eventoCon(new File(['x'], 'facturas.csv')));
    componente.seleccionar('contabilidad', eventoCon(new File(['x'], 'contabilidad.csv')));
    fixture.detectChanges();
    botonProcesar().click();

    expect(emitido?.facturas.name).toBe('facturas.csv');
    expect(emitido?.contabilidad.name).toBe('contabilidad.csv');
  });

  it('muestra el estado de carga y bloquea el botón mientras procesa', () => {
    fixture.componentRef.setInput('cargando', true);
    fixture.detectChanges();
    expect(botonProcesar().disabled).toBeTrue();
    expect(fixture.nativeElement.textContent).toContain('Procesando');
  });
});
