export interface InvitationResponse {
  id: number;
  test_id: number;
  test_title: string;
  invited_by: number;
  inviter_name: string;
  message: string;
  token: string;
  is_used: boolean;
  is_guest: boolean;
  guest_user_id?: number;
  guest_name?: string;
  expires_at: string;
  created_at: string;
  status: 'active' | 'used' | 'expired';
  invitation_url: string;
}

export interface InvitationsFilter {
  page: number;
  page_size: number;
  sort_by: string;
  sort_order: 'asc' | 'desc';
  
  // Filtros
  search?: string;
  test_id?: number;
  invited_by?: number;
  is_used?: boolean;
  is_guest?: boolean;
  status?: string;
  
  // Fechas
  start_date?: string;
  end_date?: string;
}

export interface InvitationsResponse {
  invitations: InvitationResponse[];
  pagination: {
    page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
  };
  filters_applied: InvitationsFilter;
  available_filters: any;
}
