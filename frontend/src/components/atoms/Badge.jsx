export default function Badge({ children, className = "" }) {
  return (
    <span className={`bg-error/20 text-error text-[10px] px-2 py-0.5 rounded-full border border-error/50 uppercase font-bold ${className}`}>
      {children}
    </span>
  );
}
