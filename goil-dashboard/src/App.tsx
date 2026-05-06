import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sidebar } from './components/Sidebar';
import { OverviewTab } from './components/OverviewTab';
import { RevenueTab } from './components/RevenueTab';
import { ExpensesTab } from './components/ExpensesTab';
import { ProfitabilityTab } from './components/ProfitabilityTab';
import { FuelSalesTab } from './components/FuelSalesTab';
import { BalanceSheetTab } from './components/BalanceSheetTab';
import { CashFlowTab } from './components/CashFlowTab';
import { OperationsTab } from './components/OperationsTab';
import { RegionalTab } from './components/RegionalTab';
import { useDashboardData } from './hooks/useDashboardData';
import { Loader2, AlertTriangle } from 'lucide-react';

const tabIcons = ['📊', '💰', '📉', '📈', '⛽', '🏦', '💳', '⚙️', '🌍'];

function App() {
  const { revenue, expenses, fuel, ops, balanceSheet, cashFlow, loading, error } = useDashboardData();
  const [activeTab, setActiveTab] = useState(0);
  const [selectedYears, setSelectedYears] = useState<number[]>([2023, 2024, 2025]);
  const [selectedQuarters, setSelectedQuarters] = useState<string[]>(['Q1', 'Q2', 'Q3', 'Q4']);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const tabs = [
    'Overview',
    'Revenue',
    'Expenses',
    'Profitability',
    'Fuel Sales',
    'Balance Sheet',
    'Cash Flow',
    'Operations',
    'Regionals',
  ];

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg-dark">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
            className="mx-auto mb-6"
          >
            <Loader2 className="h-16 w-16 text-primary" />
          </motion.div>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-lg font-medium text-text-secondary"
          >
            Loading dashboard data...
          </motion.p>
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ duration: 2, repeat: Infinity }}
            className="mx-auto mt-4 h-1 w-48 rounded-full bg-gradient-to-r from-primary via-secondary to-primary"
          />
        </motion.div>
      </div>
    );
  }

  if (error || !revenue || !expenses || !fuel || !ops || !balanceSheet || !cashFlow) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg-dark">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <AlertTriangle className="mx-auto mb-4 h-16 w-16 text-danger" />
          <p className="text-lg text-text-secondary">{error || 'Failed to load dashboard data'}</p>
        </motion.div>
      </div>
    );
  }

  const tabContent = {
    0: <OverviewTab revenue={revenue} expenses={expenses} fuel={fuel} ops={ops} balanceSheet={balanceSheet} cashFlow={cashFlow} selectedYears={selectedYears} />,
    1: <RevenueTab revenue={revenue} selectedYears={selectedYears} />,
    2: <ExpensesTab expenses={expenses} revenue={revenue} selectedYears={selectedYears} />,
    3: <ProfitabilityTab ops={ops} revenue={revenue} expenses={expenses} selectedYears={selectedYears} />,
    4: <FuelSalesTab fuel={fuel} selectedYears={selectedYears} />,
    5: <BalanceSheetTab balanceSheet={balanceSheet} selectedYears={selectedYears} />,
    6: <CashFlowTab cashFlow={cashFlow} revenue={revenue} expenses={expenses} selectedYears={selectedYears} />,
    7: <OperationsTab ops={ops} selectedYears={selectedYears} />,
    8: <RegionalTab revenue={revenue} expenses={expenses} selectedYears={selectedYears} />,
  };

  return (
    <div className="flex min-h-screen bg-bg-dark">
      <Sidebar
        years={[2023, 2024, 2025]}
        selectedYears={selectedYears}
        onYearChange={setSelectedYears}
        quarters={['Q1', 'Q2', 'Q3', 'Q4']}
        selectedQuarters={selectedQuarters}
        onQuarterChange={setSelectedQuarters}
        isCollapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      <main className={`flex-1 overflow-auto relative ${sidebarCollapsed ? 'p-6' : 'p-8'}`}>
        {/* Animated background elements */}
        <div className="pointer-events-none fixed inset-0 overflow-hidden">
          <motion.div
            animate={{
              x: [0, 100, 0],
              y: [0, 50, 0],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
            className="absolute -right-40 -top-40 h-80 w-80 rounded-full bg-primary/5 blur-3xl"
          />
          <motion.div
            animate={{
              x: [0, -50, 0],
              y: [0, 100, 0],
              opacity: [0.2, 0.4, 0.2],
            }}
            transition={{ duration: 15, repeat: Infinity, ease: 'linear' }}
            className="absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-secondary/5 blur-3xl"
          />
          <motion.div
            animate={{
              x: [0, 80, 0],
              y: [0, -80, 0],
              opacity: [0.15, 0.3, 0.15],
            }}
            transition={{ duration: 18, repeat: Infinity, ease: 'linear' }}
            className="absolute left-1/2 top-1/2 h-64 w-64 -translate-x-1/2 -translate-y-1/2 rounded-full bg-accent/5 blur-3xl"
          />
        </div>
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8 flex items-center justify-between"
        >
          <div>
            <h1 className="bg-gradient-to-r from-text-primary via-primary to-secondary bg-clip-text text-3xl font-bold text-transparent">
              Financial Performance Dashboard
            </h1>
            <p className="mt-1 text-sm text-text-muted">
              Comprehensive analytics for Goil Ghana Limited • {Math.max(...selectedYears)}
            </p>
          </div>
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-2 rounded-full border border-primary/30 bg-gradient-to-r from-primary/10 to-secondary/10 px-4 py-2 text-sm text-primary backdrop-blur-xl"
          >
            <motion.div
              animate={{ scale: [1, 1.3, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="h-2 w-2 rounded-full bg-primary"
            />
            FY {Math.max(...selectedYears)}
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="mb-8 flex gap-2 overflow-x-auto pb-2"
        >
          {tabs.map((tab, index) => (
            <motion.button
              key={tab}
              onClick={() => setActiveTab(index)}
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.95 }}
              className={`whitespace-nowrap rounded-xl border px-5 py-2.5 text-xs font-bold uppercase tracking-wider transition-all duration-300 ${
                activeTab === index
                  ? 'border-primary bg-gradient-to-r from-primary to-secondary text-white shadow-lg shadow-primary/30'
                  : 'border-card-border bg-card-bg text-text-muted hover:border-primary/50 hover:text-text-primary'
              }`}
            >
              <span className="mr-2">{tabIcons[index]}</span>
              {tab}
            </motion.button>
          ))}
        </motion.div>

        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {tabContent[activeTab as keyof typeof tabContent]}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
