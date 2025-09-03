export interface User {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  role: 'candidate' | 'recruiter' | 'admin';
  createdAt: string;
  updatedAt: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: 'candidate' | 'recruiter';
}
