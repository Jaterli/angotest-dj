export interface UserResultDetail {
  result_id: number;
  test_id: number;
  title: string;
  description: string;
  main_topic: string;
  sub_topic: string;
  specific_topic: string;
  level: string;
  created_at: string;
  total_questions: number;
  correct_answers: number;
  wrong_answers: number;
  score: number;
  time_taken: number;
  status: 'completed' | 'in_progress' | 'abandoned';
  started_at: string;
  updated_at: string;
  answered_count: number;
}

export interface UserResultsFilters {
  page?: number;
  page_size?: number;
  status?: 'all' | 'completed' | 'in_progress';
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  search?: string;
  level?: string;
  main_topic?: string;
  sub_topic?: string;
  from_date?: string;
  to_date?: string;
}

export interface UserResultsResponse {
  results: UserResultDetail[];
  total_results: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  has_more: boolean;
  
  stats: {
    total_tests: number;
    completed_tests: number;
    in_progress_tests: number;
    average_score: number;
    total_time_spent: number;
    total_questions_answered: number;
    total_correct_answers: number;
  };
  
  filters: {
    status?: string;
    level?: string;
    main_topic?: string;
    sub_topic?: string;
    from_date?: string;
    to_date?: string;
    search?: string;
    sort_by: string;
    sort_order: string;
  };
}


export interface UserResultsData {
  user: UserDetail;
  data: UserResultsResponse;
}

export interface UserDetail {
    id: number;
    username: string;
    role: string;
    email: string;
    first_name?: string;
    last_name?: string;
}

export interface TestDetail {
  created_at: string;
  description: string;
  id: number;
  level: string;
  main_topic: string;
  specific_topic: string;
  sub_topic: string;
  title: string;
}

export interface ResultInfo {
  id: number;
  user_id: number;
  test_id: number;
  correct_answers: number;
  wrong_answers: number;
  time_taken: number;
  status: string;
  answered_questions: any;
  started_at: string;
  updated_at: string;
}

export interface ResultDetailsResponse {
  result: ResultInfo;
  user: UserDetail;
  test: TestDetail;
  questions: {
    id: number;
    question_text: string;
    answers: {
      id: number;
      answer_text: string;
      is_correct: boolean;
    }[];
  }[];

  total_questions: number;
  score_details: {
    correct: number;
    wrong: number;
    score_percentage: number;
  };
}