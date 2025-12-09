import React, { useEffect, useState } from 'react';
import GroceryList from './components/GroceryList';
import AddItemForm from './components/AddItemForm';
import Recommendations from './components/Recommendations';
import ExpiringReminders from './components/ExpiringReminders';
import HealthySuggestion from './components/HealthySuggestion';

const API = process.env.REACT_APP_API || 'http://localhost:5000';

function App(){
  const [items,setItems] = useState([]);
  const [selectedForRec, setSelectedForRec] = useState([]);
  const [recs, setRecs] = useState([]);
  const [healthy, setHealthy] = useState(null);

  useEffect(()=> fetchItems(), []);

  async function fetchItems(){
    const res = await fetch(`${API}/items`);
    const data = await res.json();
    setItems(data);
  }

  function toggleSelect(name){
    setSelectedForRec(prev => {
      const n = prev.includes(name) ? prev.filter(x=>x!==name) : [...prev, name];
      return n;
    });
  }

  async function handleGetRecs(){
    const res = await fetch(`${API}/recommendations`, {
      method:'POST',
      headers:{ 'Content-Type': 'application/json' },
      body: JSON.stringify({ current: selectedForRec })
    });
    const data = await res.json();
    setRecs(data.recommendations || []);
  }

  async function handleGetHealthy(itemName){
    const res = await fetch(`${API}/healthy-subs?item=${encodeURIComponent(itemName)}`);
    const data = await res.json();
    setHealthy(data);
  }

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif', maxWidth:900, margin:'0 auto' }}>
      <h1>Smart Grocery Shopping Assistant</h1>
      <p>Manage items, get recommended missing items, healthy alternatives, and expiring reminders.</p>

      <AddItemForm onAdded={fetchItems} api={API} />
      <GroceryList items={items} onRefresh={fetchItems} toggleSelect={toggleSelect} selected={selectedForRec} onHealthy={handleGetHealthy} />
      <div style={{ display:'flex', gap:20, marginTop:20 }}>
        <div style={{ flex:1 }}>
          <h3>Recommendations</h3>
          <button onClick={handleGetRecs}>Predict Missing Items for Selected</button>
          <Recommendations recs={recs} />
        </div>
        <div style={{ flex:1 }}>
          <h3>Healthy Substitution</h3>
          <HealthySuggestion healthy={healthy} />
        </div>
      </div>

      <div style={{ marginTop: 30 }}>
        <ExpiringReminders api={API} />
      </div>
    </div>
  );
}

export default App;
