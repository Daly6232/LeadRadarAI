"use client";
import Sidebar from "../../components/Sidebar";
import { api } from "../../lib/api";

export default function ExportPage() {
  function download(format: "csv" | "json" | "excel") {
    window.open(api.exportUrl(format), "_blank");
  }

  const formats = [
    { id: "csv" as const, label: "CSV", icon: "📄", desc: "Compatible with Excel, Google Sheets" },
    { id: "excel" as const, label: "Excel (.xlsx)", icon: "📊", desc: "Formatted spreadsheet with styling" },
    { id: "json" as const, label: "JSON", icon: "📋", desc: "For developers and API integrations" },
  ];

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0F1B2D" }}>
      <Sidebar />
      <main style={{ marginLeft: 220, flex: 1, padding: 32 }}>
        <h1 style={{ color: "#fff", margin: "0 0 6px", fontSize: 24 }}>📤 Export Leads</h1>
        <p style={{ color: "#90CAF9", margin: "0 0 32px", fontSize: 14 }}>Download all your leads in your preferred format</p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: 16, maxWidth: 800 }}>
          {formats.map(f => (
            <div key={f.id} style={{ background: "#1E3A5F", borderRadius: 10, padding: 28, textAlign: "center" }}>
              <div style={{ fontSize: 40, marginBottom: 12 }}>{f.icon}</div>
              <h3 style={{ color: "#fff", margin: "0 0 8px", fontSize: 17 }}>{f.label}</h3>
              <p style={{ color: "#90CAF9", fontSize: 13, margin: "0 0 20px" }}>{f.desc}</p>
              <button onClick={() => download(f.id)}
                style={{ width: "100%", padding: "11px", background: "#4FC3F7", color: "#0F1B2D", border: "none", borderRadius: 8, fontWeight: 700, cursor: "pointer", fontSize: 14 }}>
                Download {f.label}
              </button>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
