export function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-bg-dark">
      <div className="text-center">
        <div className="mb-4 text-8xl font-bold text-text-muted">404</div>
        <h1 className="mb-2 text-3xl font-bold text-text-primary">Page Not Found</h1>
        <p className="mb-6 text-text-secondary">The page you're looking for doesn't exist.</p>
        <button
          onClick={() => window.location.href = '/'}
          className="rounded-lg bg-primary px-6 py-3 font-semibold text-white transition-colors hover:bg-primary/80"
        >
          Go to Dashboard
        </button>
      </div>
    </div>
  );
}
