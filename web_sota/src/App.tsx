import { useCallback, useEffect, useState } from "react";

import {
  DEFAULT_EXAMPLE_FEED_URL,
  EXAMPLE_FEEDS,
  feedlySubscribeUrl,
  inoreaderSubscribeUrl,
} from "./example_feeds";

type Tab = "rss" | "weather" | "probe" | "resolve" | "opml";

const LS_SIDEBAR = "glance.sidebar.collapsed";
const SIDEBAR_W = { open: 228, shut: 56 } as const;

const NAV: { id: Tab; label: string; short: string; hint: string }[] = [
  { id: "rss", label: "Feeds", short: "F", hint: "RSS / Atom feeds" },
  { id: "weather", label: "Weather", short: "W", hint: "Open-Meteo forecast" },
  { id: "probe", label: "Fleet probe", short: "P", hint: "Parallel HTTP health checks" },
  { id: "resolve", label: "Redirects", short: "T", hint: "HTTP redirect chain (trace hops)" },
  { id: "opml", label: "OPML", short: "O", hint: "Parse OPML → feed URLs" },
];

export default function App() {
  const [tab, setTab] = useState<Tab>("rss");
  const [busy, setBusy] = useState(false);
  const [out, setOut] = useState<string>("");
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    try {
      return globalThis.localStorage?.getItem(LS_SIDEBAR) === "1";
    } catch {
      return false;
    }
  });

  useEffect(() => {
    try {
      globalThis.localStorage?.setItem(LS_SIDEBAR, sidebarCollapsed ? "1" : "0");
    } catch {
      /* ignore */
    }
  }, [sidebarCollapsed]);

  const run = useCallback(async (path: string, body: unknown) => {
    setBusy(true);
    setOut("");
    try {
      const r = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const j = await r.json();
      setOut(JSON.stringify(j, null, 2));
    } catch (e) {
      setOut(String(e));
    } finally {
      setBusy(false);
    }
  }, []);

  const sw = sidebarCollapsed ? SIDEBAR_W.shut : SIDEBAR_W.open;

  return (
    <div style={{ display: "flex", minHeight: "100vh", width: "100%", background: "#0f1115" }}>
      <aside
        style={{
          width: sw,
          minWidth: sw,
          flexShrink: 0,
          display: "flex",
          flexDirection: "column",
          borderRight: "1px solid rgba(100,120,160,.22)",
          background: "linear-gradient(180deg, rgba(28,32,42,.98), rgba(14,16,22,.99))",
          transition: "width 0.22s ease, min-width 0.22s ease",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            padding: sidebarCollapsed ? "14px 8px" : "18px 16px",
            borderBottom: "1px solid rgba(100,120,160,.15)",
          }}
        >
          {sidebarCollapsed ? (
            <div
              style={{
                fontSize: 13,
                fontWeight: 700,
                letterSpacing: "-0.02em",
                textAlign: "center",
                color: "#8ec5ff",
              }}
              title="glance-mcp"
            >
              g
            </div>
          ) : (
            <>
              <div style={{ fontSize: 15, fontWeight: 700, color: "#e8eaef", letterSpacing: "-0.02em" }}>
                glance-mcp
              </div>
              <div style={{ fontSize: 11, opacity: 0.55, marginTop: 4 }}>fleet utilities</div>
            </>
          )}
        </div>

        <nav style={{ padding: 8, display: "flex", flexDirection: "column", gap: 6, flex: 1 }}>
          {NAV.map((item) => {
            const on = tab === item.id;
            return (
              <button
                key={item.id}
                type="button"
                title={item.hint}
                onClick={() => setTab(item.id)}
                style={{
                  width: "100%",
                  padding: sidebarCollapsed ? "10px 0" : "10px 12px",
                  borderRadius: 10,
                  border: on ? "1px solid rgba(100,160,240,.45)" : "1px solid transparent",
                  background: on ? "rgba(70,110,190,.28)" : "transparent",
                  color: "#e8eaef",
                  cursor: "pointer",
                  textAlign: sidebarCollapsed ? "center" : "left",
                  fontSize: sidebarCollapsed ? 14 : 14,
                  fontWeight: on ? 600 : 500,
                }}
              >
                {sidebarCollapsed ? item.short : item.label}
              </button>
            );
          })}
        </nav>

        <div style={{ padding: 8, borderTop: "1px solid rgba(100,120,160,.12)" }}>
          <button
            type="button"
            onClick={() => setSidebarCollapsed((c) => !c)}
            title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            style={{
              width: "100%",
              padding: "8px 6px",
              borderRadius: 8,
              border: "1px solid rgba(100,120,160,.25)",
              background: "rgba(30,36,48,.6)",
              color: "#b8c0d0",
              cursor: "pointer",
              fontSize: 12,
            }}
          >
            {sidebarCollapsed ? "»" : "« Collapse"}
          </button>
        </div>
      </aside>

      <main
        style={{
          flex: 1,
          minWidth: 0,
          overflow: "auto",
          padding: "1.25rem 1.5rem 2rem",
        }}
      >
        <div style={{ maxWidth: 920, margin: "0 auto" }}>
          <header
            style={{
              marginBottom: "1.25rem",
              padding: "1.1rem 1.25rem",
              borderRadius: 12,
              background: "linear-gradient(145deg, rgba(40,48,64,.9), rgba(20,24,32,.95))",
              border: "1px solid rgba(120,140,180,.25)",
            }}
          >
            <h1 style={{ margin: "0 0 .35rem", fontSize: "1.35rem" }}>
              {NAV.find((n) => n.id === tab)?.label ?? tab}
            </h1>
            <p style={{ margin: 0, opacity: 0.88, fontSize: "0.92rem" }}>
              {tab === "rss" &&
                "RSS / Atom (podcasts, blogs, releases). Click titles to open — no copy-paste."}
              {tab === "weather" && "Open-Meteo grid forecast — no API key."}
              {tab === "probe" &&
                "Parallel GET for /health URLs. Click results to open — metadata IPs blocked."}
              {tab === "resolve" &&
                "Hop-by-hop redirect trace (HEAD or GET). Use GET if the server rejects HEAD (405)."}
              {tab === "opml" &&
                "Paste OPML subscription XML; get a list of feed URLs (open links — no copy-paste)."}
            </p>
          </header>

          {tab === "rss" && <RssPanel />}
          {tab === "weather" && <WeatherPanel busy={busy} onRun={run} />}
          {tab === "probe" && <ProbePanel />}
          {tab === "resolve" && <ResolvePanel />}
          {tab === "opml" && <OpmlPanel />}

          {tab === "weather" && (
            <pre
              style={{
                marginTop: 20,
                padding: 12,
                borderRadius: 8,
                background: "#151922",
                border: "1px solid #2a3140",
                overflow: "auto",
                maxHeight: 420,
                fontSize: 12,
              }}
            >
              {out || "…"}
            </pre>
          )}
        </div>
      </main>
    </div>
  );
}

