import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from './store/store';
import Navbar from './components/layout/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AssessmentView from './pages/AssessmentView';
import CreateAssessment from './pages/CreateAssessment';
import PublicAssessment from './pages/PublicAssessment';

function App() {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);

  return (
    <div className="App">
      <Navbar />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />} />
          <Route path="/assessment/public/:id" element={<PublicAssessment />} />
          
          {/* Protected routes */}
          <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/assessment/:id" element={isAuthenticated ? <AssessmentView /> : <Navigate to="/login" />} />
          <Route path="/create-assessment" element={isAuthenticated ? <CreateAssessment /> : <Navigate to="/login" />} />
          
          {/* Default redirect */}
          <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App;