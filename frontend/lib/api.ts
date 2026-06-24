const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken() {
  return typeof window !== "undefined" ? localStorage.getItem("token") : null;
}

async function request(path: string, options: RequestInit = {}) {
  const token = getToken();
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  register: (email: string, password: string) =>
    request("/auth/register", { method: "POST", body: JSON.stringify({ email, password }) }),

  login: async (email: string, password: string) => {
    const data = await request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    if (data.access_token) localStorage.setItem("token", data.access_token);
    return data;
  },

  logout: () => localStorage.removeItem("token"),

  getLeads: (params?: Record<string, string | number>) => {
    const qs = params ? "?" + new URLSearchParams(params as any).toString() : "";
    return request(`/leads/${qs}`);
  },

  getLead: (id: number) => request(`/leads/${id}`),

  deleteLead: (id: number) => request(`/leads/${id}`, { method: "DELETE" }),

  scan: (category: string, city: string, country: string, limit = 20) =>
    request("/leads/scan", {
      method: "POST",
      body: JSON.stringify({ category, city, country, limit }),
    }),

  getStats: () => request("/leads/stats"),

  exportUrl: (format: "csv" | "json" | "excel") => `${BASE}/leads/export/${format}`,
};
