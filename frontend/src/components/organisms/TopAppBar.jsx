import Icon from '@/components/atoms/Icon';

export default function TopAppBar() {
  return (
    <header className="bg-surface dark:bg-surface-container-low border-b border-outline-variant dark:border-outline flex justify-between items-center px-lg py-sm w-full z-50 sticky top-0 h-[72px]">
      <div className="flex items-center gap-md md:hidden">
        <Icon name="menu" className="text-primary text-[28px]" />
      </div>
      <div className="flex-1 md:flex-none">
      </div>
      <div className="flex items-center gap-sm">
        <button className="flex items-center justify-center w-10 h-10 rounded-full text-on-surface-variant hover:text-primary dark:hover:text-primary-fixed transition-colors relative">
          <Icon name="notifications" />
          <span className="absolute top-2 right-2 w-2 h-2 bg-error rounded-full"></span>
        </button>
        <div className="h-8 w-px bg-outline-variant mx-xs hidden md:block"></div>
        <a href="https://docs.google.com/document/d/1rPEPm1u_srbs9IXnfvZ5snFPKIyFipt7ra8YRYLWjHM/export?format=pdf" target="_blank" rel="noopener noreferrer" className="hidden md:flex bg-transparent border border-secondary-container text-secondary-fixed hover:bg-secondary-container/20 py-xs px-sm rounded-lg font-label-sm text-label-sm transition-colors items-center gap-xs">
          Export PDF
          <Icon name="download" className="text-[16px]" />
        </a>
        <div className="w-10 h-10 rounded-full bg-surface-container-highest border border-outline-variant overflow-hidden ml-xs">
          <img className="w-full h-full object-cover" data-alt="Avatar" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBEtwoGvBPnX91R0ec5cuuotAUFurbCQs5E-AQ8XiLlYisAHlOzr5ulBC7MlmOSeP6uiXrEBhHQMt_HzLlhhZcVjR580bjSimWXz2FbGq9y68F1k7nTkA3aFClcfHF5YdDegt_ZK_5eWMP8ZIyH1xYQsedta29S_qJX3huOIgXamRy9avTbXH-aSGQUbue7hPGRXTVRS1aj0FCFrQmWBn3H32FaxA0oX_zCgC7xHb7tFSFMSJ7LfA6w" />
        </div>
      </div>
    </header>
  );
}
