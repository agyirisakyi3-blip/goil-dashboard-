import { useState } from 'react';
import { motion, AnimatePresence, type Variants } from 'framer-motion';
import { Fuel, Calendar, ChevronUp, Activity, BarChart3, ChevronLeft, ChevronRight } from 'lucide-react';

interface SidebarProps {
  years: number[];
  selectedYears: number[];
  onYearChange: (years: number[]) => void;
  quarters: string[];
  selectedQuarters: string[];
  onQuarterChange: (quarters: string[]) => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
}

const sidebarVariants: Variants = {
  hidden: { x: -50, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: { duration: 0.5 },
  },
};

const itemVariants: Variants = {
  hidden: { x: -20, opacity: 0 },
  visible: (i: number) => ({
    x: 0,
    opacity: 1,
    transition: { delay: i * 0.1, duration: 0.3 },
  }),
};

export function Sidebar({
  years,
  selectedYears,
  onYearChange,
  quarters,
  selectedQuarters,
  onQuarterChange,
  isCollapsed,
  onToggleCollapse,
}: SidebarProps) {
  const [openSection, setOpenSection] = useState<string | null>('years');

  const toggleSection = (section: string) => {
    setOpenSection((prev) => (prev === section ? null : section));
  };

  const toggleYear = (year: number) => {
    if (selectedYears.includes(year)) {
      if (selectedYears.length > 1) onYearChange(selectedYears.filter((y) => y !== year));
    } else {
      onYearChange([...selectedYears, year]);
    }
  };

  const toggleQuarter = (q: string) => {
    if (selectedQuarters.includes(q)) {
      if (selectedQuarters.length > 1) onQuarterChange(selectedQuarters.filter((x) => x !== q));
    } else {
      onQuarterChange([...selectedQuarters, q]);
    }
  };

  return (
    <motion.aside
      variants={sidebarVariants}
      initial="hidden"
      animate="visible"
      className={`flex h-full ${isCollapsed ? 'w-16' : 'w-64'} flex-col border-r border-card-border bg-gradient-to-b from-bg-dark via-[#1A1A1A] to-bg-dark backdrop-blur-xl transition-all duration-300 relative ${isCollapsed ? 'items-center p-2' : 'p-4'}`}
    >
      <motion.button
        onClick={onToggleCollapse}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="absolute -right-3 top-8 z-10 flex h-6 w-6 items-center justify-center rounded-full border border-card-border bg-bg-dark text-primary shadow-lg hover:bg-primary hover:text-white transition-colors"
      >
        <motion.div
          animate={{ rotate: isCollapsed ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          {isCollapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
        </motion.div>
      </motion.button>

      <AnimatePresence mode="wait">
        {!isCollapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              className="mb-6 text-center"
            >
              <div className="mb-3 flex items-center justify-center">
                <div className="relative">
                  <Fuel className="h-10 w-10 text-primary" />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="absolute -right-1 -top-1 h-3 w-3 rounded-full bg-primary"
                  />
                </div>
              </div>
              <div className="bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-2xl font-bold text-transparent">
                GOIL GHANA
              </div>
              <div className="mt-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-text-muted">
                Financial Dashboard
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {isCollapsed && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="mb-6 flex justify-center"
        >
          <Fuel className="h-8 w-8 text-primary" />
        </motion.div>
      )}

      <AnimatePresence mode="wait">
        {!isCollapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="flex-1 overflow-y-auto"
          >
            <div className="mb-4 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />

            <motion.div
              custom={0}
              variants={itemVariants}
              initial="hidden"
              animate="visible"
              className="mb-2 flex items-center justify-between cursor-pointer"
              onClick={() => toggleSection('years')}
            >
              <span className="text-[10px] font-bold uppercase tracking-widest text-text-muted">
                Time Period
              </span>
              <motion.div
                animate={{ rotate: openSection === 'years' ? 180 : 0 }}
                transition={{ duration: 0.3 }}
              >
                <ChevronUp size={14} className="text-text-muted" />
              </motion.div>
            </motion.div>

            <AnimatePresence>
              {openSection === 'years' && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="mb-4 space-y-1.5 overflow-hidden"
                >
                  {years.map((year, i) => (
                    <motion.button
                      key={year}
                      custom={i}
                      variants={itemVariants}
                      initial="hidden"
                      animate="visible"
                      onClick={() => toggleYear(year)}
                      whileHover={{ x: 5 }}
                      whileTap={{ scale: 0.95 }}
                      className={`flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-xs font-semibold transition-all duration-300 ${
                        selectedYears.includes(year)
                          ? 'bg-gradient-to-r from-primary/20 to-primary/5 text-primary shadow-lg shadow-primary/10'
                          : 'text-text-muted hover:bg-card-bg hover:text-text-primary'
                      }`}
                    >
                      <Calendar size={12} />
                      {year}
                      {selectedYears.includes(year) && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="ml-auto h-1.5 w-1.5 rounded-full bg-primary"
                        />
                      )}
                    </motion.button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>

            <motion.div
              custom={1}
              variants={itemVariants}
              initial="hidden"
              animate="visible"
              className="mb-2 mt-4 flex items-center justify-between cursor-pointer"
              onClick={() => toggleSection('quarters')}
            >
              <span className="text-[10px] font-bold uppercase tracking-widest text-text-muted">
                Quarters
              </span>
              <motion.div
                animate={{ rotate: openSection === 'quarters' ? 180 : 0 }}
                transition={{ duration: 0.3 }}
              >
                <ChevronUp size={14} className="text-text-muted" />
              </motion.div>
            </motion.div>

            <AnimatePresence>
              {openSection === 'quarters' && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="mb-4 space-y-1.5 overflow-hidden"
                >
                  {quarters.map((q, i) => (
                    <motion.button
                      key={q}
                      custom={i}
                      variants={itemVariants}
                      initial="hidden"
                      animate="visible"
                      onClick={() => toggleQuarter(q)}
                      whileHover={{ x: 5 }}
                      whileTap={{ scale: 0.95 }}
                      className={`flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-xs font-semibold transition-all duration-300 ${
                        selectedQuarters.includes(q)
                          ? 'bg-gradient-to-r from-accent/20 to-accent/5 text-accent shadow-lg shadow-accent/10'
                          : 'text-text-muted hover:bg-card-bg hover:text-text-primary'
                      }`}
                    >
                      <BarChart3 size={12} />
                      {q}
                      {selectedQuarters.includes(q) && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          className="ml-auto h-1.5 w-1.5 rounded-full bg-accent"
                        />
                      )}
                    </motion.button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>

            <div className="mb-4 h-px bg-gradient-to-r from-transparent via-card-border to-transparent" />

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="mb-4 flex items-center gap-2 rounded-xl border border-primary/20 bg-primary/5 px-4 py-2.5 backdrop-blur-xl"
            >
              <motion.div
                animate={{ scale: [1, 1.3, 1] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                <Activity size={14} className="text-primary" />
              </motion.div>
              <span className="text-xs font-semibold text-primary">Live Data</span>
            </motion.div>

            <div className="h-px bg-gradient-to-r from-transparent via-card-border to-transparent" />

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
              className="mt-auto space-y-1 text-center text-[10px] text-text-muted"
            >
              <div>
                Currency:{' '}
                <span className="font-bold text-text-primary">GHS (₵)</span>
              </div>
              <div>
                Last Updated:{' '}
                <span className="text-text-primary">
                  {new Date().toLocaleDateString('en-US', {
                    month: 'short',
                    day: '2-digit',
                    year: 'numeric',
                  })}
                </span>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.aside>
  );
}
