export interface UserList {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  address: string;
  country: string;
  birth_date: string;
  role: string;
  registered_at: string;
  
  // Estadísticas
  tests_completed: number;
  tests_in_progress: number;
  tests_not_started: number;
  average_score: number;
  total_tests_taken: number;
}

// Interfaz para los filtros de usuarios
export interface UsersListFilters {
  page_size: number;
  page: number;
  ordering: string;
  order_dir: 'asc' | 'desc';
  role?: string;
  search?: string;
}

export interface Pagination {
  page_size: number;
  current_page: number;
  total_filtered: number;
  total_pages: number;
  has_more: boolean;
}

export interface UserListStats {
  total_unfiltered: number;
  total_filtered: number;
}

export interface UserListResponse {
  data: UserList[];
  sort_fields: string[];
  pagination: Pagination;
  stats: UserListStats;
}