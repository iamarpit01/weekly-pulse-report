import Icon from '@/components/atoms/Icon';
import RatingBar from '@/components/molecules/RatingBar';

export default function RatingDistribution({ ratingDistribution, totalReviews, averageRating }) {
  return (
    <div className="glass-panel rounded-xl p-sm md:p-md flex flex-col h-full glass-panel-active">
      <div className="flex justify-between items-center mb-md">
        <h3 className="font-headline-md font-semibold text-on-surface flex items-center gap-xs">
          <Icon name="star_half" className="text-secondary-fixed text-[18px]" />
          Rating Distribution
        </h3>
      </div>
      <div className="flex-1 flex flex-col justify-center gap-sm">
        {[5, 4, 3, 2, 1].map(star => (
          <RatingBar key={star} star={star} pct={ratingDistribution[star.toString()] || 0} />
        ))}
      </div>
      <div className="mt-auto pt-sm border-t border-outline-variant/30 flex justify-between items-center text-label-sm font-label-sm text-on-surface-variant">
        <div className="flex flex-col gap-1 w-full">
          <div className="flex justify-between items-center">
            <span className="text-label-sm text-on-surface-variant opacity-80">Total Reviews Analyzed</span>
            <span className="text-label-sm font-bold text-on-surface">{totalReviews}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-label-sm text-on-surface-variant opacity-80">Average Rating</span>
            <span className="text-label-sm font-bold text-tertiary-fixed-dim flex items-center gap-1">
              {averageRating} <Icon name="star" className="text-[14px]" filled />
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
