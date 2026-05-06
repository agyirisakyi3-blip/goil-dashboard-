import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  Legend,
} from 'recharts';
import { KpiCard, ProgressBar, MetricRow, ChartContainer } from './UI';
import { formatGhs } from '../utils/helpers';
import type { RevenueData, ExpenseData, FuelSalesVolume, OperationalData, BalanceSheetData, CashFlowData } from '../types';

const COLORS = ['#E8760A', '#F59E0B', '#D4600A', '#FFB347', '#EF4444'];

interface OverviewTabProps {
  revenue: RevenueData;
  expenses: ExpenseData;
  fuel: FuelSalesVolume;
  ops: OperationalData;
  balanceSheet: BalanceSheetData;
  cashFlow: CashFlowData;
  selectedYears: number[];
}

export function OverviewTab({ revenue, expenses, fuel, ops, selectedYears }: OverviewTabProps) {
  const revSummary = revenue.revenue.annual_summary;
  const expSummary = expenses.expenses.annual_summary;

  const latestYear = String(Math.max(...selectedYears.filter((y) => revSummary[String(y)])));

  const latestRev = revSummary[latestYear]?.total_revenue ?? 0;
  const latestExp = expSummary[latestYear]?.total_expenses ?? 0;
  const latestProfit = latestRev - latestExp;
  const latestMargin = latestRev > 0 ? (latestProfit / latestRev) * 100 : 0;
  const revGrowth = revSummary[latestYear]?.yoy_growth ?? 0;

  const stations = ops.operational_metrics.station_network[latestYear] ?? { total_stations: 0, operational_uptime_percent: 0, new_stations_opened: 0 };
  const fuelVol = fuel.fuel_sales_volume.annual_summary[latestYear] ?? { total_liters: 0 };
  const employees = ops.operational_metrics.employee_metrics[latestYear] ?? { total_employees: 0, safety_incidents: 0 };

  const quarterlyData = revenue.revenue.quarterly;
  const kpisQuarterly = ops.operational_metrics.kpis.quarterly;
  const latestKpi = kpisQuarterly.filter((k) => k.quarter.includes(latestYear)).slice(-1)[0] ?? null;

  const yearsForBar = ['2023', '2024', '2025'];

  const fmt = (v: unknown) => formatGhs(Number(v));

  return (
    <div>
      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        <KpiCard icon="💰" label="Total Revenue" value={formatGhs(latestRev)} delta={`${revGrowth.toFixed(1)}% YoY`} />
        <KpiCard icon="📈" label="Net Profit" value={formatGhs(latestProfit)} delta={`${latestMargin.toFixed(1)}% Margin`} />
        <KpiCard icon="💸" label="Total Expenses" value={formatGhs(latestExp)} delta={`${((latestExp / latestRev) * 100).toFixed(1)}% of Rev`} />
        <KpiCard icon="⛽" label="Stations" value={stations.total_stations.toLocaleString()} delta="+34 New Sites" />
        <KpiCard icon="🛢️" label="Fuel Volume" value={`${(fuelVol.total_liters / 1e9).toFixed(2)}B L`} delta="+19.1% YoY" />
        <KpiCard icon="👥" label="Employees" value={employees.total_employees.toLocaleString()} delta="+240 Added" />
      </div>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ChartContainer title="Revenue Trajectory">
            <ResponsiveContainer width="100%" height={320}>
              <AreaChart data={quarterlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="quarter" stroke="#94A3B8" />
                <YAxis stroke="#94A3B8" tickFormatter={fmt} />
                <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
                <Area type="monotone" dataKey="total_revenue" name="Total Revenue" stroke="#E8760A" fill="rgba(16,185,129,0.1)" strokeWidth={3} />
                <Area type="monotone" dataKey="fuel_sales" name="Fuel Sales" stroke="#F59E0B" fill="transparent" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </ChartContainer>
        </div>

        <ChartContainer title="Revenue Composition">
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Fuel Sales', value: revSummary[latestYear].fuel_sales },
                  { name: 'Lubricants', value: revSummary[latestYear].lubricants },
                  { name: 'Convenience', value: revSummary[latestYear].convenience_store },
                  { name: 'Fleet', value: revSummary[latestYear].fleet_services },
                  { name: 'Other', value: revSummary[latestYear].other_income },
                ]}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {COLORS.map((color, i) => (
                  <Cell key={i} fill={color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <ChartContainer title="P&L Comparison">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={fmt} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
              <Legend />
              <Bar name="Revenue" dataKey={(d: string) => revSummary[d]?.total_revenue ?? 0} fill="#E8760A" />
              <Bar name="Expenses" dataKey={(d: string) => expSummary[d]?.total_expenses ?? 0} fill="#EF4444" />
              <Bar name="Profit" dataKey={(d: string) => (revSummary[d]?.total_revenue ?? 0) - (expSummary[d]?.total_expenses ?? 0)} fill="#F59E0B" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Key Performance Indicators">
          <ProgressBar label="Gross Margin" value={latestKpi?.gross_profit_margin ?? 0} maxValue={100} />
          <ProgressBar label="Net Margin" value={latestKpi?.net_profit_margin ?? 0} maxValue={100} />
          <ProgressBar label="EBITDA Margin" value={latestKpi?.ebitda_margin ?? 0} maxValue={100} />
          <ProgressBar label="ROE" value={latestKpi?.return_on_equity ?? 0} maxValue={100} />
        </ChartContainer>

        <ChartContainer title="Quick Stats">
          <div className="space-y-2">
            <MetricRow label="Customer Satisfaction" value={`${(ops.operational_metrics.customer_metrics[latestYear]?.customer_satisfaction_score ?? 0).toFixed(1)}/100`} badgeText="Excellent" badgeType="success" />
            <MetricRow label="NPS Score" value={String(ops.operational_metrics.customer_metrics[latestYear]?.nps_score ?? 0)} badgeText="Strong" badgeType="success" />
            <MetricRow label="Station Uptime" value={`${(stations.operational_uptime_percent ?? 0).toFixed(1)}%`} badgeText="99%+" badgeType="success" />
            <MetricRow label="Inventory Turnover" value={`${latestKpi?.inventory_turnover ? latestKpi.inventory_turnover.toFixed(1) : '0'}x`} badgeText="Healthy" badgeType="info" />
            <MetricRow label="Safety Incidents" value={String(employees.safety_incidents ?? 0)} badgeText="Improving" badgeType="success" />
          </div>
        </ChartContainer>
      </div>
    </div>
  );
}
