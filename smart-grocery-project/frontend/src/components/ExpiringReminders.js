import React, { useEffect, useState } from 'react';

export default function ExpiringReminders({ api }) {
  const [days, setDays] = useState(7);
  const [result, setResult] = useState(null);

  async function load() {
    const res = await fetch(`${api}/expiring?days=${days}`);
    const data = await res.json();
    setResult(data);
  }
  useEffect(()=>{ load(); }, []);

  return (
    <div>
      <h3>Expiring Soon</h3>
      <div style={{ display:'flex', gap:8, alignItems:'center' }}>
        <label>Days ahead:</label>
        <input type="number" value={days} onChange={e=>setDays(e.target.value)} style={{ width:80 }} />
        <button onClick={load}>Check</button>
      </div>
      <div style={{ marginTop:10 }}>
        {result ? (
          <div>
            <div>{result.count} item(s) expiring within {days} days.</div>
            <ul>
              {result.items.map(it=> <li key={it.id}>{it.name} — expiry: {it.expiryDate}</li>)}
            </ul>
          </div>
        ) : <div>Loading...</div>}
      </div>
    </div>
  );
}
