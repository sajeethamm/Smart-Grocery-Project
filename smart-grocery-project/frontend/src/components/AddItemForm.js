import React, { useState } from 'react';

export default function AddItemForm({ onAdded, api }) {
  const [name, setName] = useState('');
  const [category,setCategory] = useState('');
  const [purchaseDate, setPurchaseDate] = useState(new Date().toISOString().slice(0,10));
  const [shelf, setShelf] = useState(7);

  async function submit(e){
    e.preventDefault();
    if (!name) return alert('enter name');
    await fetch(`${api}/items`, {
      method:'POST',
      headers:{ 'Content-Type':'application/json' },
      body: JSON.stringify({ name, category, purchaseDate, shelfLifeDays: shelf })
    });
    setName('');
    onAdded();
  }

  return (
    <form onSubmit={submit} style={{ marginBottom:20, display:'flex', gap:10, alignItems:'center' }}>
      <input value={name} placeholder="Item name" onChange={e=>setName(e.target.value)} />
      <input value={category} placeholder="Category" onChange={e=>setCategory(e.target.value)} />
      <input type="date" value={purchaseDate} onChange={e=>setPurchaseDate(e.target.value)} />
      <input type="number" value={shelf} onChange={e=>setShelf(e.target.value)} style={{ width:80 }} />
      <button type="submit">Add</button>
    </form>
  );
}
