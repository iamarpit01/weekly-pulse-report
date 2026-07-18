export default function Icon({ name, className = "", filled = false }) {
  const style = filled ? { fontVariationSettings: "'FILL' 1" } : {};
  return (
    <span className={`material-symbols-outlined ${className}`} style={style}>
      {name}
    </span>
  );
}
