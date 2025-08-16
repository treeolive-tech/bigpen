export default function Loading() {
  return (
    <div
      // Fullscreen container
      className="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-body"
      style={{ zIndex: 9999 }}
    >
      {/* Keyframes definition */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>

      {/* Custom spinner */}
      <div
        style={{
          width: "60px",
          height: "60px",
          border: "6px solid var(--bs-primary)",
          borderTopColor:
            "color-mix(in srgb, var(--bs-primary), transparent 90%)",
          borderRadius: "50%",
          animation: "spin 1s linear infinite",
        }}
      />
    </div>
  );
}
