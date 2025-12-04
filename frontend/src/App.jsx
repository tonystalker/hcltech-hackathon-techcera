import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ProviderView from './pages/ProviderView'
import PublicInfo from './pages/PublicInfo'
import Profile from './pages/Profile'
import GoalTracker from './pages/GoalTracker'
import ProtectedRoute from './components/ProtectedRoute'

export default function App(){
  return (
    <div className="app-root">
      <Header />
      <main className="container">
        <Routes>
          <Route path="/login" element={<Login/>} />
          <Route path="/register" element={<Register/>} />

          <Route path="/" element={<ProtectedRoute><Dashboard/></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile/></ProtectedRoute>} />
          <Route path="/goals" element={<ProtectedRoute><GoalTracker/></ProtectedRoute>} />
          <Route path="/provider" element={<ProtectedRoute><ProviderView/></ProtectedRoute>} />

          <Route path="/info" element={<PublicInfo/>} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}
