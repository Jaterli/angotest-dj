export interface UserStats {
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
export interface UsersStatsFilters {
  page_size?: number;
  page?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  role?: string;
  search?: string;
}

export interface Pagination {
  page: number;
  page_size: number;
  total_filtered: number;
  total_pages: number;
}

export interface UserStatsFullResponse {
  data: UserStats[];
  sort_fields: string[];
  pagination: Pagination;
  stats: {
    total_users: number;
    total_filtered_users: number;
  };    
}