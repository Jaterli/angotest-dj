import { Component, OnInit, signal, computed, inject } from '@angular/core';
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

  // Paginación (datos devueltos por el backend)
  totalPages = signal(0);
  hasMore = signal(false);

  // Filtros (objeto único con tipado fuerte)
  availableFilters = signal<TestAvailableFilters>({ main_topics: [] });

  private readonly defaultFilters: InProgressTestsFilter = {
    page: 1,
    page_size: 10,
    ordering: 'updated_at',
    order_dir: 'desc',
    main_topic: 'all',
    sub_topic: 'all',
    level: 'all',
  };
  selectedFilters = signal<InProgressTestsFilter>(this.defaultFilters);

  // Estado de la UI
  showFilters = signal(false);

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

  // Opciones de ordenación (para la UI)
  sortOptions = [
    { value: 'title', label: 'Título' },
    { value: 'main_topic', label: 'Tema principal' },
    { value: 'level', label: 'Nivel' },    
    { value: 'created_at', label: 'Fecha de creación' },
    { value: 'updated_at', label: 'Fecha de actualización' },
    { value: 'question_count', label: 'Número de preguntas' },
  ];
 

  // Opciones para niveles (desde servicio compartido)
  levelOptions = this.sharedUtilsService.getSharedPredefinedLevels();

  // Usuario
  currentUser: User | null = null;

  // Computed properties
  currentSortLabel = computed(() => {
    const ordering = this.selectedFilters().ordering || 'updated_at';
    const option = this.sortOptions.find(o => o.value === ordering);
    return option ? option.label : 'Fecha de actualización';
  });

  // Computed: índices de paginación
  startIndex = computed(() => (this.selectedFilters().page - 1) * this.selectedFilters().page_size + 1);
  endIndex = computed(() => Math.min(this.selectedFilters().page * this.selectedFilters().page_size, this.stats().total_filtered));

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

  // Clave para localStorage
  private readonly FILTER_STORAGE_KEY = 'in_progress_tests_filters';

  loadSavedFilters(): void {
    try {
      const savedFilters = localStorage.getItem(this.FILTER_STORAGE_KEY);
      if (savedFilters) {
        const filters = JSON.parse(savedFilters);
        this.selectedFilters.set({ ...this.selectedFilters(), ...filters });
      }
    } catch (error) {
      console.error('Error loading saved filters:', error);
    }
  }

  saveFilters(): void {
    const filters = {
      ...this.selectedFilters(),
      timestamp: new Date().getTime()
    };
    localStorage.setItem(this.FILTER_STORAGE_KEY, JSON.stringify(filters));
  }

  loadTests(): void {
    this.loading.set(true);
    
    // Construir el filtro para el servicio
    const raw = this.selectedFilters();
    const filter: InProgressTestsFilter = {
      ...raw,                          // Copia todos los campos
      ordering: raw.order_dir === 'desc' ? `-${raw.ordering}` : raw.ordering,
    };
   
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

  updateFilter<K extends keyof InProgressTestsFilter>(key: K, value: InProgressTestsFilter[K]): void {
    this.selectedFilters.update(f => ({ ...f, [key]: value }));
    if (key !== 'page') {
      // Al cambiar cualquier filtro que no sea página, resetear a página 1
      this.selectedFilters.update(f => ({ ...f, page: 1 }));
    }
    this.loadTests();
  }

  resetFilters(): void {
    this.selectedFilters.set({ ...this.defaultFilters });
    this.loadTests();
  }

  removeFilter(key: keyof InProgressTestsFilter): void {
    const defaultValue = this.defaultFilters[key] ?? '';
    this.updateFilter(key, defaultValue);
  }

  // --- Ordenamiento ---
  setSortBy(sortBy: string): void {
    this.updateFilter('ordering', sortBy);
  }

  toggleSortOrder(): void {
    const currentDir = this.selectedFilters().order_dir || 'desc';
    this.updateFilter('order_dir', currentDir === 'asc' ? 'desc' : 'asc');
  }

  // --- Paginación ---
  setPageSize(size: number): void {
    this.updateFilter('page_size', size);
  }

  goToPage(page: number): void {
    if (page < 1 || page > this.totalPages()) return;
    this.updateFilter('page', page);
  }

  previousPage(): void {
    if (this.selectedFilters().page > 1) {
      this.goToPage(this.selectedFilters().page - 1);
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


  // --- Utilidades UI --- 
  showFilterIndicators(): boolean {
    const f = this.selectedFilters();
    return !!(f.ordering || f.order_dir ||f.main_topic || f.level);
  }

  showPagination(): boolean {
    return this.stats().total_filtered > 0 && this.totalPages() > 1;
  }

  // --- Métodos para la UI ---
  getSortOrderIcon(): string {
    return this.selectedFilters().order_dir === 'asc' ? '↑' : '↓';
  }

  getSortOrderLabel(): string {
    return this.selectedFilters().order_dir === 'asc' ? 'Ascendente' : 'Descendente';
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