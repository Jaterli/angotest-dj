import { Component, OnInit, signal, inject } from '@angular/core';
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

  // Filtros (objeto único con tipado fuerte)
  selectedFilters = signal<CompletedTestsFilter>({
    page: 1,
    page_size: 10,
    ordering: 'updated_at',
    order_dir: 'desc',
    main_topic: 'all',
    level: 'all',
    from_date: '',
    to_date: '',
  });

  // Opciones para niveles (desde servicio compartido)
  levelOptions = this.sharedUtilsService.getSharedPredefinedLevels();
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

  // Clave para localStorage
  private readonly FILTER_STORAGE_KEY = 'completed_tests_filters';

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

    // Construir el filtro a partir de selectedFilters, limpiando valores 'all' o vacíos
    const raw = this.selectedFilters();
    const filter: CompletedTestsFilter = {
      page: raw.page,
      page_size: raw.page_size,
      ordering: raw.ordering,
      main_topic: raw.main_topic,
      level: raw.level,
    };

    filter.ordering = raw.order_dir === 'desc' ? `-${raw.ordering}` : raw.ordering;

    this.testService.getMyCompletedTests(filter).subscribe({
      next: (res) => {
        this.completedTestsData.set(res.data);
        this.totalPages.set(res.pagination.total_pages);
        this.hasMore.set(res.pagination.has_more);
        // this.currentPage.set(res.pagination.current_page);
        // this.pageSize.set(res.pagination.page_size);
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
      from_date: '',
      to_date: '',
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
    this.selectedFilters.update(f => ({ ...f, page_size: size }));
    this.selectedFilters.update(f => ({ ...f, current_page: 1 }));
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
    const map: Record<string, string> = {
      'test_title': 'Título del test',
      'test_created_at': 'Fecha del test',
      'result_started_at': 'Fecha de inicio',
      'result_updated_at': 'Fecha de finalización',
      'result_time_taken': 'Tiempo empleado',
      'score': 'Puntuación',
    };
    return map[this.selectedFilters().ordering || 'result_updated_at'];
  }

  getStartIndex(): number {
    const page = this.selectedFilters().page;
    const size = this.selectedFilters().page_size;
    return (page - 1) * size + 1;
  }

  getEndIndex(): number {
    const page = this.selectedFilters().page;
    const size = this.selectedFilters().page_size;
    return Math.min(page * size, this.completedTestsData().length);
  }

  showFilterIndicators(): boolean {
    const f = this.selectedFilters();
    return f.main_topic !== 'all' || f.level !== 'all';
  }

  showPagination(): boolean {
    return this.totalPages() > 1;
  }

  // --- Modal de revisión ---

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

  // --- Modal de invitación ---

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