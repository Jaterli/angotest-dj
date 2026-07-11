export interface Answer {
  id?: number;
  answer_text: string;
  is_correct: boolean;
}

export interface Question {
  id?: number;
  question_text: string;
  answers: Answer[];
}

export interface Test {
  id: number;
  title: string;
  description?: string;
  main_topic: string;
  sub_topic: string;
  specific_topic: string;
  created_by: number;
  level: string;
  is_active: boolean;
  created_at: string; 
  updated_at: string;   
  questions?: Question[];
  total_questions?: number;
  results?: Result[];
}

export interface TestsResponse {
  tests: Test[];
}

export interface TestWithCount extends Test {
  question_count: number;
}

export interface TestFiltersApplied {
    main_topic: string | null;
    sub_topic: string | null;
    level?: string;
    is_active?: boolean;
    page: number;
    page_size: number;
    search?: string;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
}

export interface TestAvailableFilters {
    main_topics: string[]; 
    sub_topics: string[];
    levels: string[];
    is_active?: boolean;
}

export interface TestsListResponse {
  data: {
    tests: TestWithCount[];
  }
  pagination: TestsPagination;
  available_filters: TestAvailableFilters;
  stats: {
    total_filtered_tests: number;
    total_tests: number;
  }
}

interface TestsPagination {
  total_tests: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  has_more: boolean;
}

export interface Result {
  id: number;
  correct_answers: number;
  wrong_answers: number;
  total_questions: number;
  score_percent: number;
  created_at: string;
  user_id: number;
  test_id: number;
  test_title: string;
  test_category: string;
  test_description: string;
  test_level: string;
  time_taken: number;
}

// export interface ResultResponse {
//   results: Result[];
// }

// export interface NotCompletedTestsResponse {
//   tests: Test[];
//   not_completed_count: number;
//   message: string;
// }

export interface AnswerSubmit {
  question_id: number;
  answer_id: number;
}

export interface SaveResultInput {
  test_id: number;
  answers: Record<string, number>;
  time_taken: number;
  status: 'in_progress' | 'completed' | 'expired';
}

export interface ResumeTestResponse {
  test: Test;
  answers: AnswerSubmit[];
  time_elapsed: number;
  progress: number;
  is_resuming: boolean;
  result_id?: number;
}


// In Progress Tests
export interface InProgressTestsFilter {
  page?: number;
  page_size?: number;
  main_topic?: string;
  level?: string;
  ordering?: string;
}

export interface InProgressTestsResponse {
  in_progress_tests: any[];
  count: number;
}


// Not Started Tests
export interface NotStartedTestsFilter {
  page?: number;
  page_size?: number;
  main_topic?: string;
  level?: string;
  ordering?: string;
}

export interface NotStartedTestsResponse {
  data: {
    tests: Test[];
    main_topics: string[];
  }
  pagination: TestsPagination;
  stats: NotStartedTestsStats;
}

 export interface NotStartedTestsStats {
    total_by_level: Record<string, number>;  
    total_filtered: number;
    total_unfiltered: number;
 }


// CompletedTests
export interface CompletedTestsFilter {
  page?: number;
  page_size?: number;
  main_topic?: string;
  level?: string;
  ordering?: string;
  search?: string;
  from_date?: string;
  to_date?: string;
}

export interface CompletedTest {
  id: number;
  user_id: number;
  test_id: number;
  correct_answers: number;
  wrong_answers: number;
  time_taken: number;
  status: string;
  started_at: string;
  updated_at: string;
  
  // Datos del test
  test_title: string;
  test_description?: string;
  test_main_topic: string;
  test_sub_topic: string;
  test_specific_topic: string;
  test_level: string;
  test_created_at: string;
  
  // Estadísticas
  attempt_position: number;
  total_attempts: number;
  total_questions: number;
  score_percent: number;
  score_rounded: number;
  accuracy: number;
  completion_time?: string;
}


