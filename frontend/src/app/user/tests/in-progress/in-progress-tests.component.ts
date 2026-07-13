import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { TestService } from '../../../shared/services/test.service';
import { AuthService } from '../../../shared/services/auth.service';
import { User } from '../../../shared/models/user.models';
import { SharedUtilsService } from '../../../shared/services/shared-utils.service';
import {
  InProgressTestsStats,
  InProgressTestsFilter,
  InProgressTest,
  TestAvailableFilters
} from '../../../shared/models/test.models';
import { toSignal } from '@angular/core/rxjs-interop';
import { SystemConfigServiceForUser } from '../../../shared/services/systemconfig.service';

@Component({
  selector: 'app-in-progress-tests',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './in-progress-tests.component.html',
})
export class InProgressTestsComponent implements OnInit {
  private testService = inject(TestService);
  private authService = inject(AuthService);
  private sharedUtilsService = inject(SharedUtilsService);
  private systemConfigServiceForUser = inject(SystemConfigServiceForUser);
  private router = inject(Router);

  // Tests y estado
  inProgressTestsData = signal<InProgressTest[]>([]);
  loading = signal(true);

  // Configuración de expiración (desde el servicio)
  expiredDays = toSignal(
    this.systemConfigServiceForUser.getSystemConfigByKey("MARK_IN_PROGRESS_AS_EXPIRED_AFTER_DAYS")
  );

  // Filtros (objeto único con tipado fuerte)
  selectedFilters = signal<InProgressTestsFilter>({
    page: 1,
    page_size: 10,
    ordering: 'updated_at',
    order_dir: 'desc',
    main_topic: 'all',
    level: 'all',
  });

  // Opciones para niveles (desde servicio compartido)
  levelOptions = this.sharedUtilsService.getSharedPredefinedLevels();
  availableFilters = signal<TestAvailableFilters>({ main_topics: [] });

  // Paginación (datos devueltos por el backend)
  totalPages = signal(0);
  hasMore = signal(false);

  // Estadísticas
  stats = signal<InProgressTestsStats>({
    total_filtered: 0,
    total_unfiltered: 0,
    total_questions_answered: 0,
    total_time_spent: 0,
    total_by_level: {
      Principiante: 0,
      Intermedio: 0,
      Avanzado: 0,
    },
  });

  // Usuario
  currentUser: User | null = null;

  // Estado de la UI
  showFilters = signal(false);

  // Clave para localStorage
  private readonly FILTER_STORAGE_KEY = 'in_progress_tests_filters';

  ngOnInit(): void {
    this.loadCurrentUser();
    this.loadSavedFilters();
    this.loadTests();
  }

  loadCurrentUser(): void {
    const currentUser = this.authService.currentUser();
    if (currentUser) {
      this.currentUser = currentUser;
    }
  }

  loadSavedFilters(): void {
    try {
      const saved = localStorage.getItem(this.FILTER_STORAGE_KEY);
      if (saved) {
        const filters = JSON.parse(saved);
        this.selectedFilters.update(f => ({
          ...f,
          main_topic: filters.mainTopic || 'all',
          level: filters.level || 'all',
          ordering: filters.sortBy || 'result_updated_at',
          order_dir: filters.sortOrder || 'desc',
          page_size: filters.pageSize || 10,
        }));
      }
    } catch (error) {
      console.error('Error loading saved filters:', error);
    }
  }

  saveFilters(): void {
    const f = this.selectedFilters();
    const filters = {
      mainTopic: f.main_topic,
      level: f.level,
      sortBy: f.ordering,
      sortOrder: f.order_dir,
      pageSize: f.page_size,
      timestamp: new Date().getTime(),
    };
    localStorage.setItem(this.FILTER_STORAGE_KEY, JSON.stringify(filters));
  }

  loadTests(): void {
    this.loading.set(true);

    // Construir el filtro a partir de selectedFilters
    const raw = this.selectedFilters();
    const filter: InProgressTestsFilter = {
      page: raw.page,
      page_size: raw.page_size,
      ordering: raw.ordering,
      main_topic: raw.main_topic,
      level: raw.level,
    };

    filter.ordering = raw.order_dir === 'desc' ? `-${raw.ordering}` : raw.ordering;
    
    this.testService.getMyInProgressTests(filter).subscribe({
      next: (res) => {
        this.inProgressTestsData.set(res.data);
        this.availableFilters.set(res.available_filters);
        this.totalPages.set(res.pagination.total_pages);
        this.hasMore.set(res.pagination.has_more);
        this.stats.set(res.stats);
        this.loading.set(false);
        this.saveFilters();
      },
      error: (err) => {
        console.error('Error al cargar tests en progreso:', err);
        this.loading.set(false);
      },
    });
  }

  // --- Métodos de filtros ---

  onFilterChange(): void {
    this.selectedFilters.update(f => ({ ...f, page: 1 }));
    this.loadTests();
  }

  resetFilters(): void {
    this.selectedFilters.set({
      page: 1,
      page_size: 10,
      ordering: 'updated_at',
      order_dir: 'desc',
      main_topic: 'all',
      level: 'all',
    });
    this.loadTests();
  }

  toggleSortOrder(): void {
    this.selectedFilters.update(f => ({
      ...f,
      order_dir: f.order_dir === 'asc' ? 'desc' : 'asc',
      page: 1,
    }));
    this.loadTests();
  }

  removeFilter(filterType: 'main_topic' | 'level'): void {
    this.selectedFilters.update(f => ({
      ...f,
      [filterType]: 'all',
      page: 1,
    }));
    this.loadTests();
  }

