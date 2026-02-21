export interface UserQuota {
  id: number;
  user_id: number;
  username?: string;
  user_email?: string;
  month_year: string;
  max_requests: number;
  used_requests: number;
  created_at: string;
  updated_at: string;
}

export interface QuotaFilter {
  page: number;
  page_size: number;
  sort_by: string;
  sort_order: 'asc' | 'desc';
  
  // Filtros
  search?: string;
  user_id?: number;
  month_year?: string;
  min_remaining?: number;
  max_usage?: number;
  min_requests?: number;
  max_requests?: number;
  
  // Filtros de fecha
  start_date?: string;
  end_date?: string;
  
  // Estado de cuota
  quota_status?: 'normal' | 'warning' | 'critical' | 'exceeded';
}

export interface QuotaResponse {
  quotas: UserQuota[];
  pagination: {
    total_items: number;
    total_pages: number;
    page: number;
    page_size: number;
  };
}

export interface CreateQuotaInput {
  user_id: number;
  month_year: string;
  max_requests: number;
}

export interface UpdateQuotaInput {
  max_requests?: number;
  used_requests?: number;
}

export interface QuotaSummary {
  user_id: number;
  username: string;
  email: string;
  current_month_quota: UserQuota | null;
  average_monthly_usage: number;
  total_requests_year: number;
  months_with_quota: number;
}