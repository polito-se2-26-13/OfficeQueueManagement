import { BrowserRouter, Routes, Route } from 'react-router';
import './App.css'

import Home from './pages/Home'
import Customer from './pages/Customer'
import Officer from './pages/Officer'
import Admin from './pages/Admin'
import Ticket from './pages/Ticket'

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/customer" element={<Customer />} />
          <Route path="/officer" element={<Officer />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/ticket/:code" element={<Ticket />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
