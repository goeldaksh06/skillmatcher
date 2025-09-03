// MUI Components
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

// Redux
import { Provider } from 'react-redux';
import { store } from './store';

// Routing
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Notifications
import { SnackbarProvider } from 'notistack';

// Theme
import theme from './theme';

// Components
import Navbar from './components/layout/Navbar';

const App = () => {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <SnackbarProvider maxSnack={3}>
          <Router>
            <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
              <Navbar />
              <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <Routes>
                  {/* Add your routes here */}
                  <Route path="/" element={<div>Welcome to Skill Matcher</div>} />
                </Routes>
              </Box>
            </Box>
          </Router>
        </SnackbarProvider>
      </ThemeProvider>
    </Provider>
  );
};

export default App;
