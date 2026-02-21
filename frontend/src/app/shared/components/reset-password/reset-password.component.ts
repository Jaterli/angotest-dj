// reset-password.component.ts
import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './reset-password.component.html',
})

export class ResetPasswordComponent implements OnInit {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  form = this.fb.group({
    new_password: ['', [Validators.required, Validators.minLength(6)]],
    confirm_password: ['', [Validators.required, Validators.minLength(6)]]
  });

  loading = signal(false);
  invalidToken = signal(false);
  successMessage = signal<string>('');
  errorMessage = signal<string>('');
  token = signal<string>('');

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const token = params.get('token');
      if (token) {
        this.token.set(token);
        this.validateToken(token);
      } else {
        this.invalidToken.set(true);
      }
    });
  }

  validateToken(token: string) {
    this.loading.set(true);
    this.authService.validateResetToken(token).subscribe({
      next: (response) => {
        this.loading.set(false);
        if (!response.valid) {
          this.invalidToken.set(true);
        }
      },
      error: () => {
        this.loading.set(false);
        this.invalidToken.set(true);
      }
    });
  }

  get passwordMismatch(): boolean {
    const newPw = this.form.get('new_password')?.value;
    const confirmPw = this.form.get('confirm_password')?.value;
    return newPw !== confirmPw && confirmPw !== '';
  }

  onSubmit() {
    if (this.form.invalid || this.passwordMismatch) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.successMessage.set('');
    this.errorMessage.set('');

    const data = {
      token: this.token(),
      new_password: this.form.value.new_password!,
      confirm_password: this.form.value.confirm_password!
    };

    this.authService.resetPassword(data).subscribe({
      next: (response) => {
        this.loading.set(false);
        this.successMessage.set(
          response.message || 'Contraseña actualizada exitosamente'
        );
        this.form.disable();
        
        // Redirigir automáticamente después de 3 segundos
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 5000);
      },
      error: (error) => {
        this.loading.set(false);
        this.errorMessage.set(
          error.error?.message || 'Error al restablecer la contraseña'
        );
      }
    });
  }

    clearMessage() {
        this.errorMessage.set('');
        this.successMessage.set('');
    }

}