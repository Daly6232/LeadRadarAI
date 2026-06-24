"use client";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import { api } from "../../lib/api";

interface Stats {
  total_leads: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
  average_score: number;
  leads_with_website: number;
  leads_without_website: number;
}

function StatCard({ label, value, color }: { label: string; value: string | number; color: string }) {
  return (
    <div style={{ background: "#1E3A5F", borderRadius: 10, padding: "20px 24px", borderLeft: `4px solid ${color}` }}>
      <div style={{ color: "#90CAF9", fontSize: 13, marginBottom: 6 }}>{label}</div>
      <div style={{ color: "#fff", fontSize: 28, fontWeight: 700 }}>{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getStats().then(setStats).catch(console.error).finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0F1B2D" }}>
      <Sidebar />
      <main style={{ marginLeft: 220, flex: 1, padding: 32 }}>
        <h1 style={{ color: "#fff", margin: "0 0 6px", fontSize: 24 }}>Dashboard</h1>
        <p style={{ color: "#90CAF9", margin: "0 0 32px", fontSize: 14 }}>Lead intelligence overview</p>

        {loading ? (
          <p style={{ color: "#4FC3F7" }}>Loading stats...</p>
        ) : stats ? (
          <>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16, marginBottom: 32 }}>
              <StatCard label="Total Leads" value={stats.total_leads} color="#4FC3F7" />
              <StatCard label="High Priority" value={stats.high_priority} color="#ef5350" />
              <StatCard label="Medium Priority" value={stats.medium_priority} color="#FFA726" />
              <StatCard label="Low Priority" value={stats.low_priority} color="#66BB6A" />
              <StatCard label="Avg Score" value={`${stats.average_score}/100`} color="#AB47BC" />
              <StatCard label="Have Website" value={stats.leads_with_website} color="#26C6DA" />
              <StatCard label="No Website" value={stats.leads_without_website} color="#EF9A9A" />
            </div>

            <div style={{ background: "#1E3A5F", borderRadius: 10, padding: 24 }}>
              <h3 style={{ color: "#4FC3F7", margin: "0 0 16px" }}>Quick Actions</h3>
              <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
                <a href="/scan" style={{ background: "#4FC3F7", color: "#0F1B2D", padding: "10px 20px", borderRadius: 8, textDecoration: "none", fontWeight: 600, fontSize: 14 }}>🔍 New Scan</a>
                <a href="/leads" style={{ background: "transparent", color: "#4FC3F7", border: "1px solid #4FC3F7", padding: "10px 20px", borderRadius: 8, textDecoration: "none", fontSize: 14 }}>🎯 View Leads</a>
                <a href="/export" style={{ background: "transparent", color: "#90CAF9", border: "1px solid #2d5a8e", padding: "10px 20px", borderRadius: 8, textDecoration: "none", fontSize: 14 }}>📤 Export</a>
              </div>
            </div>
          </>
        ) : (
          <p style={{ color: "#ef5350" }}>Could not load stats.</p>
        )}
      </main>
    </div>
  );
}