export interface CompletedTestsStats {
  average_score: number;
  total_filtered: number;
  total_unfiltered: number;
  total_time_spent: number;
  total_filtered_tests: number;
  total_questions_answered: number;
}

export interface CompletedTestsResponse {
  data: {
    tests: CompletedTest[];
    main_topics: string[];
  };
  pagination: TestsPagination;
  stats: CompletedTestsStats;
  //levels: string[];  
}



// Modelos para tests en progreso
export interface InProgressTestsFilter {
  page?: number;
  page_size?: number;
  main_topic?: string;
  level?: string;
  sort_by?: 'test_title' | 'progress' | 'test_created_at' | 'result_updated_at' | 'result_started_at' | 'result_time_taken' | 'test_level' | 'remaining_time' | 'remaining_count';
  sort_order?: 'asc' | 'desc';
}

export interface InProgressTest {
  id: number; 
  user_id: number;
  test_id: number;
  time_taken: number;
  status: string;
  answers?: string;
  started_at: string;
  updated_at: string;
  
  // Datos del test
  test_title: string;
  test_description?: string;
  test_main_topic: string;
  test_sub_topic: string;
  test_specific_topic: string;
  test_level: string;
  test_created_at: string;
  
  // Estadísticas
  total_questions: number;
  progress: number;
  answered_count: number;
  remaining_count: number;
  time_spent?: string;
  last_activity?: string;
}

export interface InProgressTestResponse {
  data: {
    tests: InProgressTest[];
    main_topics: string[];
  };
  pagination: TestsPagination;
  stats: InProgressTestsStats;
}

export interface InProgressTestsStats {
  total_filtered: number;
  total_unfiltered: number;
  average_progress?: number;
  total_questions_answered?: number;
  total_time_spent?: number;
  total_by_level: Record<string, number>;  
}


// Estructura para la jerarquía de temas
export interface TopicHierarchy {
  id?: number;
  main_topic: string;
  sub_topic: string;
  specific_topic: string;
  is_predefined?: boolean;
}

export interface TopicStructure {
  [mainTopic: string]: {
    [subTopic: string]: string[];
  };
}


// Interfaz para el formulario de edición
export interface TestEditFormData {
  title: string;
  description?: string;
  main_topic: string;
  sub_topic: string;
  specific_topic: string;
  level: string;
  created_at: string;
  questions: QuestionEditFormData[];
}

export interface QuestionEditFormData {
  id?: number;
  question_text: string;
  answers: AnswerEditFormData[];
}

export interface AnswerEditFormData {
  id?: number;
  answer_text: string;
  is_correct: boolean;
}

export interface QuestionWithAnswers {
  id: number;
  question_text: string;
  answers: AnswerResponse[];
}

export interface AnswerResponse {
  id: number;
  answer_text: string;
}


// Nueva interfaz para siguiente pregunta
export interface NextQuestionResponse {
  question: QuestionWithAnswers;
  question_number: number;
  total_questions: number;
  is_completed: boolean;  
  answered_count: number;
  progress: number;
}

export interface SingleQuestionResponse {
  question: QuestionWithAnswers;
  question_number: number;
  total_questions: number;
  has_next: boolean;
  is_last: boolean;
}

export interface QuestionWithAnswers {
  id: number;
  question_text: string;
  answers: AnswerResponse[];
}

export interface AnswerResponse {
  id: number;
  answer_text: string;
}


// Otros
export interface TestsWithStatusResponse {
  tests: TestWithStatus[];
  total_tests: number;
  completed_count: number;
  in_progress_count: number;
  not_started_count: number;
  message: string;
}

export interface TestWithStatus extends Test {
  status: 'not_started' | 'in_progress' | 'completed';
  completed_at?: string; 
  last_score?: number;
  correct_answers: number;
  wrong_answers: number;
  total_questions: number;
  time_taken: number;
  progress?: number;
  question_count?: number; 
}
