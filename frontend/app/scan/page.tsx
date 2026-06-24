"use client";
import { useState } from "react";
import Sidebar from "../../components/Sidebar";
import { api } from "../../lib/api";

export default function ScanPage() {
  const [category, setCategory] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  async function handleScan() {
    if (!category || !city || !country) { setError("All fields required"); return; }
    setLoading(true); setError(""); setResult(null);
    try {
      const res = await api.scan(category, city, country, limit);
      setResult(res);
    } catch (e: any) {
      setError(e.message);
    } finally { setLoading(false); }
  }

  const input = (placeholder: string, value: string, onChange: (v: string) => void) => (
    <input placeholder={placeholder} value={value} onChange={e => onChange(e.target.value)}
      style={{ width: "100%", padding: "12px 14px", borderRadius: 8, border: "1px solid #2d5a8e",
        background: "#0F1B2D", color: "#fff", fontSize: 14, boxSizing: "border-box", marginBottom: 12 }} />
  );

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0F1B2D" }}>
      <Sidebar />
      <main style={{ marginLeft: 220, flex: 1, padding: 32 }}>
        <h1 style={{ color: "#fff", margin: "0 0 6px", fontSize: 24 }}>🔍 Business Scan</h1>
        <p style={{ color: "#90CAF9", margin: "0 0 32px", fontSize: 14 }}>Discover and analyze businesses automatically</p>

        <div style={{ background: "#1E3A5F", borderRadius: 10, padding: 28, maxWidth: 500 }}>
          {input("Category (e.g. dentist, restaurant, lawyer)", category, setCategory)}
          {input("City (e.g. London, Paris, Tunis)", city, setCity)}
          {input("Country (e.g. UK, France, Tunisia)", country, setCountry)}
          <div style={{ marginBottom: 20 }}>
            <label style={{ color: "#90CAF9", fontSize: 13, display: "block", marginBottom: 6 }}>Max results: {limit}</label>
            <input type="range" min={5} max={50} value={limit} onChange={e => setLimit(+e.target.value)}
              style={{ width: "100%", accentColor: "#4FC3F7" }} />
          </div>

          {error && <div style={{ background: "#ef5350", color: "#fff", padding: "10px 14px", borderRadius: 6, marginBottom: 16, fontSize: 13 }}>{error}</div>}

          <button onClick={handleScan} disabled={loading}
            style={{ width: "100%", padding: "13px", background: loading ? "#2d5a8e" : "#4FC3F7",
              color: "#0F1B2D", border: "none", borderRadius: 8, fontSize: 15, fontWeight: 700, cursor: loading ? "not-allowed" : "pointer" }}>
            {loading ? "⏳ Scanning... (may take 30–60s)" : "🚀 Start Scan"}
          </button>
        </div>

        {result && (
          <div style={{ background: "#1a3a1a", border: "1px solid #43a047", borderRadius: 10, padding: 24, marginTop: 24, maxWidth: 500 }}>
            <h3 style={{ color: "#66BB6A", margin: "0 0 8px" }}>✅ Scan Complete</h3>
            <p style={{ color: "#fff", margin: "0 0 4px", fontSize: 16 }}>{result.message}</p>
            {result.count > 0 && (
              <a href="/leads" style={{ color: "#4FC3F7", fontSize: 14 }}>→ View leads</a>
            )}
          </div>
        )}

        <div style={{ marginTop: 32, background: "#1E3A5F", borderRadius: 10, padding: 24, maxWidth: 500 }}>
          <h3 style={{ color: "#4FC3F7", margin: "0 0 12px", fontSize: 15 }}>💡 Example searches</h3>
          {[
            ["dentist", "London", "UK"],
            ["restaurant", "Paris", "France"],
            ["lawyer", "Tunis", "Tunisia"],
            ["gym", "Dubai", "UAE"],
          ].map(([cat, c, co]) => (
            <button key={cat + c} onClick={() => { setCategory(cat); setCity(c); setCountry(co); }}
              style={{ background: "#0F1B2D", border: "1px solid #2d5a8e", color: "#90CAF9",
                padding: "6px 14px", borderRadius: 20, fontSize: 12, cursor: "pointer", margin: "4px 4px 4px 0" }}>
              {cat} in {c}
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}
