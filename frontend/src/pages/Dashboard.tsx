import React, { useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Alert,
} from '@mui/material';
import { Add, Assessment, People } from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../store/store';
import { fetchAssessments } from '../store/slices/assessmentSlice';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const { assessments, loading, error } = useSelector((state: RootState) => state.assessment);

  useEffect(() => {
    if (user?.role === 'recruiter') {
      dispatch(fetchAssessments() as any);
    }
  }, [dispatch, user]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'default';
      case 'active': return 'primary';
      case 'completed': return 'success';
      case 'rejected': return 'error';
      default: return 'default';
    }
  };

  if (user?.role === 'recruiter') {
    return (
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
          <Typography variant="h4" component="h1">
            Recruiter Dashboard
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => navigate('/create-assessment')}
          >
            Create Assessment
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {assessments.map((assessment) => (
            <Grid item xs={12} md={6} lg={4} key={assessment.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {assessment.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {assessment.description || 'No description'}
                  </Typography>
                  
                  <Box mt={2} mb={1}>
                    <Typography variant="subtitle2" gutterBottom>
                      Required Skills:
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={0.5}>
                      {assessment.required_skills.map((skill, index) => (
                        <Chip key={index} label={skill} size="small" />
                      ))}
                    </Box>
                  </Box>
                  
                  <Box mt={2}>
                    <Chip
                      label={assessment.status}
                      color={getStatusColor(assessment.status) as any}
                      size="small"
                    />
                  </Box>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    startIcon={<Assessment />}
                    onClick={() => navigate(`/assessment/${assessment.id}`)}
                  >
                    View Details
                  </Button>
                  <Button
                    size="small"
                    startIcon={<People />}
                    onClick={() => {/* TODO: View candidates */}}
                  >
                    Candidates
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>

        {assessments.length === 0 && !loading && (
          <Box textAlign="center" mt={4}>
            <Typography variant="h6" color="text.secondary">
              No assessments created yet
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => navigate('/create-assessment')}
              sx={{ mt: 2 }}
            >
              Create Your First Assessment
            </Button>
          </Box>
        )}
      </Box>
    );
  }

  // Candidate dashboard
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Candidate Dashboard
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        Welcome! To take an assessment, you'll need the assessment link from your recruiter.
      </Alert>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            How to Take an Assessment:
          </Typography>
          <Typography variant="body1" paragraph>
            1. Receive an assessment link from your recruiter
          </Typography>
          <Typography variant="body1" paragraph>
            2. Click the link to view assessment details
          </Typography>
          <Typography variant="body1" paragraph>
            3. Upload your resume or paste resume text
          </Typography>
          <Typography variant="body1" paragraph>
            4. If eligible, answer the AI-generated questions
          </Typography>
          <Typography variant="body1">
            5. View your results and feedback
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;