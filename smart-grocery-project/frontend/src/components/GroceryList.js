import React from 'react';

export default function GroceryList({ items=[], onRefresh, toggleSelect, selected=[], onHealthy }) {
  async function del(id){
    await fetch(`http://localhost:5000/items/${id}`, { method:'DELETE' });
    onRefresh();
  }
  return (
    <div>
      <h3>Grocery Items</h3>
      {items.length===0 && <div>No items</div>}
      <table border="1" cellPadding="6" style={{ borderCollapse:'collapse', width:'100%' }}>
        <thead><tr><th>Select</th><th>Name</th><th>Category</th><th>Purchase Date</th><th>Expiry Date</th><th>Actions</th></tr></thead>
        <tbody>
          {items.map(it=>(
            <tr key={it.id}>
              <td><input type="checkbox" checked={selected.includes(it.name)} onChange={()=>toggleSelect(it.name)} /></td>
              <td>{it.name}</td>
              <td>{it.category}</td>
              <td>{it.purchaseDate}</td>
              <td>{it.expiryDate}</td>
              <td>
                <button onClick={()=>onHealthy(it.name)}>Healthy</button>
                <button onClick={()=>del(it.id)} style={{ marginLeft:8 }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
