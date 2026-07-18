import Icon from '@/components/atoms/Icon';

export default function TopKPIs({ netSentiment, totalReviews, summaries, aiConfidence }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-sm md:gap-md">
      <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col gap-xs relative overflow-hidden">
        <div className="absolute top-0 right-0 p-sm text-primary-container">
          <Icon name="thumbs_up_down" />
        </div>
        <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Net Sentiment</span>
        <span className="font-headline-lg-mobile md:font-headline-lg text-primary">{netSentiment > 0 ? '+' : ''}{netSentiment.toFixed(1)}</span>
        <div className="flex items-center gap-xs text-tertiary-fixed-dim font-label-sm text-label-sm mt-auto">
          <Icon name="arrow_upward" className="text-[16px]" /> 5.2% vs last week
        </div>
      </div>
      <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col gap-xs relative overflow-hidden">
        <div className="absolute top-0 right-0 p-sm text-secondary-fixed">
          <Icon name="speed" />
        </div>
        <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Velocity Score</span>
        <span className="font-headline-lg-mobile md:font-headline-lg text-secondary-fixed">{(totalReviews * 1.2).toFixed(1)}k</span>
        <div className="flex items-center gap-xs text-tertiary-fixed-dim font-label-sm text-label-sm mt-auto">
          <Icon name="arrow_upward" className="text-[16px]" /> {((totalReviews / 100) * 4).toFixed(1)}% spike
        </div>
      </div>
      <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col gap-xs relative overflow-hidden">
        <div className="absolute top-0 right-0 p-sm text-error">
          <Icon name="warning" />
        </div>
        <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Clustered Mentions</span>
        <span className="font-headline-lg-mobile md:font-headline-lg text-error">{summaries.reduce((acc, s) => acc + s.review_count, 0)}</span>
        <div className="flex items-center gap-xs text-error-container font-label-sm text-label-sm mt-auto">
          <Icon name="insights" className="text-[16px]" /> Top topics
        </div>
      </div>
      <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col gap-xs relative overflow-hidden border border-primary-container/30">
        <div className="absolute inset-0 bg-primary-container/5"></div>
        <div className="absolute top-0 right-0 p-sm text-primary-container">
          <Icon name="insights" filled />
        </div>
        <span className="font-label-sm text-label-sm text-primary-container uppercase tracking-wider z-10">AI Confidence</span>
        <span className="font-headline-lg-mobile md:font-headline-lg text-on-surface z-10">{aiConfidence}%</span>
        <div className="flex items-center gap-xs text-on-surface-variant font-label-sm text-label-sm mt-auto z-10">
          Based on {totalReviews} recent inputs
        </div>
      </div>
    </div>
  );
}
