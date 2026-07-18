export default function VerbatimItem({ author, quote }) {
  return (
    <div className="bg-error/5 border border-error/20 rounded-lg p-sm hover:border-error/50 transition-colors">
      <div className="flex justify-between items-start mb-xs">
        <div className="flex items-center gap-xs">
          <span className="font-label-sm text-label-sm text-error">{author}</span>
          <span className="text-[10px] text-on-surface-variant opacity-60">• Recent</span>
        </div>
        <span className="bg-error text-on-error text-[10px] px-2 py-0.5 rounded-full font-bold uppercase">CRITICAL</span>
      </div>
      <p className="text-body-md text-on-surface font-semibold text-[14px] leading-relaxed italic">"{quote}"</p>
    </div>
  );
}
