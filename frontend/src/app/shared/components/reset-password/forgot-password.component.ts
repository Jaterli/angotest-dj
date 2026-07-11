// forgot-password.component.ts
import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './forgot-password.component.html'
})
export class ForgotPasswordComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]]
  });

  loading = signal(false);
  successMessage = signal<string>('');
  errorMessage = signal<string>('');

  onSubmit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.successMessage.set('');
    this.errorMessage.set('');

    const email = this.form.value.email!;

    this.authService.forgotPassword(email).subscribe({
      next: (response) => {
        this.loading.set(false);
        this.successMessage.set(
          response.message || 'Se ha enviado un enlace de recuperación a tu email.'
        );
        // Si estamos en desarrollo, mostrar el link
        if (response.reset_link) {
          this.successMessage.set(
            this.successMessage()
          );
        }
      },
      error: (error) => {
        this.loading.set(false);
        this.errorMessage.set(
          error.error?.message || 'Error al procesar la solicitud'
        );
      }
    });
  }

    clearMessage() {
        this.errorMessage.set('');
        this.successMessage.set('');
    }

}