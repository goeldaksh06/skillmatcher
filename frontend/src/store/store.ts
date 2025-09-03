import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import assessmentSlice from './slices/assessmentSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    assessment: assessmentSlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;