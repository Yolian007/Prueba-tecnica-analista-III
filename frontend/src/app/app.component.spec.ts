import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { AppComponent } from './app.component';
import { ConciliacionService } from './services/conciliacion.service';
import { RespuestaConciliacion } from './models/conciliacion.model';

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;
  let componente: AppComponent;
  let servicio: jasmine.SpyObj<ConciliacionService>;

  const archivos = {
    facturas: new File(['x'], 'facturas.csv'),
    contabilidad: new File(['x'], 'contabilidad.csv')
  };

  const respuesta: RespuestaConciliacion = {
    resumen: { total_facturas: 2, correctas: 1, con_inconsistencia: 1 },
    resultados: []
  };

  beforeEach(() => {
    servicio = jasmine.createSpyObj<ConciliacionService>('ConciliacionService', ['procesarArchivos']);
    TestBed.configureTestingModule({
      providers: [{ provide: ConciliacionService, useValue: servicio }]
    });
    fixture = TestBed.createComponent(AppComponent);
    componente = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('muestra el resumen tras una conciliación exitosa', () => {
    servicio.procesarArchivos.and.returnValue(of(respuesta));
    componente.procesar(archivos);
    fixture.detectChanges();

    expect(componente.cargando).toBeFalse();
    expect(fixture.nativeElement.querySelector('app-resumen-conciliacion')).not.toBeNull();
    expect(fixture.nativeElement.textContent).toContain('Total facturas');
  });

  it('muestra el mensaje de error del backend', () => {
    servicio.procesarArchivos.and.returnValue(throwError(() => new HttpErrorResponse({
      status: 400,
      error: { detail: "El archivo 'x.csv' no contiene las columnas requeridas: id_factura." }
    })));
    componente.procesar(archivos);

    expect(componente.cargando).toBeFalse();
    expect(componente.mensajeError).toContain('columnas requeridas');
  });

  it('usa un mensaje genérico si el detalle no es texto (errores 422 de validación)', () => {
    servicio.procesarArchivos.and.returnValue(throwError(() => new HttpErrorResponse({
      status: 422,
      error: { detail: [{ msg: 'Field required' }] }
    })));
    componente.procesar(archivos);

    expect(componente.mensajeError).toBe('Error al procesar los archivos. Intente de nuevo.');
  });

  it('indica cuando el backend no está disponible', () => {
    servicio.procesarArchivos.and.returnValue(throwError(() => new HttpErrorResponse({ status: 0 })));
    componente.procesar(archivos);

    expect(componente.mensajeError).toContain('No se pudo conectar con el servidor');
  });
});
