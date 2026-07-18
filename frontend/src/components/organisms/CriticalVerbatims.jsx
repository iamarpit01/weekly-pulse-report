import Icon from '@/components/atoms/Icon';
import Badge from '@/components/atoms/Badge';
import VerbatimItem from '@/components/molecules/VerbatimItem';

export default function CriticalVerbatims({ summaries }) {
  const quotes = summaries.slice(0, 5).flatMap(s => s.verbatim_quotes);
  
  return (
    <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col lg:col-span-2 h-full overflow-hidden">
      <div className="flex justify-between items-center mb-md">
        <h3 className="font-headline-md font-semibold text-on-surface flex items-center gap-xs">
          <Icon name="format_quote" className="text-error" />
          Critical Verbatims
        </h3>
        <div className="flex items-center gap-xs">
          <Badge>{quotes.length} CRITICAL ISSUES</Badge>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto pr-1 flex flex-col gap-sm custom-scrollbar">
        {quotes.map((q, idx) => (
          <VerbatimItem key={idx} author={q.author} quote={q.quote} />
        ))}
      </div>
    </div>
  );
}
