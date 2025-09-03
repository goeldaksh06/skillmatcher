import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Chip,
  Alert,
  TextField,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import { CheckCircle, Upload, Login as LoginIcon } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/store';
import { startAssessment } from '../store/slices/assessmentSlice';
import { assessmentAPI } from '../services/api';

const PublicAssessment: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  const { loading, error } = useSelector((state: RootState) => state.assessment);
  
  const [assessment, setAssessment] = useState<any>(null);
  const [resumeText, setResumeText] = useState('');
  const [loadingAssessment, setLoadingAssessment] = useState(true);
  const [assessmentError, setAssessmentError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAssessment = async () => {
      try {
        const response = await assessmentAPI.getPublicAssessment(Number(id));
        setAssessment(response.data.assessment);
      } catch (error: any) {
        setAssessmentError(error.response?.data?.error || 'Assessment not found');
      } finally {
        setLoadingAssessment(false);
      }
    };

    if (id) {
      fetchAssessment();
    }
  }, [id]);

  const handleStartAssessment = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (!resumeText.trim()) {
      return;
    }

    const result = await dispatch(startAssessment({
      assessmentId: Number(id),
      resumeText
    }) as any);

    if (startAssessment.fulfilled.match(result)) {
      if (result.payload.eligible) {
        navigate(`/assessment/${id}`);
      }
    }
  };

  if (loadingAssessment) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (assessmentError) {
    return (
      <Alert severity="error">
        {assessmentError}
      </Alert>
    );
  }

  if (!assessment) {
    return (
      <Alert severity="error">
        Assessment not found
      </Alert>
    );
  }

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {assessment.title}
        </Typography>
        
        {assessment.description && (
          <Typography variant="body1" paragraph>
            {assessment.description}
          </Typography>
        )}

        <Box mb={3}>
          <Typography variant="h6" gutterBottom>
            Required Skills:
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {assessment.required_skills.map((skill: string, index: number) => (
              <Chip key={index} label={skill} color="primary" />
            ))}
          </Box>
        </Box>

        <Alert severity="info" sx={{ mb: 3 }}>
          You need to match at least {assessment.threshold_percentage}% of the required skills to be eligible for this assessment.
        </Alert>

        <Typography variant="h6" gutterBottom>
          Assessment Process:
        </Typography>
        <List dense>
          <ListItem>
            <ListItemIcon>
              <CheckCircle color="primary" />
            </ListItemIcon>
            <ListItemText primary="Upload your resume or paste resume text" />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircle color="primary" />
            </ListItemIcon>
            <ListItemText primary="AI will verify your skills match the requirements" />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircle color="primary" />
            </ListItemIcon>
            <ListItemText primary="Answer AI-generated questions about your skills" />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <CheckCircle color="primary" />
            </ListItemIcon>
            <ListItemText primary="Receive instant feedback and results" />
          </ListItem>
        </List>

        {!isAuthenticated ? (
          <Box mt={4}>
            <Alert severity="warning" sx={{ mb: 2 }}>
              You need to login or register to take this assessment.
            </Alert>
            <Button
              variant="contained"
              startIcon={<LoginIcon />}
              onClick={() => navigate('/login')}
              fullWidth
            >
              Login to Continue
            </Button>
          </Box>
        ) : (
          <Box mt={4}>
            <Typography variant="h6" gutterBottom>
              Upload Your Resume:
            </Typography>
            
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <TextField
              fullWidth
              multiline
              rows={8}
              label="Paste your resume text here"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Copy and paste your resume content here..."
              sx={{ mb: 2 }}
            />

            <Button
              variant="contained"
              startIcon={<Upload />}
              onClick={handleStartAssessment}
              disabled={!resumeText.trim() || loading}
              fullWidth
            >
              {loading ? <CircularProgress size={24} /> : 'Start Assessment'}
            </Button>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default PublicAssessment;