type RssEntry = {
  title?: string | null;
  link?: string | null;
  published?: string | null;
  summary?: string | null;
};

type RssJson = {
  success?: boolean;
  feed_title?: string | null;
  message?: string;
  entries?: RssEntry[];
  error?: string;
};

function RssPanel() {
  const [url, setUrl] = useState(DEFAULT_EXAMPLE_FEED_URL);
  const [busy, setBusy] = useState(false);
  const [data, setData] = useState<RssJson | null>(null);

  const fetchFeed = useCallback(async () => {
    setBusy(true);
    setData(null);
    try {
      const r = await fetch("/api/rss/fetch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feed_url: url, max_items: 25 }),
      });
      const j = (await r.json()) as RssJson;
      setData(j);
    } catch (e) {
      setData({ success: false, error: String(e) });
    } finally {
      setBusy(false);
    }
  }, [url]);

  const entries = data?.success && Array.isArray(data.entries) ? data.entries : [];
  const feedTitle = data?.feed_title;

  return (
    <section>
      <p style={{ opacity: 0.85, marginTop: 0 }}>
        Default: <strong>Simon Willison</strong> (full Atom). Chips include <strong>Schneier</strong>, Julia
        Evans, Dan Luu, hnRSS (HN links — not the blog itself).
      </p>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 12 }}>
        {EXAMPLE_FEEDS.map((f) => (
          <button
            key={f.id}
            type="button"
            title={`${f.focus} — ${f.url}`}
            onClick={() => setUrl(f.url)}
            style={{
              padding: "4px 10px",
              borderRadius: 999,
              border: url === f.url ? "1px solid #5a8fd8" : "1px solid #444",
              background: url === f.url ? "rgba(80,120,200,.2)" : "#1f2430",
              color: "#d8dce6",
              fontSize: 12,
              cursor: "pointer",
            }}
          >
            {f.title}
          </button>
        ))}
      </div>
      <label style={{ display: "block", marginBottom: 8 }}>
        Feed URL
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            width: "100%",
            marginTop: 4,
            padding: 8,
            borderRadius: 6,
            border: "1px solid #333",
            background: "#1a1e26",
            color: "#fff",
          }}
        />
      </label>
      <p style={{ margin: "0 0 12px", fontSize: 12, opacity: 0.8 }}>
        Raw feeds show XML in the browser — use a reader instead:{" "}
        <a href={feedlySubscribeUrl(url)} target="_blank" rel="noopener noreferrer" style={{ color: "#8ec5ff" }}>
          Feedly
        </a>
        {" · "}
        <a
          href={inoreaderSubscribeUrl(url)}
          target="_blank"
          rel="noopener noreferrer"
          style={{ color: "#8ec5ff" }}
        >
          Inoreader
        </a>
      </p>
      <button
        type="button"
        disabled={busy}
        onClick={() => void fetchFeed()}
        style={{ padding: "8px 16px", borderRadius: 8, cursor: busy ? "wait" : "pointer" }}
      >
        Fetch
      </button>

      {data && (
        <div style={{ marginTop: 20 }}>
          {data.success === false && (
            <p style={{ color: "#f88" }}>{data.error ?? "Request failed."}</p>
          )}
          {data.success !== false && feedTitle && (
            <h2 style={{ fontSize: "1.1rem", margin: "0 0 12px", fontWeight: 600 }}>{feedTitle}</h2>
          )}
          {entries.length > 0 && (
            <ol
              style={{
                margin: 0,
                paddingLeft: 22,
                display: "flex",
                flexDirection: "column",
                gap: 12,
              }}
            >
              {entries.map((e, i) => (
                <li key={`${e.link ?? ""}-${i}`} style={{ lineHeight: 1.4 }}>
                  {e.link ? (
                    <a
                      href={e.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: "#8ec5ff", fontWeight: 500, fontSize: "1.02rem" }}
                    >
                      {e.title?.trim() || "(untitled)"}
                    </a>
                  ) : (
                    <span>{e.title?.trim() || "(no link)"}</span>
                  )}
                  {e.published && (
                    <div style={{ fontSize: 12, opacity: 0.65, marginTop: 2 }}>{e.published}</div>
                  )}
                </li>
              ))}
            </ol>
          )}
          {data.success && entries.length === 0 && (
            <p style={{ opacity: 0.75 }}>No entries in this response.</p>
          )}
          <details style={{ marginTop: 16 }}>
            <summary style={{ cursor: "pointer", opacity: 0.75, fontSize: 13 }}>Raw JSON</summary>
            <pre
              style={{
                marginTop: 8,
                padding: 12,
                borderRadius: 8,
                background: "#151922",
                border: "1px solid #2a3140",
                overflow: "auto",
                maxHeight: 240,
                fontSize: 11,
              }}
            >
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </section>
  );
}

