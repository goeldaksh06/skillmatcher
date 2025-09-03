import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  
  register: (userData: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    role?: string;
  }) => api.post('/api/auth/register', userData),
  
  getProfile: () => api.get('/api/auth/profile'),
  
  updateProfile: (userData: { first_name?: string; last_name?: string }) =>
    api.put('/api/auth/profile', userData),
};

// Assessment API
export const assessmentAPI = {
  // For recruiters
  createAssessment: (data: {
    title: string;
    description?: string;
    required_skills: string;
    threshold_percentage?: number;
  }) => api.post('/api/recruiter/assessments', data),
  
  getAssessments: () => api.get('/api/recruiter/assessments'),
  
  getAssessmentDetails: (assessmentId: number) =>
    api.get(`/api/recruiter/assessments/${assessmentId}`),
  
  getAssessmentCandidates: (assessmentId: number) =>
    api.get(`/api/recruiter/assessments/${assessmentId}/candidates`),
  
  // For candidates
  getPublicAssessment: (assessmentId: number) =>
    api.get(`/api/assessment/public/${assessmentId}`),
  
  startAssessment: (assessmentId: number, resumeText: string) =>
    api.post(`/api/assessment/start/${assessmentId}`, { resume_text: resumeText }),
  
  uploadResumeFile: (assessmentId: number, file: File) => {
    const formData = new FormData();
    formData.append('resume_file', file);
    return api.post(`/api/assessment/start/${assessmentId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  getProgress: (assessmentId: number) =>
    api.get(`/api/assessment/progress/${assessmentId}`),
  
  submitAnswer: (questionId: number, answerText: string, timeSpent?: number) =>
    api.post(`/api/assessment/question/${questionId}/answer`, {
      answer_text: answerText,
      time_spent_seconds: timeSpent,
    }),
  
  completeAssessment: (assessmentId: number) =>
    api.post(`/api/assessment/complete/${assessmentId}`),
};

export default api;