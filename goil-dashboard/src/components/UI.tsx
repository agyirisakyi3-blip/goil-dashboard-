import { motion, type Variants } from 'framer-motion';
import type { ReactNode } from 'react';

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.1,
      duration: 0.5,
    },
  }),
};

const hoverScale = { scale: 1.02 };
const tapScale = { scale: 0.98 };

interface KpiCardProps {
  icon: string;
  label: string;
  value: string;
  delta?: string;
  deltaType?: 'positive' | 'negative';
  index?: number;
}

export function KpiCard({ icon, label, value, delta, deltaType = 'positive', index = 0 }: KpiCardProps) {
  return (
    <motion.div
      custom={index}
      initial="hidden"
      animate="visible"
      variants={cardVariants}
      whileHover={hoverScale}
      whileTap={tapScale}
      className="group relative overflow-hidden rounded-2xl border border-card-border bg-card-bg p-6 backdrop-blur-xl transition-all duration-500 hover:border-primary/50 hover:shadow-2xl hover:shadow-primary/20"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: index * 0.1 + 0.3, type: 'spring', stiffness: 200 }}
        className="mb-3 text-3xl"
      >
        {icon}
      </motion.div>

      <div className="mb-2 text-xs font-semibold uppercase tracking-widest text-text-muted">
        {label}
      </div>

      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: index * 0.1 + 0.4 }}
        className="mb-3 bg-gradient-to-r from-text-primary to-text-secondary bg-clip-text text-3xl font-bold text-transparent"
      >
        {value}
      </motion.div>

      {delta && (
        <motion.span
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.1 + 0.5 }}
          className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-bold ${
            deltaType === 'positive'
              ? 'bg-emerald-500/20 text-emerald-400'
              : 'bg-red-500/20 text-red-400'
          }`}
        >
          {deltaType === 'positive' ? '↑' : '↓'} {delta}
        </motion.span>
      )}

      <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-primary/10 blur-2xl" />
    </motion.div>
  );
}

interface ProgressBarProps {
  label: string;
  value: number;
  maxValue: number;
  color?: string;
  index?: number;
}

export function ProgressBar({ label, value, maxValue, color, index = 0 }: ProgressBarProps) {
  const pct = Math.min(100, (value / maxValue) * 100);
  const barColor = color || 'from-primary to-secondary';

  return (
    <motion.div
      custom={index}
      initial="hidden"
      animate="visible"
      variants={cardVariants}
      className="mb-4 rounded-xl border border-card-border bg-card-bg p-4 backdrop-blur-xl"
    >
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm text-text-secondary">{label}</span>
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-sm font-bold text-text-primary"
        >
          {pct.toFixed(1)}%
        </motion.span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-bg-dark/50">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ delay: index * 0.1 + 0.3, duration: 1 }}
          className={`h-full rounded-full bg-gradient-to-r ${barColor} shadow-lg`}
          style={{ boxShadow: '0 0 10px rgba(232, 118, 10, 0.5)' }}
        />
      </div>
    </motion.div>
  );
}

interface MetricRowProps {
  label: string;
  value: string;
  badgeText?: string;
  badgeType?: 'success' | 'warning' | 'info';
  index?: number;
}

export function MetricRow({ label, value, badgeText, badgeType = 'info', index = 0 }: MetricRowProps) {
  const badgeClasses: Record<string, string> = {
    success: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    warning: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    info: 'bg-primary/20 text-primary border-primary/30',
  };

  return (
    <motion.div
      custom={index}
      initial="hidden"
      animate="visible"
      variants={cardVariants}
      whileHover={{ x: 5 }}
      className="flex items-center justify-between rounded-xl border border-card-border bg-card-bg px-5 py-3.5 backdrop-blur-xl transition-all duration-300 hover:border-primary/30 hover:bg-card-bg/80"
    >
      <span className="text-sm text-text-secondary">{label}</span>
      <div className="flex items-center gap-3">
        {badgeText && (
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300 }}
            className={`rounded-full border px-3 py-0.5 text-[10px] font-bold uppercase tracking-wider ${badgeClasses[badgeType]}`}
          >
            {badgeText}
          </motion.span>
        )}
        <span className="text-sm font-bold text-text-primary">{value}</span>
      </div>
    </motion.div>
  );
}

interface ChartContainerProps {
  title?: string;
  children: ReactNode;
  className?: string;
  delay?: number;
}

export function ChartContainer({ title, children, className = '', delay = 0 }: ChartContainerProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.6 }}
      whileHover={{ y: -2 }}
      className={`group relative overflow-hidden rounded-2xl border border-card-border bg-card-bg p-6 backdrop-blur-xl transition-all duration-500 hover:border-primary/30 hover:shadow-2xl hover:shadow-primary/10 ${className}`}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

      {title && (
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: delay + 0.2 }}
          className="mb-6 flex items-center gap-3"
        >
          <div className="h-1 w-6 rounded-full bg-gradient-to-r from-primary to-secondary" />
          <div className="text-lg font-bold text-text-primary">{title}</div>
        </motion.div>
      )}

      <div className="relative z-10">{children}</div>

      <div className="absolute -bottom-6 -right-6 h-32 w-32 rounded-full bg-primary/5 blur-3xl" />
    </motion.div>
  );
}

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  index?: number;
}

export function SectionHeader({ title, subtitle, index = 0 }: SectionHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      className="mb-6"
    >
      <h2 className="bg-gradient-to-r from-text-primary via-text-secondary to-text-primary bg-clip-text text-2xl font-bold text-transparent">
        {title}
      </h2>
      {subtitle && <p className="mt-1 text-sm text-text-muted">{subtitle}</p>}
      <div className="mt-3 h-px w-full bg-gradient-to-r from-primary/50 via-transparent to-transparent" />
    </motion.div>
  );
}

interface EmptyStateProps {
  message?: string;
  icon?: string;
}

export function EmptyState({ message = 'No data available', icon = '📊' }: EmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center justify-center rounded-2xl border border-card-border bg-card-bg p-12 text-center backdrop-blur-xl"
    >
      <div className="mb-4 text-6xl opacity-50">{icon}</div>
      <p className="text-text-muted">{message}</p>
    </motion.div>
  );
}
