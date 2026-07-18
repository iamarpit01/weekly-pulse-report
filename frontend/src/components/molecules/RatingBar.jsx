export default function RatingBar({ star, pct }) {
  const isHigh = star >= 4;
  const isMed = star === 3;
  const colorClass = isHigh ? 'bg-primary' : (isMed ? 'bg-outline-variant' : 'bg-error');
  const textClass = isHigh ? 'text-primary' : (isMed ? 'text-on-surface-variant' : 'text-error');
  
  return (
    <div className="flex items-center gap-xs">
      <span className={`w-8 text-label-sm font-bold text-right ${textClass}`}>{star}★</span>
      <div className="flex-1 h-2 bg-surface-container-highest rounded-full overflow-hidden shadow-[inset_0_1px_2px_rgba(0,0,0,0.5)]">
        <div className={`h-full ${colorClass} rounded-full transition-all duration-500`} style={{ width: `${pct}%` }}></div>
      </div>
      <span className={`w-10 text-label-sm font-bold text-right ${textClass}`}>{Math.round(pct)}%</span>
    </div>
  );
}
