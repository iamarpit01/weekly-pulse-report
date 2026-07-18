import Sidebar from '@/components/organisms/Sidebar';
import TopAppBar from '@/components/organisms/TopAppBar';
import Footer from '@/components/organisms/Footer';

export default function DashboardLayout({ children, isoWeek }) {
  return (
    <div className="bg-background text-on-background font-body-md min-h-screen flex flex-col md:flex-row antialiased selection:bg-primary-container selection:text-on-primary-container">
      <Sidebar />
      <main className="flex-1 flex flex-col md:ml-64 w-full relative">
        <TopAppBar />
        <div className="p-margin-mobile md:p-margin-desktop flex-1 flex flex-col gap-md max-w-[1600px] mx-auto w-full">
          {children}
        </div>
        <Footer isoWeek={isoWeek} />
      </main>
    </div>
  );
}
