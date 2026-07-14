import { Component, OnInit, signal, computed, inject } from '@angular/core';
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
  private readonly defaultFilters: NotStartedTestsFilter = {
    page: 1,
    page_size: 10,
    ordering: 'created_at',
    order_dir: 'desc',
    main_topic: 'all',
    level: 'all',
  };
  selectedFilters = signal<NotStartedTestsFilter>(this.defaultFilters);

  // Estado de la UI
  showFilters = signal(false);

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

  // Opciones de ordenación (para la UI)
  sortOptions = [
    { value: 'title', label: 'Título' },
    { value: 'main_topic', label: 'Tema principal' },
    { value: 'level', label: 'Nivel' },    
    { value: 'created_at', label: 'Fecha de creación' },
    { value: 'question_count', label: 'Nº de preguntas' },

  ];
 
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
  private readonly FILTER_STORAGE_KEY = 'not_started_tests_filters';

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
    const filter: NotStartedTestsFilter = {
      ...raw,                          // Copia todos los campos
      ordering: raw.order_dir === 'desc' ? `-${raw.ordering}` : raw.ordering,
    };

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

  updateFilter<K extends keyof NotStartedTestsFilter>(key: K, value: NotStartedTestsFilter[K]): void {
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

  removeFilter(key: keyof NotStartedTestsFilter): void {
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

  // --- Métodos de UI (getters) ---

  getSortOrderIcon(): string {
    return this.selectedFilters().order_dir === 'asc' ? '↑' : '↓';
  }

  getSortOrderLabel(): string {
    return this.selectedFilters().order_dir === 'asc' ? 'Ascendente' : 'Descendente';
  }

  // --- Métodos auxiliares (delegados a SharedUtilsService) ---

  getLevelBadgeClass(level: string): string {
    return this.sharedUtilsService.getSharedLevelBadgeClass(level);
  }

  formatDate(dateString: string): string {
    return this.sharedUtilsService.sharedFormatDate(dateString);
  }
}