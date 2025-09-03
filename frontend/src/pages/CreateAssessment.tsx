import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Slider,
} from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../store/store';
import { createAssessment, clearError } from '../store/slices/assessmentSlice';

const CreateAssessment: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state: RootState) => state.assessment);
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    required_skills: '',
    threshold_percentage: 70,
  });

  // Redirect if not recruiter
  React.useEffect(() => {
    if (user && user.role !== 'recruiter') {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleThresholdChange = (_: Event, newValue: number | number[]) => {
    setFormData({
      ...formData,
      threshold_percentage: newValue as number,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(clearError());
    
    const result = await dispatch(createAssessment(formData) as any);
    if (createAssessment.fulfilled.match(result)) {
      navigate('/dashboard');
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Create New Assessment
      </Typography>

      <Paper elevation={3} sx={{ p: 4, maxWidth: 600 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Assessment Title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            margin="normal"
            required
            placeholder="e.g., Senior Python Developer Assessment"
          />

          <TextField
            fullWidth
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            margin="normal"
            multiline
            rows={3}
            placeholder="Brief description of the role and assessment"
          />

          <TextField
            fullWidth
            label="Required Skills"
            name="required_skills"
            value={formData.required_skills}
            onChange={handleChange}
            margin="normal"
            required
            placeholder="Python, SQL, Flask, REST API, Machine Learning"
            helperText="Enter skills separated by commas"
          />

          <Box mt={3} mb={2}>
            <Typography gutterBottom>
              Minimum Skill Match Threshold: {formData.threshold_percentage}%
            </Typography>
            <Slider
              value={formData.threshold_percentage}
              onChange={handleThresholdChange}
              min={50}
              max={100}
              step={5}
              marks={[
                { value: 50, label: '50%' },
                { value: 70, label: '70%' },
                { value: 90, label: '90%' },
                { value: 100, label: '100%' },
              ]}
              valueLabelDisplay="auto"
            />
            <Typography variant="body2" color="text.secondary">
              Candidates must match at least this percentage of required skills to be eligible
            </Typography>
          </Box>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Create Assessment'}
          </Button>

          <Button
            fullWidth
            variant="outlined"
            sx={{ mt: 1 }}
            onClick={() => navigate('/dashboard')}
          >
            Cancel
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default CreateAssessment;