import React from 'react';

export default function HealthySuggestion({ healthy }) {
  if (!healthy) return <div>Click 'Healthy' for an item in the list.</div>;
  if (!healthy.alternative) return <div>No healthier alternative found for <b>{healthy.item}</b></div>;
  return (
    <div>
      <div>Alternative for <b>{healthy.item}</b>:</div>
      <div style={{ marginTop:8, padding:8, border:'1px solid #ddd', borderRadius:6 }}>
        <b>{healthy.alternative}</b>
      </div>
    </div>
  );
}