type ResolveHop = {
  hop?: number;
  url?: string;
  status_code?: number | null;
  location?: string | null;
  error?: string;
};

type ResolveJson = {
  success?: boolean;
  message?: string;
  chain?: ResolveHop[];
  final_url?: string;
  error?: string;
};

function ResolvePanel() {
  const [url, setUrl] = useState("https://xkcd.com/");
  const [method, setMethod] = useState<"head" | "get">("head");
  const [busy, setBusy] = useState(false);
  const [data, setData] = useState<ResolveJson | null>(null);

  const run = useCallback(async () => {
    setBusy(true);
    setData(null);
    try {
      const r = await fetch("/api/resolve/trace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url,
          max_hops: 15,
          timeout_seconds: 20,
          method,
        }),
      });
      setData((await r.json()) as ResolveJson);
    } catch (e) {
      setData({ success: false, error: String(e) });
    } finally {
      setBusy(false);
    }
  }, [url, method]);

  const chain = data?.chain ?? [];

  return (
    <section>
      <label style={{ display: "block", marginBottom: 8 }}>
        URL
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            width: "100%",
            marginTop: 4,
            padding: 8,
            borderRadius: 6,
            border: "1px solid #333",
            background: "#1a1e26",
            color: "#fff",
          }}
        />
      </label>
      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 12, flexWrap: "wrap" }}>
        <label style={{ fontSize: 14 }}>
          Method{" "}
          <select
            value={method}
            onChange={(e) => setMethod(e.target.value as "head" | "get")}
            style={{ marginLeft: 6, padding: 6, borderRadius: 6, background: "#1a1e26", color: "#fff" }}
          >
            <option value="head">HEAD</option>
            <option value="get">GET</option>
          </select>
        </label>
        <button
          type="button"
          disabled={busy}
          onClick={() => void run()}
          style={{ padding: "8px 16px", borderRadius: 8, cursor: busy ? "wait" : "pointer" }}
        >
          Trace
        </button>
      </div>

      {data && (
        <div style={{ marginTop: 8 }}>
          {data.error && !chain.length && <p style={{ color: "#f88" }}>{data.error}</p>}
          {chain.length > 0 && (
            <ol style={{ paddingLeft: 20, margin: 0, display: "flex", flexDirection: "column", gap: 10 }}>
              {chain.map((h, i) => (
                <li key={`${h.url}-${i}`} style={{ lineHeight: 1.45 }}>
                  <a
                    href={h.url || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: "#8ec5ff", wordBreak: "break-all" }}
                  >
                    {h.url}
                  </a>
                  <span style={{ opacity: 0.75, marginLeft: 8 }}>
                    {h.status_code != null ? `· ${h.status_code}` : ""}
                  </span>
                  {h.location && (
                    <div style={{ fontSize: 12, opacity: 0.7, marginTop: 4 }}>
                      → Location: {h.location}
                    </div>
                  )}
                  {h.error && <div style={{ fontSize: 12, color: "#f88" }}>{h.error}</div>}
                </li>
              ))}
            </ol>
          )}
          {data.final_url && (
            <p style={{ marginTop: 12, fontSize: 14 }}>
              <strong>Final:</strong>{" "}
              <a href={data.final_url} target="_blank" rel="noopener noreferrer" style={{ color: "#8ec5ff" }}>
                {data.final_url}
              </a>
            </p>
          )}
          <details style={{ marginTop: 16 }}>
            <summary style={{ cursor: "pointer", opacity: 0.75, fontSize: 13 }}>Raw JSON</summary>
            <pre
              style={{
                marginTop: 8,
                padding: 12,
                borderRadius: 8,
                background: "#151922",
                border: "1px solid #2a3140",
                overflow: "auto",
                maxHeight: 220,
                fontSize: 11,
              }}
            >
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </section>
  );
}

