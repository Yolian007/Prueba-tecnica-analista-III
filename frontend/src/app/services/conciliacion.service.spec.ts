import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ConciliacionService } from './conciliacion.service';
import { environment } from '../../environments/environment';

describe('ConciliacionService', () => {
  let servicio: ConciliacionService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()]
    });
    servicio = TestBed.inject(ConciliacionService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('envía ambos archivos como multipart con los nombres de campo que espera la API', () => {
    const facturas = new File(['a'], 'facturas.csv', { type: 'text/csv' });
    const contabilidad = new File(['b'], 'contabilidad.csv', { type: 'text/csv' });

    servicio.procesarArchivos(facturas, contabilidad).subscribe();

    const peticion = http.expectOne(`${environment.apiUrl}/api/conciliacion`);
    expect(peticion.request.method).toBe('POST');
    const cuerpo = peticion.request.body as FormData;
    expect((cuerpo.get('facturas') as File).name).toBe('facturas.csv');
    expect((cuerpo.get('contabilidad') as File).name).toBe('contabilidad.csv');
    peticion.flush({ resumen: { total_facturas: 0, correctas: 0, con_inconsistencia: 0 }, resultados: [] });
  });

  it('consulta el endpoint de salud del servicio en español (/salud)', () => {
    let respuestaSalud: any;
    servicio.verificarSalud().subscribe(resp => (respuestaSalud = resp));

    const peticion = http.expectOne(`${environment.apiUrl}/salud`);
    expect(peticion.request.method).toBe('GET');
    peticion.flush({ estado: 'ok', servicio: 'conciliador-contable' });

    expect(respuestaSalud).toEqual({ estado: 'ok', servicio: 'conciliador-contable' });
  });
});
