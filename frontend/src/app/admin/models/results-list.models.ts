// ====== Modelos para Administración de Resultados ======

export interface AdminResult {
  id: number;
  user_id: number;
  test_id: number;
  correct_answers: number;
  wrong_answers: number;
  total_questions: number;
  score: number;
  time_taken: number;
  status: 'in_progress' | 'completed' | 'expired';
  answers?: string;
  started_at: string;
  updated_at: string;
  
  // Datos del usuario
  user_username: string;
  user_email: string;
  user_first_name?: string;
  user_last_name?: string;
  user_role: string;
  
  // Datos del test
  test_title: string;
  test_description?: string;
  test_main_topic: string;
  test_sub_topic: string;
  test_specific_topic: string;
  test_level: string;
  test_created_by: number;
  test_created_at: string;
  test_is_active: boolean;
}

// export interface AdminResultsFilter {

//   // Filtros por usuario
//   user_id?: number;
//   user_role?: string;
//   user_email?: string;
//   user_username?: string;

//   // Filtros por test
//   test_id?: number;
//   test_title?: string;
//   test_main_topic?: string;
//   test_sub_topic?: string;
//   test_level?: string;
//   test_created_by?: number;
//   test_is_active?: boolean;

//   // Filtros por resultado
//   status?: string;
//   min_score?: number;
//   max_score?: number;
    
//   // Fechas
//   start_date?: string;
//   end_date?: string;

//   page?: number;
//   page_size?: number;
//   main_topic?: string;
//   level?: string;
//   ordering?: string;
//   sort_order?: 'asc' | 'desc';
//   search?: string;
//   from_date?: string;
//   to_date?: string;
// }

export interface AdminResultsFilter {
  // Filtros por usuario
  user_role?: string;

  // Filtros por test
  test_main_topic?: string;
  test_sub_topic?: string;
  test_level?: string;
  test_created_by?: number;
  test_is_active?: boolean;

  // Filtros por resultado
  status?: string;
  started_at?: string;
  updated_at?: string;
  min_score?: number;
  max_score?: number;

  page: number;
  page_size: number;
  search?: string;
  ordering: string;
  order_dir?: 'asc' | 'desc';
}


export interface AdminResultsResponse {
  data: AdminResult[];
  stats: ResultsStats;
  pagination: ResultsPagination;
  available_filters: ResultsAvailableFilters
}

export interface ResultsStats {
  average_score: number;
  total_filtered: number;
  total_unfiltered: number;
  total_time_spent: number;
}

export interface ResultsAvailableFilters {
    main_topics: string[]; 
    levels?: string[];
    statuses?: string[];
    roles: string[];
}

interface ResultsPagination {
  total_filtered: number;
  total_unfiltered: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  has_more: boolean;
}