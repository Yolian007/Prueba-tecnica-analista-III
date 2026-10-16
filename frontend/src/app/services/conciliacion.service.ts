import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { RespuestaConciliacion } from '../models/conciliacion.model';

@Injectable({
  providedIn: 'root'
})
export class ConciliacionService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  procesarArchivos(facturas: File, contabilidad: File): Observable<RespuestaConciliacion> {
    const formData = new FormData();
    formData.append('facturas', facturas, facturas.name);
    formData.append('contabilidad', contabilidad, contabilidad.name);

    return this.http.post<RespuestaConciliacion>(`${this.apiUrl}/api/conciliacion`, formData);
  }

  verificarSalud(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/health`);
  }
}
