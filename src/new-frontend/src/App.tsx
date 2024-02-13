import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import { ChakraProvider, extendTheme } from '@chakra-ui/react';

import Layout from './pages/Layout';
import NotFound from './pages/NotFound';
import Login from './pages/auth/Login';
import RecoverPassword from './pages/auth/RecoverPassword';
import Admin from './pages/main/Admin';
import Dashboard from './pages/main/Dashboard';
import Items from './pages/main/Items';
import Profile from './pages/main/Profile';

// Theme
const theme = extendTheme({
  colors: {
    ui: {
      main: "#009688",
      secondary: "#EDF2F7",
      success: '#48BB78',
      danger: '#E53E3E',
    }
  },
  components: {
    Tabs: {
      variants: {
        enclosed: {
          tab: {
            _selected: {
              color: 'ui.main',
            },
          },
        },
      },
    },
  },
});

function App() {
  return (
    <>
      <Router>
        <ChakraProvider theme={theme}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/recover-password" element={<RecoverPassword />} />
            <Route element={<Layout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/settings" element={<Profile />} />
              <Route path="/items" element={<Items />} />
              <Route path="/admin" element={<Admin />} />
            </Route>
            <Route path="*" element={<NotFound />} />
          </Routes>
        </ ChakraProvider>
      </Router>
    </>
  )
}

export default App
