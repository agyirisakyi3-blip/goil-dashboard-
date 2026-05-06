import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  AreaChart,
  Area,
} from 'recharts';
import { KpiCard, ProgressBar, MetricRow, ChartContainer } from './UI';
import { formatGhs } from '../utils/helpers';
import type { CashFlowData, RevenueData, ExpenseData } from '../types';

interface CashFlowTabProps {
  cashFlow: CashFlowData;
  revenue: RevenueData;
  expenses: ExpenseData;
  selectedYears: number[];
}

export function CashFlowTab({ cashFlow, revenue, expenses, selectedYears }: CashFlowTabProps) {
  const cfSummary = cashFlow.cash_flow.annual_summary;
  const revSummary = revenue.revenue.annual_summary;
  const expSummary = expenses.expenses.annual_summary;
  const availableYears = selectedYears.filter((y) => cfSummary[String(y)]);
  const latestYear = String(Math.max(...availableYears));
  const yearsForBar = availableYears.map(String);

  const quarterlyData = cashFlow.cash_flow.quarterly;

  const operatingCfMargin = (cfSummary[latestYear].net_cash_from_operations / revSummary[latestYear].total_revenue) * 100;
  const fcfConversion = (cfSummary[latestYear].free_cash_flow / cfSummary[latestYear].net_cash_from_operations) * 100;
  const capexRevenue = (Math.abs(cfSummary[latestYear].capex) / revSummary[latestYear].total_revenue) * 100;
  const netProfit = revSummary[latestYear].total_revenue - expSummary[latestYear].total_expenses;
  const cashConversion = (cfSummary[latestYear].net_cash_from_operations / netProfit) * 100;

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Cash Flow Analysis</h2>
        <p className="text-text-secondary">Operating, investing, and financing cash movements</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <KpiCard
          icon="💵"
          label="Operating CF"
          value={formatGhs(cfSummary[latestYear].net_cash_from_operations)}
          delta={`+${((cfSummary[latestYear].net_cash_from_operations / cfSummary['2023'].net_cash_from_operations - 1) * 100).toFixed(1)}% vs 2023`}
        />
        <KpiCard
          icon="📈"
          label="Free Cash Flow"
          value={formatGhs(cfSummary[latestYear].free_cash_flow)}
          delta={`+${((cfSummary[latestYear].free_cash_flow / cfSummary['2023'].free_cash_flow - 1) * 100).toFixed(1)}% vs 2023`}
        />
        <KpiCard icon="🏗️" label="CapEx" value={formatGhs(Math.abs(cfSummary[latestYear].capex))} delta="Investing in Growth" />
      </div>

      <ChartContainer title="Cash Flow Components" className="mb-4">
        <ResponsiveContainer width="100%" height={340}>
          <BarChart data={yearsForBar}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey={(d) => d} stroke="#94A3B8" />
            <YAxis stroke="#94A3B8" tickFormatter={(v: number) => formatGhs(v)} />
            <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
            <Legend />
            <Bar name="Operating" dataKey={(d: string) => cfSummary[d]?.net_cash_from_operations ?? 0} fill="#E8760A" />
            <Bar name="Investing" dataKey={(d: string) => cfSummary[d]?.net_cash_from_investing ?? 0} fill="#EF4444" />
            <Bar name="Financing" dataKey={(d: string) => cfSummary[d]?.net_cash_from_financing ?? 0} fill="#D4600A" />
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title="Free Cash Flow Growth">
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: unknown) => formatGhs(Number(v))} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
              <Area
                name="Free Cash Flow"
                dataKey={(d: string) => cfSummary[d]?.free_cash_flow ?? 0}
                stroke="#F59E0B"
                strokeWidth={3}
                fill="rgba(245, 158, 11, 0.15)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Quarterly Free Cash Flow">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={quarterlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="quarter" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: unknown) => formatGhs(Number(v))} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
              <Bar dataKey="free_cash_flow" name="Quarterly FCF" fill="#E8760A" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <ChartContainer title="Cash Flow Health Check">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div>
            <ProgressBar label="Operating CF Margin" value={operatingCfMargin} maxValue={20} />
            <ProgressBar label="FCF Conversion" value={fcfConversion} maxValue={100} />
          </div>
          <div className="space-y-2">
            <MetricRow label="Dividends Paid" value={formatGhs(cfSummary[latestYear].dividends_paid)} badgeText="Consistent" badgeType="info" />
            <MetricRow label="Debt Reduction" value={formatGhs(Math.abs(cfSummary[latestYear].net_cash_from_financing))} badgeText="Active" badgeType="success" />
          </div>
          <div className="space-y-2">
            <MetricRow label="CapEx / Revenue" value={`${capexRevenue.toFixed(1)}%`} badgeText="Reinvesting" badgeType="info" />
            <MetricRow label="Cash Conversion" value={`${cashConversion.toFixed(1)}%`} badgeText="Strong" badgeType="success" />
          </div>
        </div>
      </ChartContainer>
    </div>
  );
}
