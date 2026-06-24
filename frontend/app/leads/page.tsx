"use client";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import { api } from "../../lib/api";

const priorityColor: Record<string, string> = {
  High: "#ef5350", Medium: "#FFA726", Low: "#66BB6A"
};

export default function LeadsPage() {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<any>(null);
  const [filter, setFilter] = useState({ priority: "", min_score: "" });

  function load() {
    const params: any = {};
    if (filter.priority) params.priority = filter.priority;
    if (filter.min_score) params.min_score = filter.min_score;
    api.getLeads(params).then(setLeads).catch(console.error).finally(() => setLoading(false));
  }

  useEffect(() => { load(); }, []);

  async function handleDelete(id: number) {
    await api.deleteLead(id);
    setLeads(l => l.filter(x => x.id !== id));
    if (selected?.id === id) setSelected(null);
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0F1B2D" }}>
      <Sidebar />
      <main style={{ marginLeft: 220, flex: 1, padding: 32 }}>
        <h1 style={{ color: "#fff", margin: "0 0 6px", fontSize: 24 }}>🎯 Leads</h1>
        <p style={{ color: "#90CAF9", margin: "0 0 20px", fontSize: 14 }}>{leads.length} leads found</p>

        <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
          <select value={filter.priority} onChange={e => setFilter(f => ({ ...f, priority: e.target.value }))}
            style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #2d5a8e", background: "#1E3A5F", color: "#fff", fontSize: 13 }}>
            <option value="">All Priorities</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
          <input placeholder="Min score (e.g. 50)" value={filter.min_score}
            onChange={e => setFilter(f => ({ ...f, min_score: e.target.value }))}
            style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #2d5a8e", background: "#1E3A5F", color: "#fff", fontSize: 13, width: 160 }} />
          <button onClick={load} style={{ padding: "8px 16px", background: "#4FC3F7", color: "#0F1B2D", border: "none", borderRadius: 8, cursor: "pointer", fontWeight: 600, fontSize: 13 }}>Filter</button>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: selected ? "1fr 380px" : "1fr", gap: 16 }}>
          <div>
            {loading ? <p style={{ color: "#4FC3F7" }}>Loading...</p> : leads.length === 0 ? (
              <div style={{ background: "#1E3A5F", borderRadius: 10, padding: 32, textAlign: "center" }}>
                <p style={{ color: "#90CAF9" }}>No leads yet. <a href="/scan" style={{ color: "#4FC3F7" }}>Run a scan</a></p>
              </div>
            ) : leads.map(lead => (
              <div key={lead.id} onClick={() => setSelected(selected?.id === lead.id ? null : lead)}
                style={{ background: selected?.id === lead.id ? "#1a3050" : "#1E3A5F", borderRadius: 10, padding: "16px 20px",
                  marginBottom: 10, cursor: "pointer", border: `1px solid ${selected?.id === lead.id ? "#4FC3F7" : "transparent"}`,
                  display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
                  <div style={{ color: "#fff", fontWeight: 600, fontSize: 15 }}>{lead.business_name}</div>
                  <div style={{ color: "#90CAF9", fontSize: 12, marginTop: 3 }}>
                    {lead.city} · {lead.category} · {lead.has_website ? "🌐 Website" : "❌ No website"}
                  </div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ color: priorityColor[lead.priority] || "#fff", fontWeight: 700, fontSize: 14 }}>{lead.priority}</div>
                  <div style={{ color: "#4FC3F7", fontSize: 18, fontWeight: 700 }}>{lead.score}</div>
                </div>
              </div>
            ))}
          </div>

          {selected && (
            <div style={{ background: "#1E3A5F", borderRadius: 10, padding: 24, height: "fit-content", position: "sticky", top: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                <h3 style={{ color: "#4FC3F7", margin: 0, fontSize: 16 }}>{selected.business_name}</h3>
                <button onClick={() => setSelected(null)} style={{ background: "transparent", border: "none", color: "#90CAF9", cursor: "pointer", fontSize: 18 }}>✕</button>
              </div>
              <div style={{ color: "#90CAF9", fontSize: 12, marginBottom: 16 }}>
                {selected.city} · {selected.country} · Score: <span style={{ color: "#4FC3F7", fontWeight: 700 }}>{selected.score}/100</span>
              </div>
              {selected.website && <p style={{ color: "#fff", fontSize: 13, margin: "0 0 8px" }}>🌐 <a href={selected.website} target="_blank" style={{ color: "#4FC3F7" }}>{selected.website}</a></p>}
              {selected.email && <p style={{ color: "#fff", fontSize: 13, margin: "0 0 8px" }}>📧 {selected.email}</p>}
              {selected.phone && <p style={{ color: "#fff", fontSize: 13, margin: "0 0 8px" }}>📞 {selected.phone}</p>}
              {selected.score_explanation && (
                <div style={{ background: "#0F1B2D", borderRadius: 8, padding: 14, margin: "12px 0", fontSize: 12, color: "#CBD5E1", whiteSpace: "pre-line" }}>
                  {selected.score_explanation}
                </div>
              )}
              {selected.outreach_strategy && (
                <div style={{ background: "#1a3a1a", borderRadius: 8, padding: 14, margin: "12px 0", fontSize: 12, color: "#A5D6A7", whiteSpace: "pre-line" }}>
                  {selected.outreach_strategy}
                </div>
              )}
              <button onClick={() => handleDelete(selected.id)}
                style={{ width: "100%", marginTop: 12, padding: "9px", background: "transparent", border: "1px solid #ef5350", color: "#ef5350", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
                🗑 Delete Lead
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
