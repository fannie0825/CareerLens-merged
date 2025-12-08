import React, { useMemo, useState } from 'react';
import {
  Eye,
  FileText,
  LayoutDashboard,
  Menu,
  Settings,
  Target,
  X
} from 'lucide-react';

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'resume', label: 'Resume Analysis', icon: FileText },
  { id: 'market', label: 'Market Match', icon: Target },
  { id: 'settings', label: 'Settings', icon: Settings }
];

const metricCards = [
  {
    id: 'match-score',
    label: 'MATCH SCORE',
    value: '92%',
    description: 'Overall alignment',
    valueClass: 'text-[#377dff]'
  },
  {
    id: 'salary',
    label: 'EST. SALARY',
    value: 'HK$55k',
    description: 'Median offer range',
    valueClass: 'text-slate-900'
  },
  {
    id: 'skill-gaps',
    label: 'SKILL GAPS',
    value: '3',
    description: 'Key areas to upskill',
    valueClass: 'text-[#f04438]'
  }
];

const DashboardLayout = () => {
  const [activeNav, setActiveNav] = useState('dashboard');
  const [isNavOpen, setIsNavOpen] = useState(false);

  const activeLabel = useMemo(
    () => navItems.find((item) => item.id === activeNav)?.label ?? 'Dashboard',
    [activeNav]
  );

  const toggleNav = () => setIsNavOpen((prev) => !prev);
  const closeNav = () => setIsNavOpen(false);

  const handleNavClick = (id) => {
    setActiveNav(id);
    closeNav();
  };

  return (
    <div className="min-h-screen bg-[#f5f7fa] text-[#111827] flex font-['Inter']">
      {/* Backdrop for mobile navigation */}
      {isNavOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-30 lg:hidden"
          aria-hidden="true"
          onClick={closeNav}
        />
      )}

      {/* Sidebar Navigation */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-72 bg-[#1a2332] text-white flex flex-col shadow-2xl transform transition-transform duration-300 ease-out lg:static lg:translate-x-0 ${
          isNavOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="flex items-center justify-between px-6 pt-6 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-white/10 flex items-center justify-center">
              <Eye className="w-6 h-6 text-[#5cc5ff]" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-white/60">
                CareerLens
              </p>
              <p className="text-lg font-semibold text-white">Analytics</p>
            </div>
          </div>
          <button
            className="lg:hidden text-white/60 hover:text-white transition-colors"
            onClick={closeNav}
            aria-label="Close navigation"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <nav className="mt-4 flex-1 px-4 space-y-2">
          {navItems.map(({ id, label, icon: Icon }) => {
            const isActive = id === activeNav;
            return (
              <button
                key={id}
                onClick={() => handleNavClick(id)}
                className={`w-full flex items-center gap-4 px-4 py-3 rounded-2xl transition-all duration-200 text-left ${
                  isActive
                    ? 'bg-white/10 text-white shadow-[0_10px_30px_rgba(31,63,104,0.35)]'
                    : 'text-white/70 hover:text-white hover:bg-white/5'
                }`}
                aria-current={isActive ? 'page' : undefined}
              >
                <span
                  className={`w-10 h-10 rounded-2xl flex items-center justify-center transition-colors ${
                    isActive
                      ? 'bg-[#2f80ff]/20 text-[#58a2ff]'
                      : 'bg-white/5 text-white/70'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                </span>
                <span className="text-sm font-medium tracking-wide">
                  {label}
                </span>
              </button>
            );
          })}
        </nav>

        <div className="px-6 py-6">
          <div className="rounded-2xl bg-white/5 p-4 border border-white/10">
            <p className="text-xs uppercase tracking-[0.2em] text-white/60 mb-1">
              Active section
            </p>
            <p className="text-base font-semibold text-white">{activeLabel}</p>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Mobile Header */}
        <header className="lg:hidden flex items-center justify-between bg-[#1a2332] text-white px-5 py-4 shadow-lg">
          <div className="flex items-center gap-2">
            <Eye className="w-6 h-6 text-[#5cc5ff]" aria-hidden="true" />
            <span className="font-semibold">CareerLens</span>
          </div>
          <button
            onClick={toggleNav}
            className="p-2 rounded-xl bg-white/10"
            aria-label="Toggle navigation"
          >
            <Menu className="w-5 h-5" />
          </button>
        </header>

        <main className="flex-1 px-6 py-8 lg:px-12 lg:py-10 space-y-10">
          {/* Header Section */}
          <section className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#1a2332] to-[#2c3e50] text-white p-8 lg:p-10 shadow-xl">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-8">
              <div className="space-y-4 max-w-2xl">
                <p className="text-sm uppercase tracking-[0.35em] text-white/60">
                  CareerLens Insights
                </p>
                <p className="text-4xl font-semibold leading-tight">
                  Welcome back, Alex,
                </p>
                <p className="text-lg text-white/80">
                  Your market value has increased by 5% since last month.
                </p>
              </div>
              <div className="flex items-center justify-center">
                <div className="w-28 h-28 lg:w-32 lg:h-32 rounded-full border-4 border-white/20 bg-white/10 flex items-center justify-center">
                  <div className="w-24 h-24 lg:w-28 lg:h-28 rounded-full bg-gradient-to-b from-white/40 to-white/10 backdrop-blur flex items-center justify-center text-white/60 text-sm">
                    Avatar
                  </div>
                </div>
              </div>
            </div>
            <div className="absolute inset-0 pointer-events-none opacity-50">
              <div className="absolute -right-16 top-10 w-48 h-48 rounded-full border border-white/10" />
              <div className="absolute -right-4 top-16 w-28 h-28 rounded-full border border-white/10" />
            </div>
          </section>

          {/* Recent Activity */}
          <section>
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-6 gap-2">
              <div>
                <p className="text-sm uppercase tracking-[0.4em] text-slate-400">
                  Dashboard
                </p>
                <h2 className="text-2xl font-semibold text-[#1f2a37]">
                  Recent Activity
                </h2>
              </div>
              <p className="text-sm text-slate-500">
                Last updated <span className="font-semibold text-slate-700">2 mins ago</span>
              </p>
            </div>
            <div className="grid gap-5 md:grid-cols-3">
              {metricCards.map(({ id, label, value, description, valueClass }) => (
                <article
                  key={id}
                  className="bg-white rounded-2xl p-6 shadow-sm border border-white hover:-translate-y-1 hover:shadow-xl transition duration-300 ease-out"
                >
                  <p className="text-xs font-semibold tracking-[0.35em] text-slate-400">
                    {label}
                  </p>
                  <p className={`mt-3 text-4xl font-semibold ${valueClass}`}>
                    {value}
                  </p>
                  <p className="mt-4 text-sm text-slate-500">{description}</p>
                </article>
              ))}
            </div>
          </section>

          {/* Chart Placeholder */}
          <section>
            <div className="rounded-3xl border border-dashed border-slate-200 bg-white h-80 flex flex-col items-center justify-center text-slate-400 text-lg shadow-inner">
              <p className="font-medium">Chart Area / Data Visualization</p>
              <p className="text-sm text-slate-300 mt-2">
                Upload insights or plug in your preferred analytics source
              </p>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
