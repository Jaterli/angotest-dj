import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AdminResultsFilter, AdminResultsResponse } from '../models/results-list.models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ResultsManagementService {
  private apiUrl = `${environment.apiUrl}/results`;

  constructor(private http: HttpClient) { }

  // Obtener resultados con filtros para administración
  getAdminResults(filter: AdminResultsFilter): Observable<AdminResultsResponse> {
    let params = this.buildFilterParams(filter);
    return this.http.get<AdminResultsResponse>(`${this.apiUrl}`, { params });
  }

  // Exportar resultados a CSV con filtros
  exportResults(filter: AdminResultsFilter): Observable<Blob> {
    let params = this.buildFilterParams(filter);
    
    return this.http.get(`${this.apiUrl}/export-csv/`, {
      params: params,
      responseType: 'blob'
    });
  }

  // Construir parámetros de filtro (método auxiliar)
  private buildFilterParams(filter: AdminResultsFilter): HttpParams {
    let params = new HttpParams();
    
    // Parámetros básicos
    params = params.set('page', (filter.page || 1).toString());
    params = params.set('page_size', (filter.page_size || 20).toString());
    
    // Parámetros de usuario
    Object.keys(filter).forEach(key => {
      const value = filter[key as keyof AdminResultsFilter];
      if (value !== undefined && value !== null && value !== 'all' && value !== '') {
        params = params.set(key, value.toString());
      }
    });
    return params;
  }

  // Eliminar resultado individual
  deleteResult(resultId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${resultId}/delete/`);
  }

  // Eliminar múltiples resultados
  deleteResultsBulk(resultIds: number[]): Observable<any> {
    return this.http.delete(`${this.apiUrl}/bulk-delete/`, {
      body: { ids: resultIds }
    });
  }
}