type OpmlFeed = { title?: string; xmlUrl?: string; htmlUrl?: string; type?: string };
type OpmlJson = { success?: boolean; feeds?: OpmlFeed[]; error?: string; message?: string };

function OpmlPanel() {
  const [xml, setXml] = useState(`<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0"><head><title>Example</title></head><body>
<outline text="SW" type="rss" xmlUrl="https://simonwillison.net/atom/everything/" htmlUrl="https://simonwillison.net/"/>
</body></opml>`);
  const [busy, setBusy] = useState(false);
  const [data, setData] = useState<OpmlJson | null>(null);

  const run = useCallback(async () => {
    setBusy(true);
    setData(null);
    try {
      const r = await fetch("/api/opml/feeds", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opml_xml: xml }),
      });
      setData((await r.json()) as OpmlJson);
    } catch (e) {
      setData({ success: false, error: String(e) });
    } finally {
      setBusy(false);
    }
  }, [xml]);

  const feeds = data?.feeds ?? [];

  return (
    <section>
      <p style={{ opacity: 0.85, marginTop: 0 }}>
        Paste OPML from a reader export. Each row links to the <strong>feed URL</strong> (xmlUrl).
      </p>
      <textarea
        value={xml}
        onChange={(e) => setXml(e.target.value)}
        rows={8}
        style={{
          width: "100%",
          padding: 8,
          borderRadius: 8,
          fontFamily: "ui-monospace, monospace",
          fontSize: 12,
          background: "#1a1e26",
          color: "#e8eaef",
          border: "1px solid #333",
        }}
      />
      <button
        type="button"
        disabled={busy}
        onClick={() => void run()}
        style={{ marginTop: 10, padding: "8px 16px", borderRadius: 8, cursor: busy ? "wait" : "pointer" }}
      >
        Parse feeds
      </button>

      {data && (
        <div style={{ marginTop: 18 }}>
          {data.success === false && data.error && <p style={{ color: "#f88" }}>{data.error}</p>}
          {feeds.length > 0 && (
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 8 }}>
              {feeds.map((f, i) => (
                <li key={`${f.xmlUrl}-${i}`}>
                  <a
                    href={f.xmlUrl || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: "#8ec5ff", fontWeight: 500 }}
                  >
                    {f.title?.trim() || f.xmlUrl || "(feed)"}
                  </a>
                  {f.htmlUrl && (
                    <span style={{ fontSize: 12, opacity: 0.65, marginLeft: 8 }}>
                      · site:{" "}
                      <a href={f.htmlUrl} target="_blank" rel="noopener noreferrer" style={{ color: "#9ab" }}>
                        link
                      </a>
                    </span>
                  )}
                </li>
              ))}
            </ul>
          )}
          <details style={{ marginTop: 16 }}>
            <summary style={{ cursor: "pointer", opacity: 0.75, fontSize: 13 }}>Raw JSON</summary>
            <pre
              style={{
                marginTop: 8,
                padding: 12,
                borderRadius: 8,
                background: "#151922",
                border: "1px solid #2a3140",
                overflow: "auto",
                maxHeight: 200,
                fontSize: 11,
              }}
            >
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </section>
  );
}

