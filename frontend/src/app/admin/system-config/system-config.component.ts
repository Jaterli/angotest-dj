import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { SystemConfigService } from '../services/system-config.service';
import { SystemConfig, CreateSystemConfigDTO, UpdateSystemConfigDTO, DefaultSystemConfig } from '../models/system-config.models';
import { ModalComponent } from '../../shared/components/modal.component';

@Component({
  selector: 'app-system-config',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, ModalComponent],
  templateUrl: './system-config.component.html'
})
export class SystemConfigComponent implements OnInit {
  private systemConfigService = inject(SystemConfigService);

  // Signals
  configs = signal<SystemConfig[]>([]);
  filteredConfigs = signal<SystemConfig[]>([]);
  loading = signal(true);
  errorMessage = signal('');
  
  // Modal signals
  showCreateModal = signal(false);
  showEditModal = signal(false);
  showDeleteModal = signal(false);
  showSuccessModal = signal(false);
  showErrorModal = signal(false);
  showImportModal = signal(false);

  // Current item signals
  currentConfig = signal<SystemConfig | null>(null);
  configToDelete = signal<SystemConfig | null>(null);

  // Form data signals
  newConfig = signal<CreateSystemConfigDTO>({ key: '', value: '', description: '' });
  editConfig = signal<UpdateSystemConfigDTO>({});

  // Filter signals
  searchTerm = signal('');
  filterOptions = signal({
    sortBy: 'key',
    sortOrder: 'asc'
  });

  // Opciones de ordenación disponibles
  sortOptions = signal([
    { value: 'key', label: 'Clave' },
    { value: 'value', label: 'Valor' },
    { value: 'updated_at', label: 'Fecha actualización' },
    { value: 'created_at', label: 'Fecha creación' }
  ]);

  // Estado de la UI
  showFilters = signal(false);


  // Estado para mostrar/ocultar información de configuraciones
  showConfigInfo = signal(false);

  // Información de configuraciones predeterminadas (obtenida de la API)
  defaultConfigsInfo = signal<DefaultSystemConfig[]>([]);
  loadingDefaults = signal(false);

  // Computed properties para el template
  currentSortLabel = computed(() => {
    const sortBy = this.filterOptions().sortBy;
    const option = this.sortOptions().find(o => o.value === sortBy);
    return option ? option.label : 'Clave';
  });

  getSortOrderIcon(): string {
    const order = this.filterOptions().sortOrder || 'asc';
    return order === 'asc' ? '↑' : '↓';
  }

  isLoading = computed(() => this.loading());

  constructor() {}

  ngOnInit(): void {
    this.loadConfigs();
    this.loadDefaultConfigs();
  }

  loadConfigs(): void {
    this.loading.set(true);
    this.systemConfigService.getAll().subscribe({
      next: (configs) => {
        this.configs.set(configs);
        this.applyFilters();
        this.loading.set(false);
      },
      error: (error) => {
        this.errorMessage.set('Error al cargar las configuraciones.');
        this.showErrorModal.set(true);
        this.loading.set(false);
      }
    });
  }

loadDefaultConfigs(): void {
    this.loadingDefaults.set(true);
    this.systemConfigService.getAllDefault().subscribe({
      next: (defaultConfigs) => {
        this.defaultConfigsInfo.set(defaultConfigs);
        this.loadingDefaults.set(false);
      },
      error: (error) => {
        console.error('Error al cargar configuraciones predeterminadas:', error);
        this.loadingDefaults.set(false);
      }
    });
  }

  missingConfigs = computed(() => {
    return this.defaultConfigsInfo().filter(c => !c.exists_in_db);
  });

