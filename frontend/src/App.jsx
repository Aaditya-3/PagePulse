import { useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const EMPTY_VALUE = "Not available";

const formatMetricValue = (value) => {
  if (value === undefined || value === null || value === "") {
    return EMPTY_VALUE;
  }

  if (typeof value === "number") {
    return Number.isFinite(value) ? value.toLocaleString() : EMPTY_VALUE;
  }

  if (typeof value === "string") {
    return value;
  }

  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }

  return JSON.stringify(value);
};

const readMetric = (report, key) => {
  if (!report) {
    return EMPTY_VALUE;
  }

  return formatMetricValue(report[key]);
};

const formatResponseTime = (value) => {
  const milliseconds = Number(value);

  if (!Number.isFinite(milliseconds)) {
    return EMPTY_VALUE;
  }

  if (milliseconds >= 1000) {
    return `${(milliseconds / 1000).toFixed(2)} s`;
  }

  return `${Math.round(milliseconds)} ms`;
};

const formatMetaDescription = (value) => {
  if (typeof value !== "string" || !value.trim() || value === "No Description") {
    return "No meta description found.";
  }

  return value;
};

const formatErrorMessage = (detail) => {
  if (!detail) {
    return "The audit could not be completed.";
  }

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => item.msg || item.message || JSON.stringify(item))
      .join(" ");
  }

  return detail.message || JSON.stringify(detail);
};

const Header = () => (
  <header className="header">
    <h1>Page Pulse</h1>
    <p>Website Audit Console</p>
  </header>
);

const AuditForm = ({ url, isLoading, onSubmit, onUrlChange }) => (
  <form className="audit-form" onSubmit={onSubmit}>
    <label htmlFor="url">Website URL</label>
    <div className="form-control">
      <input
        id="url"
        type="text"
        value={url}
        onChange={(event) => onUrlChange(event.target.value)}
        placeholder="example.com"
        autoComplete="url"
        disabled={isLoading}
        autoFocus
      />
    </div>
    <button type="submit" disabled={isLoading}>
      {isLoading ? (
        <>
          <span className="button-spinner" aria-hidden="true" />
          Auditing...
        </>
      ) : (
        "Run Audit"
      )}
    </button>
  </form>
);

const EmptyState = () => (
  <section className="state-card">
    <p>Enter a website URL and click Run Audit.</p>
  </section>
);

const LoadingState = () => (
  <section className="state-card" role="status" aria-live="polite">
    <span className="spinner" aria-hidden="true" />
    <p>Auditing website...</p>
  </section>
);

const ErrorState = ({ message }) => (
  <section className="error-card" role="alert">
    <strong>Audit Failed</strong>
    <p>{message}</p>
  </section>
);

const MetricCard = ({ className = "", label, value, variant = "default" }) => (
  <article className={`metric-card ${className}`.trim()}>
    <span className="metric-label">{label}</span>
    <strong className={`metric-value metric-value-${variant}`}>{value}</strong>
  </article>
);

const ReportGrid = ({ report }) => {
  const status = Number(report.status);
  const statusVariant = Number.isFinite(status) && status >= 400 ? "danger" : "success";

  return (
    <section className="report-grid" aria-label="Audit report">
      <MetricCard
        label="🌐 HTTP Status"
        value={readMetric(report, "status")}
        variant={statusVariant}
      />
      <MetricCard
        label="⚡ Response Time"
        value={formatResponseTime(report.response_time_ms)}
      />
      <MetricCard label="🏷 H1 Count" value={readMetric(report, "h1_count")} />
      <MetricCard label="📚 Word Count" value={readMetric(report, "word_count")} />
      <MetricCard
        label="🖼 Missing Alt Images"
        value={readMetric(report, "images_missing_alt")}
      />
      <MetricCard
        label="📄 Page Title"
        value={readMetric(report, "title")}
        className="wide-card"
        variant="text"
      />
      <MetricCard
        label="Meta Description"
        value={formatMetaDescription(report.meta_description)}
        className="full-card"
        variant="text"
      />
    </section>
  );
};

const Footer = () => (
  <footer className="footer">
    Built for{" "}
    <a href="https://digitalheroesco.com" target="_blank" rel="noreferrer">
      Digital Heroes
    </a>{" "}
    Training Task
  </footer>
);

function App() {
  const [url, setUrl] = useState("");
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const runAudit = async (event) => {
    event.preventDefault();

    const targetUrl = url.trim();
    if (!targetUrl) {
      setError("Please enter a website URL.");
      setReport(null);
      return;
    }

    setError("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/audit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: targetUrl }),
      });

      let data = null;
      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        throw new Error(formatErrorMessage(data?.detail));
      }

      setReport(data && typeof data === "object" ? data : {});
    } catch (auditError) {
      setReport(null);
      setError(
        auditError instanceof Error
          ? auditError.message
          : "The audit could not be completed.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="app">
      <div className="container">
        <Header />
        <AuditForm
          url={url}
          isLoading={isLoading}
          onSubmit={runAudit}
          onUrlChange={setUrl}
        />

        <div className="result-area">
          {isLoading ? <LoadingState /> : null}
          {!isLoading && error ? <ErrorState message={error} /> : null}
          {!isLoading && !error && report ? <ReportGrid report={report} /> : null}
          {!isLoading && !error && !report ? <EmptyState /> : null}
        </div>

        <Footer />
      </div>
    </main>
  );
}

export default App;