function WeatherPanel({
  busy,
  onRun,
}: {
  busy: boolean;
  onRun: (p: string, b: unknown) => void;
}) {
  const [lat, setLat] = useState("48.2082");
  const [lon, setLon] = useState("16.3738");
  return (
    <section>
      <p style={{ opacity: 0.85, marginTop: 0 }}>WGS84 coordinates → Open-Meteo (HTTPS, no key).</p>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <label>
          Latitude
          <input
            value={lat}
            onChange={(e) => setLat(e.target.value)}
            style={{ display: "block", marginTop: 4, padding: 8, width: 140 }}
          />
        </label>
        <label>
          Longitude
          <input
            value={lon}
            onChange={(e) => setLon(e.target.value)}
            style={{ display: "block", marginTop: 4, padding: 8, width: 140 }}
          />
        </label>
      </div>
      <button
        type="button"
        disabled={busy}
        style={{ marginTop: 12, padding: "8px 16px", borderRadius: 8, cursor: busy ? "wait" : "pointer" }}
        onClick={() =>
          onRun("/api/weather/forecast", {
            latitude: parseFloat(lat),
            longitude: parseFloat(lon),
            timezone: "auto",
            forecast_days: 3,
          })
        }
      >
        Forecast
      </button>
    </section>
  );
}

