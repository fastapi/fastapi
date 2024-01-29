import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Layout from './pages/Layout';
import Login from './pages/auth/Login';
import RecoverPassword from './pages/auth/RecoverPassword';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/recover-password" element={<RecoverPassword />} />
        <Route element={<Layout />}>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
