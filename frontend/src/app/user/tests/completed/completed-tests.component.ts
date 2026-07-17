import { Component, OnInit, signal, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { TestService } from '../../../shared/services/test.service';
import { AuthService } from '../../../shared/services/auth.service';
import { User } from '../../../shared/models/user.models';
import { SharedUtilsService } from '../../../shared/services/shared-utils.service';
import { CompletedTestsStats, CompletedTestsFilter, CompletedTest, TestAvailableFilters } from '../../../shared/models/test.models';
import { ModalComponent } from '../../../shared/components/modal.component';
import { ResultService } from '../../../shared/services/result.service';
import { InvitationCreateComponent } from '../../../shared/components/invitation/invitation-create.component';
import { CreateInvitationInput } from '../../../shared/models/invitation.models';

@Component({
  selector: 'app-completed-tests',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, ModalComponent, InvitationCreateComponent],
  templateUrl: './completed-tests.component.html',
})
export class CompletedTestsComponent implements OnInit {
  private testService = inject(TestService);
  private authService = inject(AuthService);
  private resultService = inject(ResultService);
  private sharedUtilsService = inject(SharedUtilsService);

  // Tests y estado
  completedTestsData = signal<CompletedTest[]>([]);
  loading = signal(true);

  // Configuración de filtros por defecto
  private readonly defaultFilters: CompletedTestsFilter = {
    page: 1,
    page_size: 10,
    ordering: 'updated_at',
    order_dir: 'desc',
    main_topic: 'all',
    level: 'all',
  };
  selectedFilters = signal<CompletedTestsFilter>(this.defaultFilters);

  // Opciones para niveles (desde servicio compartido)
  availableFilters = signal<TestAvailableFilters>({ main_topics: [] });

  // Paginación (datos devueltos por el backend)
  totalPages = signal(0);
  hasMore = signal(false);

  // Estadísticas
  stats = signal<CompletedTestsStats>({
    total_filtered: 0,
    total_unfiltered: 0,
    average_score: 0,
    total_time_spent: 0,
    total_questions_answered: 0,
  });

  // Usuario
  currentUser: User | null = null;

  // Estado de la UI
  showFilters = signal(false);

  // Modal para revisar respuestas
  showReviewModal = signal(false);
  reviewLoading = signal(false);
  reviewError = signal<string>('');
  selectedResult: any = null;
  incorrectQuestions = signal<any[]>([]);
  showCorrectAnswer = true;
  reviewSummary = signal<any>(null);

  // Modal para la invitación
  showInviteModal = signal(false);
  selectedTestForInvitation: CreateInvitationInput | null = null;

  // Opciones de ordenación (para la UI)
  sortOptions = [
    { value: 'test__title', label: 'Título del test' },
    { value: 'test__level', label: 'Nivel del test' },
    { value: 'started_at', label: 'Fecha de inicio' },
    { value: 'updated_at', label: 'Fecha de finalización' },
    { value: 'time_taken', label: 'Tiempo empleado' },
    { value: 'score', label: 'Puntuación' },
  ];

  // Computed properties
  currentSortLabel = computed(() => {
    const ordering = this.selectedFilters().ordering || 'updated_at';
    const option = this.sortOptions.find(o => o.value === ordering);
    return option ? option.label : 'Fecha de finalización';
  });

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
  private readonly FILTER_STORAGE_KEY = 'completed_tests_filters';

  loadSavedFilters(): void {
    try {
      const savedFilters = localStorage.getItem(this.FILTER_STORAGE_KEY);
      if (savedFilters) {
        const filters = JSON.parse(savedFilters);
        // Asignar directamente, asegurando que los valores por defecto se mantengan
        this.selectedFilters.set({ ...this.defaultFilters, ...filters });
      }
    } catch (error) {
      console.error('Error loading saved filters:', error);
    }
  }

  saveFilters(): void {
    const filters = {
      ...this.selectedFilters(),
      timestamp: new Date().getTime(),
    };
    localStorage.setItem(this.FILTER_STORAGE_KEY, JSON.stringify(filters));
  }

  loadTests(): void {
    this.loading.set(true);

    // Construir el filtro para el servicio
    const raw = this.selectedFilters();
    const filter: CompletedTestsFilter = {
      ...raw,
      ordering: raw.order_dir === 'desc' ? `-${raw.ordering}` : raw.ordering,
    };

    this.testService.getMyCompletedTests(filter).subscribe({
      next: (res) => {
        this.completedTestsData.set(res.data);
        this.totalPages.set(res.pagination.total_pages);
        this.hasMore.set(res.pagination.has_more);
        this.availableFilters.set(res.available_filters);
        this.stats.set(res.stats);
        this.loading.set(false);
        this.saveFilters();
      },
      error: (err) => {
        console.error('Error al cargar tests completados:', err);
        this.loading.set(false);
      },
    });
  }

  // --- Métodos de filtros (unificados) ---

  updateFilter<K extends keyof CompletedTestsFilter>(key: K, value: CompletedTestsFilter[K]): void {
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

  removeFilter(key: keyof CompletedTestsFilter): void {
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
    return !!(f.main_topic && f.main_topic !== 'all') || !!(f.level && f.level !== 'all');
  }

  showPagination(): boolean {
    return this.stats().total_filtered > 0 && this.totalPages() > 1;
  }

  getSortOrderIcon(): string {
    return this.selectedFilters().order_dir === 'asc' ? '↑' : '↓';
  }

  getSortOrderLabel(): string {
    return this.selectedFilters().order_dir === 'asc' ? 'Ascendente' : 'Descendente';
  }

  // --- Modal de revisión (mantenido igual) ---

  openReviewModal(completedTestData: CompletedTest): void {
    this.selectedResult = completedTestData;
    this.reviewLoading.set(true);
    this.reviewError.set('');
    this.showReviewModal.set(true);

    this.resultService.getIncorrectAnswers(this.selectedResult.id).subscribe({
      next: (response) => {
        this.incorrectQuestions.set(response.incorrect_questions || []);
        this.reviewSummary.set(response.summary || null);
        this.reviewLoading.set(false);
      },
      error: (err) => {
        console.error('Error al cargar respuestas incorrectas:', err);
        this.reviewError.set('No se pudieron cargar las respuestas incorrectas.');
        this.reviewLoading.set(false);
      },
    });
  }

  closeReviewModal(): void {
    this.showReviewModal.set(false);
    this.selectedResult = null;
    this.incorrectQuestions.set([]);
    this.reviewSummary.set(null);
    this.reviewError.set('');
  }

  hasIncorrectQuestions(): boolean {
    return this.incorrectQuestions().length > 0;
  }

  // --- Modal de invitación (mantenido igual) ---

  openInviteModal(testData: any): void {
    this.selectedTestForInvitation = testData;
    this.showInviteModal.set(true);
  }

  closeInviteModal(): void {
    this.showInviteModal.set(false);
    this.selectedTestForInvitation = null;
  }

  // --- Métodos auxiliares (delegados a SharedUtilsService) ---

  getLevelBadgeClass(level: string): string {
    return this.sharedUtilsService.getSharedLevelBadgeClass(level);
  }

  getAccuracyColor(accuracy: number): string {
    return this.sharedUtilsService.getSharedAccuracyColor(accuracy);
  }

  getScoreMessage(score: number): string {
    return this.sharedUtilsService.getSharedScoreMessage(score);
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