import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';
import { KpiCard, MetricRow, ChartContainer } from './UI';
import { formatGhs } from '../utils/helpers';
import type { BalanceSheetData } from '../types';

const ASSET_COLORS = ['#E8760A', '#D4600A', '#FFB347', '#F59E0B'];

interface BalanceSheetTabProps {
  balanceSheet: BalanceSheetData;
  selectedYears: number[];
}

export function BalanceSheetTab({ balanceSheet, selectedYears }: BalanceSheetTabProps) {
  const bs = balanceSheet.balance_sheet.annual;
  const ratios = balanceSheet.balance_sheet.key_ratios;
  const availableYears = selectedYears.filter((y) => bs[String(y)]);
  const latestYear = String(Math.max(...availableYears));
  const yearsForBar = availableYears.map(String);

  const latestBs = bs[latestYear];
  const totalAssetsGrowth = ((latestBs.assets.total_assets / bs['2023'].assets.total_assets) - 1) * 100;
  const totalEquityGrowth = ((latestBs.equity.total_equity / bs['2023'].equity.total_equity) - 1) * 100;
  const workingCapitalChange = ((ratios[latestYear].working_capital / ratios['2023'].working_capital) - 1) * 100;
  const deImprovement = ((ratios['2023'].debt_to_equity - ratios[latestYear].debt_to_equity) / ratios['2023'].debt_to_equity) * 100;

  const assetComposition = [
    { name: 'Current Assets', value: latestBs.assets.current_assets.total_current_assets },
    { name: 'Net PPE', value: latestBs.assets.non_current_assets.net_ppe },
    { name: 'Intangibles', value: latestBs.assets.non_current_assets.intangible_assets },
    { name: 'Long-term Investments', value: latestBs.assets.non_current_assets.long_term_investments },
  ];

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Balance Sheet</h2>
        <p className="text-text-secondary">Assets, liabilities, equity positions and financial health</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard icon="🏦" label="Total Assets" value={formatGhs(latestBs.assets.total_assets)} delta={`${totalAssetsGrowth.toFixed(1)}% since 2023`} />
        <KpiCard icon="💎" label="Total Equity" value={formatGhs(latestBs.equity.total_equity)} delta={`${totalEquityGrowth.toFixed(1)}% growth`} />
        <KpiCard icon="💵" label="Working Capital" value={formatGhs(ratios[latestYear].working_capital)} delta={`+${workingCapitalChange.toFixed(1)}%`} />
        <KpiCard icon="📊" label="Debt/Equity" value={ratios[latestYear].debt_to_equity.toFixed(2)} delta={`-${deImprovement.toFixed(1)}%`} />
      </div>

      <ChartContainer title="Balance Sheet Evolution" className="mb-4">
        <ResponsiveContainer width="100%" height={340}>
          <BarChart data={yearsForBar}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: unknown) => formatGhs(Number(v))} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
            <Legend />
            <Bar name="Assets" dataKey={(d: string) => bs[d]?.assets.total_assets ?? 0} fill="#E8760A" />
            <Bar name="Liabilities" dataKey={(d: string) => bs[d]?.liabilities.total_liabilities ?? 0} fill="#EF4444" />
            <Bar name="Equity" dataKey={(d: string) => bs[d]?.equity.total_equity ?? 0} fill="#F59E0B" />
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title={`Asset Composition (${latestYear})`}>
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={assetComposition}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={3}
                dataKey="value"
                label={(entry: unknown) => {
                  const e = entry as { name: string; percent: number | undefined };
                  return `${e.name} ${((e.percent ?? 0) * 100).toFixed(0)}%`;
                }}
              >
                {ASSET_COLORS.map((color, i) => (
                  <Cell key={i} fill={color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Liquidity Trends">
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip />
              <Legend />
              <Line name="Current Ratio" dataKey={(d: string) => ratios[d]?.current_ratio ?? 0} stroke="#E8760A" strokeWidth={3} />
              <Line name="Quick Ratio" dataKey={(d: string) => ratios[d]?.quick_ratio ?? 0} stroke="#D4600A" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <ChartContainer title="Detailed Balance Sheet">
        <div className="space-y-2">
          <MetricRow label="Cash & Equivalents" value={formatGhs(latestBs.assets.current_assets.cash_and_equivalents)} />
          <MetricRow label="Accounts Receivable" value={formatGhs(latestBs.assets.current_assets.accounts_receivable)} />
          <MetricRow label="Inventory" value={formatGhs(latestBs.assets.current_assets.inventory)} />
          <MetricRow label="Net PPE" value={formatGhs(latestBs.assets.non_current_assets.net_ppe)} />
          <MetricRow label="Long-term Debt" value={formatGhs(latestBs.liabilities.non_current_liabilities.long_term_debt)} />
        </div>
      </ChartContainer>
    </div>
  );
}
