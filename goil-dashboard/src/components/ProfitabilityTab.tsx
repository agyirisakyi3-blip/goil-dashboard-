import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { KpiCard, ChartContainer } from './UI';
import { formatGhs } from '../utils/helpers';
import type { OperationalData, RevenueData, ExpenseData } from '../types';

interface ProfitabilityTabProps {
  ops: OperationalData;
  revenue: RevenueData;
  expenses: ExpenseData;
  selectedYears: number[];
}

export function ProfitabilityTab({ ops, revenue, expenses, selectedYears }: ProfitabilityTabProps) {
  const kpisQuarterly = ops.operational_metrics.kpis.quarterly;
  const revSummary = revenue.revenue.annual_summary;
  const expSummary = expenses.expenses.annual_summary;
  const availableYears = selectedYears.filter((y) => revSummary[String(y)]);
  const latestYear = String(Math.max(...availableYears));

  const latestKpi = kpisQuarterly.filter((k) => k.quarter.includes(latestYear)).slice(-1)[0] ?? null;

  const yearsForBar = availableYears.map(String);

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Profitability Analysis</h2>
        <p className="text-text-secondary">Margins, returns, and profitability metrics across periods</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard icon="📊" label="Gross Margin" value={`${(latestKpi?.gross_profit_margin ?? 0).toFixed(1)}%`} delta="+3.3 pts from 2023" />
        <KpiCard icon="💰" label="Net Margin" value={`${(latestKpi?.net_profit_margin ?? 0).toFixed(1)}%`} delta="+2.4 pts from 2023" />
        <KpiCard icon="📈" label="EBITDA Margin" value={`${(latestKpi?.ebitda_margin ?? 0).toFixed(1)}%`} delta="+2.7 pts from 2023" />
        <KpiCard icon="🏦" label="ROE" value={`${(latestKpi?.return_on_equity ?? 0).toFixed(1)}%`} delta="+4.4 pts from 2023" />
      </div>

      <ChartContainer title="Margin Expansion Over Time" className="mb-4">
        <ResponsiveContainer width="100%" height={340}>
          <LineChart data={kpisQuarterly}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="quarter" stroke="#94A3B8" />
            <YAxis stroke="#94A3B8" tickFormatter={(v: number) => `${v}%`} />
            <Tooltip formatter={(value: unknown) => `${Number(value).toFixed(1)}%`} />
            <Legend />
            <Line type="monotone" dataKey="gross_profit_margin" name="Gross Margin" stroke="#E8760A" strokeWidth={3} />
            <Line type="monotone" dataKey="ebitda_margin" name="EBITDA Margin" stroke="#F59E0B" strokeWidth={3} />
            <Line type="monotone" dataKey="net_profit_margin" name="Net Margin" stroke="#D4600A" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title="Annual Profit Layers">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: number) => formatGhs(v)} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
              <Legend />
              <Bar
                name="Gross Profit"
                dataKey={(d: string) => (revSummary[d]?.total_revenue ?? 0) - (expSummary[d]?.cost_of_goods_sold ?? 0)}
                fill="#E8760A"
              />
              <Bar
                name="Operating Profit"
                dataKey={(d: string) =>
                  (revSummary[d]?.total_revenue ?? 0) - (expSummary[d]?.total_expenses ?? 0) + (expSummary[d]?.interest_expense ?? 0) + (expSummary[d]?.depreciation ?? 0)
                }
                fill="#F59E0B"
              />
              <Bar
                name="Net Profit"
                dataKey={(d: string) => (revSummary[d]?.total_revenue ?? 0) - (expSummary[d]?.total_expenses ?? 0)}
                fill="#D4600A"
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Returns vs Target">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={kpisQuarterly}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="quarter" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: number) => `${v}%`} />
            <Tooltip formatter={(value: unknown) => `${Number(value).toFixed(1)}%`} />
              <Legend />
              <Line type="monotone" dataKey="return_on_equity" name="ROE" stroke="#FFB347" strokeWidth={3} />
              <Line type="monotone" dataKey="return_on_assets" name="ROA" stroke="#EF4444" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>
    </div>
  );
}
