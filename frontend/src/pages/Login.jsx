import React, { useState } from "react";
import api from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  async function submit(e) {
    e.preventDefault();
    try {
      // OAuth2PasswordRequestForm expects username + password fields in form data
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);
      const res = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        body: params,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      });
      if (!res.ok) {
        const j = await res.json();
        throw new Error(j.detail || "Login failed");
      }
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      window.location.href = "/clients";
    } catch (error) {
      setErr(error.message);
    }
  }

  return (
    <div style={{ maxWidth: 480 }}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <div>
          <label>Email</label><br/>
          <input value={email} onChange={e => setEmail(e.target.value)} type="email" required />
        </div>
        <div>
          <label>Password</label><br/>
          <input value={password} onChange={e => setPassword(e.target.value)} type="password" required />
        </div>
        <div style={{ marginTop: 8 }}>
          <button type="submit">Login</button>
        </div>
        {err && <div style={{ color: "red", marginTop: 8 }}>{err}</div>}
      </form>
    </div>
  );
}