  setPageSize(size: number): void {
    this.selectedFilters.update(f => ({
      ...f,
      page_size: size,
      page: 1,
    }));
    this.loadTests();
  }

  // --- Paginación ---

  goToPage(page: number): void {
    const total = this.totalPages();
    if (page < 1 || page > total) return;
    this.selectedFilters.update(f => ({ ...f, page }));
    this.loadTests();
  }

  previousPage(): void {
    const current = this.selectedFilters().page;
    if (current > 1) {
      this.goToPage(current - 1);
    }
  }

  nextPage(): void {
    if (this.hasMore()) {
      this.goToPage(this.selectedFilters().page + 1);
    }
  }

  getPageNumbers(): number[] {
    return this.sharedUtilsService.getSharedPageNumbers(
      this.totalPages(),
      this.selectedFilters().page
    );
  }

  // --- Métodos de UI (getters) ---

  getSortOrderIcon(): string {
    return this.selectedFilters().order_dir === 'asc' ? '↑' : '↓';
  }

  getSortOrderLabel(): string {
    return this.selectedFilters().order_dir === 'asc' ? 'Ascendente' : 'Descendente';
  }

  getCurrentSortLabel(): string {
    const sortBy = this.selectedFilters().ordering || 'result_updated_at';
    const map: Record<string, string> = {
      'progress': 'Progreso',
      'test_created_at': 'Fecha del test',
      'test_level': 'Nivel',
      'result_started_at': 'Fecha de inicio',
      'result_updated_at': 'Última actualización',
      'result_time_taken': 'Tiempo empleado',
      'remaining_count': 'Preguntas restantes',
    };
    return map[sortBy] || 'Última actualización';
  }

  getStartIndex(): number {
    const page = this.selectedFilters().page;
    const size = this.selectedFilters().page_size;
    return (page - 1) * size + 1;
  }

  getEndIndex(): number {
    const page = this.selectedFilters().page;
    const size = this.selectedFilters().page_size;
    return Math.min(page * size, this.inProgressTestsData().length);
  }

  showFilterIndicators(): boolean {
    const f = this.selectedFilters();
    return f.main_topic !== 'all' || f.level !== 'all';
  }

  showPagination(): boolean {
    return this.totalPages() > 1;
  }

  // --- Métodos específicos de tests en progreso ---

  getExpiredDaysInfo(startedAt: string): { days: string, message: string } {
    if (!this.expiredDays() || !startedAt) {
      return { days: 'N/A', message: 'Días hasta su expiración' };
    }

    const expiredDays = parseInt(this.expiredDays() || '0', 10);
    if (expiredDays <= 0) {
      return { days: '∞', message: 'Sin límite de expiración' };
    }

    const startDate = new Date(startedAt);
    const currentDate = new Date();
    const diffTime = currentDate.getTime() - startDate.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    const remainingDays = expiredDays - diffDays;

    if (remainingDays <= 0) {
      return { days: '0', message: 'Test marcado como expirado' };
    } else {
      return { days: remainingDays.toString(), message: 'Días para expiración' };
    }
  }

  getProgressMessage(progress: number): string {
    if (progress === 0) return 'Recién comenzado';
    if (progress < 25) return 'En las primeras preguntas';
    if (progress < 50) return 'Menos de la mitad';
    if (progress < 75) return 'Más de la mitad';
    if (progress < 100) return 'Casi terminado';
    return 'Listo para finalizar';
  }

  calculatePercentage(total_answered: number, total_questions: number): number {
    return this.sharedUtilsService.sharedCalculatePercentage(total_answered, total_questions);
  }

  getRemainingQuestions(test: InProgressTest): number {
    return test.total_questions - test.answered_count;
  }

  getEstimatedTimeToComplete(test: InProgressTest): string {
    if (!test.answered_count || test.answered_count === 0 || !test.time_taken) return 'N/A';

    const timePerQuestion = test.time_taken / test.answered_count;
    const remainingQuestions = this.getRemainingQuestions(test);
    const estimatedTime = timePerQuestion * remainingQuestions;

    return this.formatTime(Math.round(estimatedTime));
  }

  // --- Acciones ---

  deleteTestProgress(testId: number): void {
    if (confirm('¿Estás seguro de que quieres reiniciar este test? Se perderá todo el progreso.')) {
      this.testService.deleteTestProgress(testId).subscribe({
        next: () => {
          this.inProgressTestsData.update(tests => tests.filter(t => t.test_id !== testId));
          this.router.navigate(['/tests', testId, 'start-single']);
        },
        error: (err) => {
          console.error('Error al eliminar progreso:', err);
          alert('Error al reiniciar el test. Inténtalo de nuevo.');
        }
      });
    }
  }

  // --- Métodos auxiliares (delegados a SharedUtilsService) ---

  getLevelBadgeClass(level: string): string {
    return this.sharedUtilsService.getSharedLevelBadgeClass(level);
  }

  getProgressColor(percentage: number): string {
    return this.sharedUtilsService.getSharedProgressColor(percentage);
  }

  getProgressBarEmpty(): string {
    return this.sharedUtilsService.getSharedProgressBarEmpty();
  }

  getProgressBarColor(progress: number): string {
    return this.sharedUtilsService.getSharedProgressBarColor(progress);
  }

  formatDate(dateString: string): string {
    return this.sharedUtilsService.sharedFormatDate(dateString);
  }

  formatDateTime(dateString: string): string {
    return this.sharedUtilsService.sharedFormatDateTime(dateString);
  }

  formatTimeShort(dateString: string): string {
    return this.sharedUtilsService.sharedFormatTimeShort(dateString);
  }

  formatTime(seconds: number): string {
    return this.sharedUtilsService.sharedFormatTime(seconds);
  }
}