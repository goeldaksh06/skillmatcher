import React from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Container,
} from '@mui/material';
import { Assessment, People, TrendingUp } from '@mui/icons-material';

const Home: React.FC = () => {
  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Box
        textAlign="center"
        py={8}
        sx={{
          background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
          borderRadius: 2,
          color: 'white',
          mb: 6,
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          Skill Matcher
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          AI-Powered Skill Assessment Platform
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
          Revolutionize your hiring process with intelligent skill assessments. 
          Our AI analyzes resumes, generates relevant questions, and provides 
          instant feedback to help you find the perfect candidates.
        </Typography>
        <Button
          variant="contained"
          size="large"
          sx={{ 
            bgcolor: 'white', 
            color: 'primary.main',
            '&:hover': { bgcolor: 'grey.100' }
          }}
        >
          Get Started
        </Button>
      </Box>

      {/* Features Section */}
      <Typography variant="h4" component="h2" textAlign="center" gutterBottom mb={4}>
        Key Features
      </Typography>
      
      <Grid container spacing={4} mb={6}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', p: 4 }}>
              <Assessment sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" component="h3" gutterBottom>
                AI-Powered Assessments
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Our AI generates relevant questions based on required skills and 
                provides intelligent grading with detailed feedback.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', p: 4 }}>
              <People sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" component="h3" gutterBottom>
                Smart Resume Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Automatically parse and analyze resumes to match candidate skills 
                with job requirements using advanced text processing.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ textAlign: 'center', p: 4 }}>
              <TrendingUp sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" component="h3" gutterBottom>
                Real-time Analytics
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Track assessment performance, identify skill gaps, and make 
                data-driven hiring decisions with comprehensive analytics.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* How it Works */}
      <Box textAlign="center" py={6}>
        <Typography variant="h4" component="h2" gutterBottom mb={4}>
          How It Works
        </Typography>
        
        <Grid container spacing={4}>
          <Grid item xs={12} md={3}>
            <Box>
              <Typography variant="h6" color="primary" gutterBottom>
                1. Create Assessment
              </Typography>
              <Typography variant="body2">
                Recruiters define required skills and set eligibility thresholds
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <Box>
              <Typography variant="h6" color="primary" gutterBottom>
                2. Upload Resume
              </Typography>
              <Typography variant="body2">
                Candidates upload their resume or paste resume text
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <Box>
              <Typography variant="h6" color="primary" gutterBottom>
                3. AI Assessment
              </Typography>
              <Typography variant="body2">
                AI generates personalized questions and grades responses
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <Box>
              <Typography variant="h6" color="primary" gutterBottom>
                4. Get Results
              </Typography>
              <Typography variant="body2">
                Instant feedback with scores and improvement recommendations
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Home;