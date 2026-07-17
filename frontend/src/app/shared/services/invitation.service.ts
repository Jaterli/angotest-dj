import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, switchMap, of, map, catchError, throwError } from 'rxjs';
import { 
  TestInvitation, 
  CreateInvitationInput, 
  CheckInvitationResponse,
  AcceptInvitationResponse
} from '../models/invitation.models';
import { environment } from '../../../environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class InvitationService {
  private http = inject(HttpClient);
  private authService = inject(AuthService);  
  private apiUrl = `${environment.apiUrl}/invitations`;

  // Crear invitación
  createInvitation(data: CreateInvitationInput): Observable<any> {
    return this.http.post(`${this.apiUrl}/create/`, data);
  }

  // Verificar invitación
  checkInvitation(token: string): Observable<CheckInvitationResponse> {
    return this.http.get<CheckInvitationResponse>(`${this.apiUrl}/check-invitation/?token=${token}`);
  }

  acceptInvitation(token: string, asGuest?: boolean): Observable<AcceptInvitationResponse> {
    return this.http.post<AcceptInvitationResponse>(
      `${this.apiUrl}/accept-invitation/?token=${token}`,
      { as_guest: asGuest || false },
      { withCredentials: true } // Asegurar que la cookie se envía y recibe
    ).pipe(
      tap(response => {
        
        // El backend ya estableció la cookie auth_token
        // Actualizar el estado del usuario si viene en la respuesta
        if (response.user) {
          this.authService.setCurrentUser(response.user);
        } else {
          console.warn('⚠️ No se recibió usuario en la respuesta');
        }
      }),

      catchError(error => {
        console.error('❌ Error en acceptInvitation:', error);
        return throwError(() => error);
      })
    );
  }
}