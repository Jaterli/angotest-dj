// auth.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../shared/services/auth.service';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  
  // Obtener token del localStorage
  const token = localStorage.getItem('access_token');
  
  // Clonar la solicitud
  let reqWithAuth = req.clone({
    withCredentials: false  // No necesitamos cookies si usamos JWT en header
  });
  
  // Agregar token al header si existe
  if (token) {
    reqWithAuth = reqWithAuth.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  
  return next(reqWithAuth).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        console.log('Token inválido o expirado');
        auth.logout(false);
        router.navigate(['/login']);
      }
      
      if (error.status === 403) {
        console.log('Acceso denegado');
        router.navigate(['/forbidden']);
      }
      
      return throwError(() => error);
    })
  );
};