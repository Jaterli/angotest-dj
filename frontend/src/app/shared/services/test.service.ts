import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  SaveResultInput, 
  ResumeTestResponse, 
  TestsWithStatusResponse,
  Test,
  CompletedTestsFilter,
  InProgressTestsFilter,
  NextQuestionResponse, 
  NotStartedTestsFilter,
  InProgressTestResponse,
  CompletedTestsResponse,
  NotStartedTestsResponse
} from '../models/test.models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TestService {
  private apiUrl = `${environment.apiUrl}/test`;

  constructor(private http: HttpClient) {}

  // Obtener la siguiente pregunta sin responder
  getNextUnansweredQuestion(testId: number): Observable<NextQuestionResponse> {
    return this.http.get<NextQuestionResponse>(
      `${this.apiUrl}/${testId}/next-question/`
    );
  }

  getTestById(testId: number): Observable<Test> {
    return this.http.get<Test>(`${this.apiUrl}/${testId}`);
  }
  
  // Guardar progreso o finalizar test
  saveOrUpdateResult(data: SaveResultInput): Observable<any> {
    return this.http.post(`${this.apiUrl}/${data.test_id}/save/`, data);
  }

  // Obtener progreso de un test
  getTestProgress(testId: number): Observable<ResumeTestResponse> {
    return this.http.get<ResumeTestResponse>(`${this.apiUrl}/${testId}/progress/`);
  }

  // ====== Método para tests completados con filtros ======
  getMyCompletedTests(filter: CompletedTestsFilter): Observable<CompletedTestsResponse> {
    
    let params = new HttpParams()
    // Agregar todos los filtros a los parámetros
    Object.keys(filter).forEach(key => {
      const value = filter[key as keyof CompletedTestsFilter];
      if (value !== undefined && value !== null && value != 'all' && value !== '') {
        params = params.set(key, value.toString());
      }
    });

    return this.http.get<CompletedTestsResponse>(`${this.apiUrl}/completed/`, { params });
  }

  // ====== Método para tests en progreso con filtros ======
  getMyInProgressTests(filter: InProgressTestsFilter): Observable<InProgressTestResponse> {
    let params = new HttpParams()
    // Agregar todos los filtros a los parámetros
    Object.keys(filter).forEach(key => {
      const value = filter[key as keyof InProgressTestsFilter];
      if (value !== undefined && value !== null && value != 'all' && value !== '') {
        params = params.set(key, value.toString());
      }
    });
    return this.http.get<InProgressTestResponse>(`${this.apiUrl}/in-progress/`, { params });
  }
    
  // ======= Método para tests por hacer ======
  getNotStartedTests(filter: NotStartedTestsFilter): Observable<NotStartedTestsResponse> {
    let params = new HttpParams()
    // Agregar todos los filtros a los parámetros
    Object.keys(filter).forEach(key => {
      const value = filter[key as keyof NotStartedTestsFilter];
      if (value !== undefined && value !== null && value != 'all' && value !== '') {
        params = params.set(key, value.toString());
      }
    });

    return this.http.get<NotStartedTestsResponse>(`${this.apiUrl}/not-started/`, { params });
  }


  // Eliminar progreso de un test
  deleteTestProgress(testId: number): Observable<any> {
    console.log(`TestService: eliminando progreso del test ${testId}...`);
    return this.http.delete(`${this.apiUrl}/${testId}/progress/delete/`);
  }

  // Obtener todos los tests con estado
  getAllTestsWithStatus(): Observable<TestsWithStatusResponse> {
    console.log('TestService: obteniendo todos los tests con estado...');
    return this.http.get<TestsWithStatusResponse>(`${this.apiUrl}/with-status/`);
  }

}