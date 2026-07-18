import Icon from '@/components/atoms/Icon';

export default function ClusterTable({ summaries, totalReviews }) {
  return (
    <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col mt-xs mb-lg">
      <div className="flex justify-between items-center mb-md">
        <h3 className="font-headline-md font-semibold text-on-surface flex items-center gap-xs">
          <Icon name="bug_report" className="text-error text-[18px]" />
          AI Detected Clusters
        </h3>
        <button className="text-primary font-label-sm text-label-sm hover:underline">View All Clusters</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[600px]">
          <thead>
            <tr className="border-b border-outline-variant/50 text-on-surface-variant font-label-sm text-label-sm">
              <th className="pb-xs font-normal">Cluster Topic</th>
              <th className="pb-xs font-normal">Volume</th>
              <th className="pb-xs font-normal">Severity</th>
              <th className="pb-xs font-normal">Trend</th>
              <th className="pb-xs font-normal text-right">Action</th>
            </tr>
          </thead>
          <tbody className="text-body-md">
            {summaries.map((summary, idx) => (
              <tr key={idx} className="border-b border-outline-variant/20 hover:bg-surface-container/30 transition-colors">
                <td className="py-sm">
                  <div className="flex items-center gap-xs">
                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                    <span className="font-semibold text-primary">{summary.theme_name}</span>
                  </div>
                </td>
                <td className="py-sm font-label-sm">{summary.review_count}</td>
                <td className="py-sm">
                  <div className="w-16 h-1.5 bg-surface-container rounded-full overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: `${Math.min(100, (summary.review_count / totalReviews) * 500)}%` }}></div>
                  </div>
                </td>
                <td className="py-sm text-primary font-label-sm text-label-sm flex items-center gap-1">
                  <Icon name="insights" className="text-[14px]" /> Automated
                </td>
                <td className="py-sm text-right">
                  <button className="bg-transparent border border-outline text-on-surface hover:border-primary hover:text-primary px-2 py-1 rounded text-label-sm font-label-sm transition-colors" onClick={() => alert(summary.actionable_ideas.join('\n'))}>
                    Ideas
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
