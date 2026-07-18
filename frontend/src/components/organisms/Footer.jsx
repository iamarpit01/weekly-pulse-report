export default function Footer({ isoWeek }) {
  return (
    <footer className="bg-surface-bright dark:bg-surface-dim border-t border-outline-variant dark:border-outline w-full py-lg mt-auto z-10 relative">
      <div className="max-w-[1600px] mx-auto px-gutter flex flex-col md:flex-row justify-between items-center gap-sm">
        <span className="font-label-md text-label-md text-on-surface-variant">Groww Internal Pulse • {isoWeek}</span>
        <div className="flex gap-md">
          <span className="font-label-md text-label-md text-secondary dark:text-on-secondary-container hover:text-primary transition-colors opacity-80 cursor-pointer">Delivery ID: 99281</span>
          <span className="font-label-md text-label-md text-secondary dark:text-on-secondary-container hover:text-primary transition-colors opacity-80 cursor-pointer">Timestamp: 2023-10-24 10:00 UTC</span>
        </div>
      </div>
    </footer>
  );
}
