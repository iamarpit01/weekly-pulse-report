import Icon from '@/components/atoms/Icon';
import DashboardLayout from '@/components/templates/DashboardLayout';
import TopKPIs from '@/components/organisms/TopKPIs';
import CriticalVerbatims from '@/components/organisms/CriticalVerbatims';
import RatingDistribution from '@/components/organisms/RatingDistribution';
import ClusterTable from '@/components/organisms/ClusterTable';

export default function DashboardPage({ data }) {
  const summaries = data?.summaries || [];
  const totalReviews = data?.total_reviews || 0;
  const isoWeek = data?.iso_week || 'Unknown';
  const ratingDistribution = data?.rating_distribution || { '5': 0, '4': 0, '3': 0, '2': 0, '1': 0 };
  const averageRating = data?.average_rating || 0;
  const netSentiment = data?.net_sentiment || 0;
  const aiConfidence = data?.ai_confidence || 0;

  return (
    <DashboardLayout isoWeek={isoWeek}>
      {/* Context Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-sm gap-sm">
        <div>
          <h2 className="font-headline-md font-semibold text-on-surface">Sentiment Analytics</h2>
          <p className="font-body-md text-on-surface-variant mt-base">High-level review breakdown & velocity analysis for {isoWeek}.</p>
        </div>
        <div className="flex gap-xs">
          <span className="bg-surface-container-high text-on-surface-variant border border-outline-variant px-sm py-base rounded font-label-sm text-label-sm flex items-center gap-xs glass-panel">
            <Icon name="android" className="text-[14px]" /> Google Play Store
          </span>
          <span className="bg-secondary-container/20 text-secondary-fixed border border-secondary-container/50 px-sm py-base rounded font-label-sm text-label-sm flex items-center gap-xs glass-panel">
            <Icon name="auto_awesome" className="text-[14px]" /> Groq Llama-3
          </span>
        </div>
      </div>
      
      {/* Top Row KPIs */}
      <TopKPIs netSentiment={netSentiment} totalReviews={totalReviews} summaries={summaries} aiConfidence={aiConfidence} />
      
      {/* Bento Grid Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-sm md:gap-md h-auto lg:h-[400px]">
        <CriticalVerbatims summaries={summaries} />
        <RatingDistribution ratingDistribution={ratingDistribution} totalReviews={totalReviews} averageRating={averageRating} />
      </div>
      
      {/* Bottom Data Table / Heatmap */}
      <ClusterTable summaries={summaries} totalReviews={totalReviews} />
    </DashboardLayout>
  );
}
