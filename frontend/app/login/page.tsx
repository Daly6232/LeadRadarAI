"use client";
import { useState } from "react";
import { api } from "../../lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true); setError("");
    try {
      await api.login(email, password);
      window.location.href = "/dashboard";
    } catch (e: any) {
      setError(e.message);
    } finally { setLoading(false); }
  }

  return (
    <div style={{ minHeight: "100vh", background: "#0F1B2D", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ background: "#1E3A5F", padding: 40, borderRadius: 12, width: 360, boxShadow: "0 8px 32px rgba(0,0,0,0.4)" }}>
        <h1 style={{ color: "#4FC3F7", margin: "0 0 8px", fontSize: 24 }}>⚡ LeadRadar AI</h1>
        <p style={{ color: "#90CAF9", margin: "0 0 28px", fontSize: 14 }}>Sign in to your account</p>
        {error && <div style={{ background: "#ef5350", color: "#fff", padding: "10px 14px", borderRadius: 6, marginBottom: 16, fontSize: 13 }}>{error}</div>}
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)}
          style={{ width: "100%", padding: "12px 14px", borderRadius: 8, border: "1px solid #2d5a8e", background: "#0F1B2D", color: "#fff", fontSize: 14, marginBottom: 12, boxSizing: "border-box" }} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSubmit()}
          style={{ width: "100%", padding: "12px 14px", borderRadius: 8, border: "1px solid #2d5a8e", background: "#0F1B2D", color: "#fff", fontSize: 14, marginBottom: 20, boxSizing: "border-box" }} />
        <button onClick={handleSubmit} disabled={loading}
          style={{ width: "100%", padding: "13px", background: "#4FC3F7", color: "#0F1B2D", border: "none", borderRadius: 8, fontSize: 15, fontWeight: 700, cursor: loading ? "not-allowed" : "pointer" }}>
          {loading ? "Signing in..." : "Sign In"}
        </button>
        <p style={{ color: "#90CAF9", textAlign: "center", marginTop: 20, fontSize: 13 }}>
          No account? <a href="/register" style={{ color: "#4FC3F7" }}>Register</a>
        </p>
      </div>
    </div>
  );
}