  applyFilters(): void {
    let filtered = [...this.configs()];
    
    // Aplicar búsqueda
    if (this.searchTerm()) {
      const term = this.searchTerm().toLowerCase();
      filtered = filtered.filter(config =>
        config.key.toLowerCase().includes(term) ||
        config.value.toLowerCase().includes(term) ||
        (config.description && config.description.toLowerCase().includes(term))
      );
    }

    // Aplicar ordenación
    filtered.sort((a, b) => {
      const order = this.filterOptions().sortOrder === 'asc' ? 1 : -1;
      switch (this.filterOptions().sortBy) {
        case 'key':
          return order * a.key.localeCompare(b.key);
        case 'value':
          return order * a.value.localeCompare(b.value);
        case 'updated_at':
          return order * (new Date(a.updated_at).getTime() - new Date(b.updated_at).getTime());
        case 'created_at':
          return order * (new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        default:
          return 0;
      }
    });

    this.filteredConfigs.set(filtered);
  }

  onSearchChange(): void {
    this.applyFilters();
  }

  onFilterChange(): void {
    this.applyFilters();
  }

  resetFilters(): void {
    this.searchTerm.set('');
    this.filterOptions.set({
      sortBy: 'key',
      sortOrder: 'asc'
    });
    this.applyFilters();
  }

  toggleSortOrder(): void {
    const currentOrder = this.filterOptions().sortOrder || 'asc';
    const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    this.filterOptions.update(filters => ({ ...filters, sortOrder: newOrder }));
    this.applyFilters();
  }

  setSortBy(sortBy: string): void {
    this.filterOptions.update(filters => ({ ...filters, sortBy }));
    this.applyFilters();
  }

  showFilterIndicators(): boolean {
    return !!(this.searchTerm());
  }

  removeFilter(key: string): void {
    if (key === 'search') {
      this.searchTerm.set('');
      this.applyFilters();
    }
  }

  openCreateModal(): void {
    this.newConfig.set({ key: '', value: '', description: '' });
    this.showCreateModal.set(true);
  }

  openEditModal(config: SystemConfig): void {
    this.currentConfig.set(config);
    this.editConfig.set({
      key: config.key,
      value: config.value,
      description: config.description
    });
    this.showEditModal.set(true);
  }

  openDeleteModal(config: SystemConfig): void {
    this.configToDelete.set(config);
    this.showDeleteModal.set(true);
  }

  createConfig(): void {
    const config = this.newConfig();
    if (!config.key || !config.value) {
      this.errorMessage.set('La clave y el valor son obligatorios');
      this.showErrorModal.set(true);
      return;
    }

    this.systemConfigService.create(config).subscribe({
      next: () => {
        this.showCreateModal.set(false);
        this.loadConfigs();
        this.showSuccessModal.set(true);
      },
      error: (error) => {
        this.errorMessage.set(error.error?.error || 'Error al crear la configuración');
        this.showErrorModal.set(true);
      }
    });
  }

  updateConfig(): void {
    const config = this.currentConfig();
    if (!config) return;

    this.systemConfigService.update(config.id, this.editConfig()).subscribe({
      next: () => {
        this.showEditModal.set(false);
        this.loadConfigs();
        this.showSuccessModal.set(true);
      },
      error: (error) => {
        this.errorMessage.set(error.error?.error || 'Error al actualizar la configuración');
        this.showErrorModal.set(true);
      }
    });
  }

  deleteConfig(): void {
    const config = this.configToDelete();
    if (!config) return;

    this.systemConfigService.delete(config.id).subscribe({
      next: () => {
        this.showDeleteModal.set(false);
        this.loadConfigs();
        this.showSuccessModal.set(true);
      },
      error: (error) => {
        this.errorMessage.set(error.error?.error || 'Error al eliminar la configuración');
        this.showErrorModal.set(true);
      }
    });
  }

  resetForm(): void {
    this.newConfig.set({ key: '', value: '', description: '' });
    this.editConfig.set({});
  }

  toggleSort(column: string): void {
    const options = this.filterOptions();
    if (options.sortBy === column) {
      options.sortOrder = options.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      options.sortBy = column;
      options.sortOrder = 'asc';
    }
    this.filterOptions.set({...options});
    this.applyFilters();
  }

  getSortIcon(column: string): string {
    const options = this.filterOptions();
    if (options.sortBy !== column) {
      return 'M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4';
    }
    return options.sortOrder === 'asc' 
      ? 'M5 15l7-7 7 7'
      : 'M19 9l-7 7-7-7';
  }
}