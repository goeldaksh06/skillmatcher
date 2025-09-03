import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { assessmentAPI } from '../../services/api';

export interface Assessment {
  id: number;
  title: string;
  description: string;
  required_skills: string[];
  threshold_percentage: number;
  recruiter_id: number;
  candidate_id?: number;
  status: string;
  resume_filename?: string;
  skill_matches?: Record<string, boolean>;
  eligibility_data?: any;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  expires_at?: string;
}

export interface Question {
  id: number;
  assessment_id: number;
  skill: string;
  question_text: string;
  question_type: string;
  options?: any;
  difficulty: string;
  order_index: number;
  created_at: string;
}

export interface AssessmentProgress {
  assessment: Assessment;
  total_questions: number;
  answered_questions: number;
  current_question?: Question;
  progress_percentage: number;
}

interface AssessmentState {
  assessments: Assessment[];
  currentAssessment: Assessment | null;
  currentProgress: AssessmentProgress | null;
  loading: boolean;
  error: string | null;
}

const initialState: AssessmentState = {
  assessments: [],
  currentAssessment: null,
  currentProgress: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchAssessments = createAsyncThunk(
  'assessment/fetchAssessments',
  async (_, { rejectWithValue }) => {
    try {
      const response = await assessmentAPI.getAssessments();
      return response.data.assessments;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error || 'Failed to fetch assessments');
    }
  }
);

export const createAssessment = createAsyncThunk(
  'assessment/create',
  async (assessmentData: {
    title: string;
    description?: string;
    required_skills: string;
    threshold_percentage?: number;
  }, { rejectWithValue }) => {
    try {
      const response = await assessmentAPI.createAssessment(assessmentData);
      return response.data.assessment;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error || 'Failed to create assessment');
    }
  }
);

export const startAssessment = createAsyncThunk(
  'assessment/start',
  async ({ assessmentId, resumeText }: { assessmentId: number; resumeText: string }, { rejectWithValue }) => {
    try {
      const response = await assessmentAPI.startAssessment(assessmentId, resumeText);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error || 'Failed to start assessment');
    }
  }
);

export const fetchProgress = createAsyncThunk(
  'assessment/fetchProgress',
  async (assessmentId: number, { rejectWithValue }) => {
    try {
      const response = await assessmentAPI.getProgress(assessmentId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error || 'Failed to fetch progress');
    }
  }
);

export const submitAnswer = createAsyncThunk(
  'assessment/submitAnswer',
  async ({ questionId, answerText, timeSpent }: {
    questionId: number;
    answerText: string;
    timeSpent?: number;
  }, { rejectWithValue }) => {
    try {
      const response = await assessmentAPI.submitAnswer(questionId, answerText, timeSpent);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.error || 'Failed to submit answer');
    }
  }
);

const assessmentSlice = createSlice({
  name: 'assessment',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentAssessment: (state) => {
      state.currentAssessment = null;
      state.currentProgress = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch assessments
    builder
      .addCase(fetchAssessments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAssessments.fulfilled, (state, action) => {
        state.loading = false;
        state.assessments = action.payload;
      })
      .addCase(fetchAssessments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Create assessment
    builder
      .addCase(createAssessment.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createAssessment.fulfilled, (state, action) => {
        state.loading = false;
        state.assessments.push(action.payload);
      })
      .addCase(createAssessment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Start assessment
    builder
      .addCase(startAssessment.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(startAssessment.fulfilled, (state, action) => {
        state.loading = false;
        state.currentAssessment = action.payload.assessment;
      })
      .addCase(startAssessment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Fetch progress
    builder
      .addCase(fetchProgress.fulfilled, (state, action) => {
        state.currentProgress = action.payload;
      });

    // Submit answer
    builder
      .addCase(submitAnswer.pending, (state) => {
        state.loading = true;
      })
      .addCase(submitAnswer.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(submitAnswer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearCurrentAssessment } = assessmentSlice.actions;
export default assessmentSlice.reducer;