type ProbeRow = {
  url?: string;
  ok?: boolean;
  status_code?: number | null;
  elapsed_ms?: number | null;
  error?: string;
};

type ProbeJson = {
  success?: boolean;
  message?: string;
  results?: ProbeRow[];
  error?: string;
};

function ProbePanel() {
  const [text, setText] = useState(
    "http://127.0.0.1:10776/health\nhttp://127.0.0.1:10746/health",
  );
  const [busy, setBusy] = useState(false);
  const [data, setData] = useState<ProbeJson | null>(null);

  const runProbe = useCallback(async () => {
    setBusy(true);
    setData(null);
    const urls = text
      .split("\n")
      .map((s) => s.trim())
      .filter(Boolean);
    try {
      const r = await fetch("/api/probe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          urls,
          timeout_seconds: 5,
          max_concurrency: 8,
        }),
      });
      setData((await r.json()) as ProbeJson);
    } catch (e) {
      setData({ success: false, error: String(e) });
    } finally {
      setBusy(false);
    }
  }, [text]);

  const rows = data?.results ?? [];

  return (
    <section>
      <p style={{ opacity: 0.85, marginTop: 0 }}>
        One URL per line — parallel GET (localhost + LAN OK; metadata IPs blocked). Click a URL to open it.
      </p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={5}
        style={{
          width: "100%",
          padding: 8,
          borderRadius: 8,
          fontFamily: "ui-monospace, monospace",
          background: "#1a1e26",
          color: "#e8eaef",
          border: "1px solid #333",
        }}
      />
      <button
        type="button"
        disabled={busy}
        style={{ marginTop: 12, padding: "8px 16px", borderRadius: 8, cursor: busy ? "wait" : "pointer" }}
        onClick={() => void runProbe()}
      >
        Probe
      </button>

      {data && (
        <div style={{ marginTop: 20 }}>
          {data.success === false && data.error && (
            <p style={{ color: "#f88" }}>{data.error}</p>
          )}
          {rows.length > 0 && (
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 10 }}>
              {rows.map((row, i) => (
                <li
                  key={`${row.url}-${i}`}
                  style={{
                    padding: "10px 12px",
                    borderRadius: 8,
                    background: "#151922",
                    border: "1px solid #2a3140",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
                    {row.url ? (
                      <a
                        href={row.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: "#8ec5ff", wordBreak: "break-all" }}
                      >
                        {row.url}
                      </a>
                    ) : (
                      <span>(no url)</span>
                    )}
                    <span
                      style={{
                        fontSize: 12,
                        padding: "2px 8px",
                        borderRadius: 4,
                        background: row.ok ? "rgba(60,140,80,.35)" : "rgba(180,60,60,.35)",
                      }}
                    >
                      {row.ok ? "OK" : "FAIL"}{" "}
                      {row.status_code != null ? `· ${row.status_code}` : ""}
                      {row.elapsed_ms != null ? ` · ${row.elapsed_ms}ms` : ""}
                    </span>
                  </div>
                  {row.error && (
                    <div style={{ fontSize: 12, color: "#f99", marginTop: 6 }}>{row.error}</div>
                  )}
                </li>
              ))}
            </ul>
          )}
          <details style={{ marginTop: 16 }}>
            <summary style={{ cursor: "pointer", opacity: 0.75, fontSize: 13 }}>Raw JSON</summary>
            <pre
              style={{
                marginTop: 8,
                padding: 12,
                borderRadius: 8,
                background: "#151922",
                border: "1px solid #2a3140",
                overflow: "auto",
                maxHeight: 240,
                fontSize: 11,
              }}
            >
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </section>
  );
}
