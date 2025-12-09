import React from 'react';

export default function Recommendations({ recs=[] }) {
  if (!recs || recs.length===0) return <div>No recommendations. Select items and click predict.</div>;
  return (
    <ul>
      {recs.map(r=>(
        <li key={r.name}>{r.name} (score: {r.score})</li>
      ))}
    </ul>
  );
}
