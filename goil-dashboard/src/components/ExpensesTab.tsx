import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { KpiCard, ProgressBar, MetricRow, ChartContainer } from './UI';
import { formatGhs } from '../utils/helpers';
import type { ExpenseData, RevenueData } from '../types';

const EXPENSE_COLORS = ['#EF4444', '#D4600A', '#F59E0B', '#FFB347', '#E8760A', '#06B6D4', '#A855F7', '#64748B'];

interface ExpensesTabProps {
  expenses: ExpenseData;
  revenue: RevenueData;
  selectedYears: number[];
}

export function ExpensesTab({ expenses, revenue, selectedYears }: ExpensesTabProps) {
  const expSummary = expenses.expenses.annual_summary;
  const revSummary = revenue.revenue.annual_summary;
  const availableYears = selectedYears.filter((y) => expSummary[String(y)]);
  const latestYear = String(Math.max(...availableYears));

  const quarterlyData = expenses.expenses.quarterly;

  const expenseCategories = [
    { key: 'cost_of_goods_sold', label: 'COGS' },
    { key: 'employee_costs', label: 'Employee Costs' },
    { key: 'transport_logistics', label: 'Transport' },
    { key: 'marketing_advertising', label: 'Marketing' },
    { key: 'maintenance_repairs', label: 'Maintenance' },
    { key: 'utilities', label: 'Utilities' },
    { key: 'depreciation', label: 'Depreciation' },
    { key: 'other_expenses', label: 'Other' },
  ];

  const pieData = expenseCategories.map((cat) => ({
    name: cat.label,
    value: expSummary[latestYear][cat.key as keyof typeof expSummary['2023']] ?? 0,
  }));

  const profit = (revSummary[latestYear]?.total_revenue ?? 0) - (expSummary[latestYear]?.total_expenses ?? 0);
  const interestExpense = expSummary[latestYear]?.interest_expense ?? 1;
  const interestCoverage = profit / interestExpense;
  const taxRate = profit > 0 ? (expSummary[latestYear]?.taxes_levies ?? 0) / profit * 100 : 0;

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Expense Management</h2>
        <p className="text-text-secondary">Track and analyze cost structure and spending patterns</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          icon="💸"
          label="Total Expenses"
          value={formatGhs(expSummary[latestYear].total_expenses)}
          delta={`${((expSummary[latestYear].total_expenses / revSummary[latestYear].total_revenue) * 100).toFixed(1)}% of Revenue`}
        />
        <KpiCard
          icon="🏭"
          label="COGS"
          value={formatGhs(expSummary[latestYear].cost_of_goods_sold)}
          delta={`${expSummary[latestYear].cogs_percentage.toFixed(1)}%`}
        />
        <KpiCard
          icon="👥"
          label="Employee Costs"
          value={formatGhs(expSummary[latestYear].employee_costs)}
          delta={`${((expSummary[latestYear].employee_costs / expSummary[latestYear].total_expenses) * 100).toFixed(1)}% of OpEx`}
        />
        <KpiCard
          icon="📦"
          label="OPEX"
          value={formatGhs(expSummary[latestYear].total_expenses - expSummary[latestYear].cost_of_goods_sold)}
          delta={`${expSummary[latestYear].opex_percentage.toFixed(1)}%`}
        />
      </div>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title={`Expense Breakdown (${latestYear})`}>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={110}
                paddingAngle={3}
                dataKey="value"
                label={(entry: unknown) => {
                  const e = entry as { name: string; percent: number | undefined };
                  return `${e.name} ${((e.percent ?? 0) * 100).toFixed(0)}%`;
                }}
              >
                {EXPENSE_COLORS.map((color, i) => (
                  <Cell key={i} fill={color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Expense Trends">
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={quarterlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="quarter" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: unknown) => formatGhs(Number(v))} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
              <Legend />
              <Line type="monotone" dataKey="total_expenses" name="Total" stroke="#EF4444" strokeWidth={3} />
              <Line type="monotone" dataKey="cost_of_goods_sold" name="COGS" stroke="#F59E0B" strokeWidth={2} />
              <Line type="monotone" dataKey="employee_costs" name="Employees" stroke="#D4600A" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <ChartContainer title="Expense Efficiency Metrics" className="mb-4">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div>
            <ProgressBar label="COGS Efficiency" value={100 - (expSummary[latestYear]?.cogs_percentage ?? 0)} maxValue={100} />
            <ProgressBar label="OpEx Control" value={100 - (expSummary[latestYear]?.opex_percentage ?? 0)} maxValue={100} />
          </div>
          <div>
            <ProgressBar
              label="Marketing ROI"
              value={expSummary[latestYear]?.marketing_advertising > 0 ? (revSummary[latestYear]?.total_revenue ?? 0) / expSummary[latestYear].marketing_advertising : 0}
              maxValue={50}
            />
            <ProgressBar
              label="Admin Efficiency"
              value={expSummary[latestYear]?.total_expenses > 0 ? (expSummary[latestYear].administrative / expSummary[latestYear].total_expenses) * 100 : 0}
              maxValue={100}
            />
          </div>
          <div className="space-y-2">
            <MetricRow label="Interest Coverage" value={`${interestCoverage.toFixed(1)}x`} badgeText="Healthy" badgeType="success" />
            <MetricRow label="Tax Rate" value={`${taxRate.toFixed(1)}%`} badgeText="Normal" badgeType="info" />
          </div>
        </div>
      </ChartContainer>
    </div>
  );
}
