import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate
} from "react-router-dom";
import Login from "./pages/Login";
import Clients from "./pages/Clients";
import ClientDetail from "./pages/ClientDetail";

export default function App() {
  const token = localStorage.getItem("token");
  return (
    <Router>
      <nav style={{ padding: 12, borderBottom: "1px solid #ddd" }}>
        <Link style={{ marginRight: 8 }} to="/">Home</Link>
        {token ? (
          <>
            <Link style={{ marginRight: 8 }} to="/clients">Clients</Link>
            <button onClick={() => { localStorage.removeItem("token"); window.location.href = "/"; }}>Logout</button>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </nav>
      <div style={{ padding: 12 }}>
        <Routes>
          <Route path="/" element={<Navigate to={token ? "/clients" : "/login"} />} />
          <Route path="/login" element={<Login />} />
          <Route path="/clients" element={<Clients />} />
          <Route path="/clients/:id" element={<ClientDetail />} />
        </Routes>
      </div>
    </Router>
  );
}
