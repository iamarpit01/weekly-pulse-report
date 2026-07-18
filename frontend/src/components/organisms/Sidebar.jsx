import Icon from '@/components/atoms/Icon';

export default function Sidebar() {
  return (
    <nav className="hidden md:flex flex-col h-screen left-0 top-0 w-64 bg-surface-container-lowest border-r border-outline-variant/30 p-md gap-sm fixed z-40">
      <div className="flex items-center gap-sm mb-lg">
        <div className="w-10 h-10 rounded bg-primary-container flex items-center justify-center">
          <Icon name="insights" className="text-on-primary-container" filled />
        </div>
        <div>
          <h1 className="font-headline-lg text-headline-lg font-bold text-primary text-[22px] leading-tight tracking-wide drop-shadow-md">Weekly Pulse</h1>
          <p className="font-label-sm text-label-sm text-on-surface-variant">Product Insights</p>
        </div>
      </div>
      <div className="flex-1 flex flex-col gap-base">
        <a className="flex items-center gap-sm px-sm py-xs rounded-lg bg-primary text-on-primary font-bold font-label-sm text-label-sm shadow-[0_0_15px_rgba(0,219,233,0.3)]" href="#">
          <Icon name="hourglass_empty" className="text-[20px]" /> Current Week
        </a>
        <a className="flex items-center gap-sm px-sm py-xs rounded-lg hover:bg-surface-container-high transition-colors font-label-sm text-label-sm font-semibold text-primary" href="#">
          <Icon name="trending_up" className="text-[20px]" /> Trend Analysis
        </a>
        <a className="flex items-center gap-sm px-sm py-xs rounded-lg hover:bg-surface-container-high transition-colors font-label-sm text-label-sm font-semibold text-primary" href="#">
          <Icon name="bookmark" className="text-[20px]" /> Saved Insights
        </a>
      </div>
      <div className="mt-auto flex flex-col gap-base border-t border-outline-variant pt-sm">
        <a className="flex items-center gap-sm px-sm py-xs rounded-lg hover:bg-surface-container-high transition-colors font-label-sm text-label-sm text-on-surface font-semibold text-primary" href="#">
          <Icon name="settings" className="text-[20px]" /> Settings
        </a>
        <a className="flex items-center gap-sm px-sm py-xs rounded-lg hover:bg-surface-container-high transition-colors font-label-sm text-label-sm text-on-surface font-semibold text-primary" href="#">
          <Icon name="help" className="text-[20px]" /> Help
        </a>
      </div>
    </nav>
  );
}
