import React, { useEffect, useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";

export default function Clients() {
  const [clients, setClients] = useState([]);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);

  async function fetchClients() {
    try {
      const res = await api.get("/clients", { q, page, per_page: 25 });
      setClients(res);
    } catch (err) {
      console.error(err);
      alert("Error fetching clients");
    }
  }

  useEffect(() => { fetchClients(); }, [page]);

  return (
    <div>
      <h2>Clients</h2>
      <div style={{ marginBottom: 8 }}>
        <input placeholder="search name or email" value={q} onChange={e => setQ(e.target.value)} />
        <button onClick={() => { setPage(1); fetchClients(); }}>Search</button>
      </div>
      <table border="1" cellPadding="6">
        <thead>
          <tr><th>ID</th><th>Name</th><th>Email</th><th>Active</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {clients.map(c => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.name}</td>
              <td>{c.email}</td>
              <td>{String(c.is_active)}</td>
              <td>
                <Link to={`/clients/${c.id}`}>View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: 8 }}>
        <button onClick={() => setPage(p => Math.max(1, p-1))}>Prev</button>
        <span style={{ margin: "0 8px" }}>Page {page}</span>
        <button onClick={() => setPage(p => p+1)}>Next</button>
      </div>
    </div>
  );
}
