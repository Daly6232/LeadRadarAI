"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { api } from "../lib/api";

const nav = [
  { href: "/dashboard", label: "📊 Dashboard" },
  { href: "/leads", label: "🎯 Leads" },
  { href: "/scan", label: "🔍 Scan" },
  { href: "/export", label: "📤 Export" },
];

export default function Sidebar() {
  const path = usePathname();
  return (
    <aside style={{
      width: 220, minHeight: "100vh", background: "#1E3A5F",
      color: "#fff", display: "flex", flexDirection: "column",
      padding: "24px 0", position: "fixed", left: 0, top: 0
    }}>
      <div style={{ padding: "0 20px 24px", borderBottom: "1px solid #2d5a8e" }}>
        <h2 style={{ margin: 0, fontSize: 18, color: "#4FC3F7" }}>⚡ LeadRadar AI</h2>
        <p style={{ margin: "4px 0 0", fontSize: 12, color: "#90CAF9" }}>v2.0</p>
      </div>
      <nav style={{ flex: 1, padding: "16px 0" }}>
        {nav.map(({ href, label }) => (
          <Link key={href} href={href} style={{
            display: "block", padding: "12px 20px", color: path === href ? "#4FC3F7" : "#CBD5E1",
            background: path === href ? "rgba(79,195,247,0.1)" : "transparent",
            textDecoration: "none", borderLeft: path === href ? "3px solid #4FC3F7" : "3px solid transparent",
            fontSize: 14, fontWeight: path === href ? 600 : 400,
          }}>
            {label}
          </Link>
        ))}
      </nav>
      <div style={{ padding: "16px 20px", borderTop: "1px solid #2d5a8e" }}>
        <button onClick={() => { api.logout(); window.location.href = "/login"; }}
          style={{ background: "transparent", border: "1px solid #ef5350", color: "#ef5350",
            padding: "8px 16px", borderRadius: 6, cursor: "pointer", fontSize: 13, width: "100%" }}>
          🚪 Logout
        </button>
      </div>
    </aside>
  );
}
