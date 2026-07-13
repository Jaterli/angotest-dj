import { Component, OnInit, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { TestService } from '../../../shared/services/test.service';
import { NotStartedTestsFilter, Test, NotStartedTestsStats, TestAvailableFilters } from '../../../shared/models/test.models';
import { AuthService } from '../../../shared/services/auth.service';
import { User } from '../../../shared/models/user.models';
import { SharedUtilsService } from '../../../shared/services/shared-utils.service';

@Component({
  selector: 'app-not-started-tests',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './not-started-tests.component.html',
})
export class NotStartedTestsComponent implements OnInit {
  private testService = inject(TestService);
  private authService = inject(AuthService);
  private sharedUtilsService = inject(SharedUtilsService);

  // Tests y estado
  notStartedTestsData = signal<Test[]>([]);
  loading = signal(true);

  // Filtros (objeto único con tipado fuerte)
  selectedFilters = signal<NotStartedTestsFilter & { order_dir?: 'asc' | 'desc' }>({
    page: 1,
    page_size: 10,
    ordering: 'test_created_at',
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
  stats = signal<NotStartedTestsStats>({
    total_filtered: 0,
    total_unfiltered: 0,
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
  private readonly FILTER_STORAGE_KEY = 'not_started_tests_filters';

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
          ordering: filters.sortBy || 'created_at',
          page_size: filters.pageSize || 10,
          order_dir: filters.sortOrder || 'desc',
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
      sortOrder: f.order_dir || 'desc',
      pageSize: f.page_size,
      timestamp: new Date().getTime(),
    };
    localStorage.setItem(this.FILTER_STORAGE_KEY, JSON.stringify(filters));
  }

  loadTests(): void {
    this.loading.set(true);

    const raw = this.selectedFilters();
    // Construir el filtro a partir de selectedFilters
    const filter: NotStartedTestsFilter = {
      page: raw.page,
      page_size: raw.page_size,
      main_topic: raw.main_topic,
      ordering: raw.ordering,
      level: raw.level,
    };

    filter.ordering = raw.order_dir === 'desc' ? `-${raw.ordering}` : raw.ordering;

    this.testService.getNotStartedTests(filter).subscribe({
      next: (res) => {
        this.notStartedTestsData.set(res.data);
        this.totalPages.set(res.pagination.total_pages);
        this.hasMore.set(res.pagination.has_more);
        this.stats.set(res.stats);
        this.availableFilters.set(res.available_filters);
        this.loading.set(false);
        this.saveFilters();
      },
      error: (err) => {
        console.error('Error al cargar tests:', err);
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
      ordering: 'created_at',
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
    const sortBy = this.selectedFilters().ordering || 'created_at';
    const map: Record<string, string> = {
      'title': 'Título',
      'created_at': 'Fecha de creación',
      'level': 'Nivel de dificultad',
      'total_questions': 'Número de preguntas',
    };
    return map[sortBy] || 'Fecha de creación';
  }

  getStartIndex(): number {
    const page = this.selectedFilters().page;
    const size = this.selectedFilters().page_size;
    return (page - 1) * size + 1;
  }

  getEndIndex(): number {
    const page = this.selectedFilters().page;
    const size = this.selectedFilters().page_size;
    return Math.min(page * size, this.notStartedTestsData().length);
  }

  showFilterIndicators(): boolean {
    const f = this.selectedFilters();
    return f.main_topic !== 'all' || f.level !== 'all';
  }

  showPagination(): boolean {
    return this.totalPages() > 1;
  }

  // --- Métodos auxiliares (delegados a SharedUtilsService) ---

  getLevelBadgeClass(level: string): string {
    return this.sharedUtilsService.getSharedLevelBadgeClass(level);
  }

  formatDate(dateString: string): string {
    return this.sharedUtilsService.sharedFormatDate(dateString);
  }
}