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
  LineChart,
  Line,
} from 'recharts';
import { KpiCard, ChartContainer } from './UI';
import type { OperationalData } from '../types';

interface OperationsTabProps {
  ops: OperationalData;
  selectedYears: number[];
}

export function OperationsTab({ ops, selectedYears }: OperationsTabProps) {
  const stations = ops.operational_metrics.station_network;
  const employees = ops.operational_metrics.employee_metrics;
  const customers = ops.operational_metrics.customer_metrics;
  const availableYears = selectedYears.filter((y) => stations[String(y)]);
  const latestYear = String(Math.max(...availableYears));
  const yearsForBar = availableYears.map(String);

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Operations Dashboard</h2>
        <p className="text-text-secondary">Station network, workforce, customer metrics, and safety</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          icon="⛽"
          label="Total Stations"
          value={stations[latestYear].total_stations.toLocaleString()}
          delta={`+${stations[latestYear].new_stations_opened} new`}
        />
        <KpiCard icon="⏱️" label="Uptime" value={`${stations[latestYear].operational_uptime_percent.toFixed(1)}%`} delta="Excellent" />
        <KpiCard
          icon="😊"
          label="Satisfaction"
          value={`${customers[latestYear].customer_satisfaction_score.toFixed(1)}/100`}
          delta="+5.3 pts"
        />
        <KpiCard icon="🎯" label="NPS Score" value={String(customers[latestYear].nps_score)} delta="+10 pts" />
      </div>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title="Station Network Growth">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip />
              <Legend />
              <Bar name="Company Owned" dataKey={(d: string) => stations[d]?.company_owned ?? 0} stackId="a" fill="#E8760A" />
              <Bar name="Dealer Owned" dataKey={(d: string) => stations[d]?.dealer_owned ?? 0} stackId="a" fill="#F59E0B" />
              <Bar name="Franchise" dataKey={(d: string) => stations[d]?.franchise ?? 0} stackId="a" fill="#D4600A" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Employee Growth">
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip formatter={(value: unknown) => Number(value).toLocaleString()} />
              <Area
                name="Employees"
                dataKey={(d: string) => employees[d]?.total_employees ?? 0}
                stroke="#E8760A"
                strokeWidth={3}
                fill="rgba(232, 118, 10, 0.1)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title="Customer Metrics">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip />
              <Legend />
              <Line name="Satisfaction" dataKey={(d: string) => customers[d]?.customer_satisfaction_score ?? 0} stroke="#E8760A" strokeWidth={3} />
              <Line name="NPS" dataKey={(d: string) => customers[d]?.nps_score ?? 0} stroke="#F59E0B" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="rounded-xl border border-card-border bg-card-bg/50 p-4">
              <div className="text-sm text-text-secondary">Active Customers</div>
              <div className="text-2xl font-bold text-text-primary">{customers[latestYear].loyalty_program_members.toLocaleString()}</div>
            </div>
            <div className="rounded-xl border border-card-border bg-card-bg/50 p-4">
              <div className="text-sm text-text-secondary">Fleet Accounts</div>
              <div className="text-2xl font-bold text-text-primary">{customers[latestYear].active_fleet_accounts.toLocaleString()}</div>
            </div>
          </div>
        </ChartContainer>

        <ChartContainer title="Safety & Workforce">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={yearsForBar}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={(d) => d} stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip />
              <Legend />
              <Bar name="Safety Incidents" dataKey={(d: string) => employees[d]?.safety_incidents ?? 0} fill="#EF4444" />
              <Bar name="Training Hours/Employee" dataKey={(d: string) => employees[d]?.training_hours_per_employee ?? 0} fill="#D4600A" />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="rounded-xl border border-card-border bg-card-bg/50 p-4">
              <div className="text-sm text-text-secondary">Avg Salary</div>
              <div className="text-2xl font-bold text-text-primary">GHS {employees[latestYear].avg_salary_ghs.toLocaleString()}</div>
            </div>
            <div className="rounded-xl border border-card-border bg-card-bg/50 p-4">
              <div className="text-sm text-text-secondary">Turnover Rate</div>
              <div className="text-2xl font-bold text-text-primary">{employees[latestYear].employee_turnover_percent.toFixed(1)}%</div>
            </div>
          </div>
        </ChartContainer>
      </div>
    </div>
  );
}
