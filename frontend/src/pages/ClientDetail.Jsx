import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import Papa from "papaparse";

export default function ClientDetail() {
  const { id } = useParams();
  const [client, setClient] = useState(null);
  const [allocations, setAllocations] = useState([]);
  const [movements, setMovements] = useState([]);
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");

  async function fetchAll() {
    try {
      const c = await api.get(`/clients/${id}`);
      setClient(c);
      const allocs = await api.get(`/allocations/client/${id}`);
      setAllocations(allocs);
      const mv = await api.get(`/movements`, { client_id: id });
      setMovements(mv);
    } catch (err) {
      console.error(err);
      alert("Error loading data");
    }
  }

  useEffect(() => { fetchAll(); }, [id]);

  function exportCSV() {
    const csv = Papa.unparse({
      allocations,
      movements
    }, { header: true });
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `client_${id}_export.csv`;
    a.click();
  }

  function filterMovements() {
    // reload movements with params
    const params = {};
    if (start) params.start_date = start;
    if (end) params.end_date = end;
    fetchMovements(params);
  }

  async function fetchMovements(params = {}) {
    try {
      const mv = await api.get("/movements", { client_id: id, ...params });
      setMovements(mv);
    } catch (err) {
      console.error(err);
      alert("Error fetching movements");
    }
  }

  return (
    <div>
      <h2>Client #{id}</h2>
      {client && <div>
        <b>Name:</b> {client.name} <br/>
        <b>Email:</b> {client.email}
      </div>}
      <section style={{ marginTop: 12 }}>
        <h3>Allocations</h3>
        <table border="1" cellPadding="6">
          <thead><tr><th>ID</th><th>Asset</th><th>Quantity</th><th>Buy price</th><th>Buy date</th></tr></thead>
          <tbody>
            {allocations.map(a => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.asset_id}</td>
                <td>{a.quantity}</td>
                <td>{a.buy_price}</td>
                <td>{a.buy_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section style={{ marginTop: 12 }}>
        <h3>Movements</h3>
        <div>
          <label>From:</label>
          <input type="date" value={start} onChange={e => setStart(e.target.value)} />
          <label>To:</label>
          <input type="date" value={end} onChange={e => setEnd(e.target.value)} />
          <button onClick={filterMovements}>Filter</button>
        </div>
        <table border="1" cellPadding="6">
          <thead><tr><th>ID</th><th>Type</th><th>Amount</th><th>Date</th><th>Note</th></tr></thead>
          <tbody>
            {movements.map(m => (
              <tr key={m.id}>
                <td>{m.id}</td>
                <td>{m.type}</td>
                <td>{m.amount}</td>
                <td>{m.date}</td>
                <td>{m.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <div style={{ marginTop: 12 }}>
        <button onClick={exportCSV}>Export CSV</button>
      </div>
    </div>
  );
}
