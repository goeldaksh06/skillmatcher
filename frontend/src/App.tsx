import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Container, Typography, Box } from '@mui/material';
import Navbar from './components/layout/Navbar';
import Home from './pages/Home';

function App() {
  return (
    <div className="App">
      <Navbar />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="*" element={
            <Box textAlign="center" mt={4}>
              <Typography variant="h4">Page Not Found</Typography>
              <Typography variant="body1" mt={2}>
                The page you're looking for doesn't exist.
              </Typography>
            </Box>
          } />
        </Routes>
      </Container>
    </div>
  );
}

export default App;