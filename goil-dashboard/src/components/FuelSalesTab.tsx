import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
} from 'recharts';
import { KpiCard, ChartContainer } from './UI';
import type { FuelSalesVolume } from '../types';

const FUEL_COLORS = ['#E8760A', '#F59E0B', '#D4600A'];

interface FuelSalesTabProps {
  fuel: FuelSalesVolume;
  selectedYears: number[];
}

export function FuelSalesTab({ fuel, selectedYears }: FuelSalesTabProps) {
  const fuelSummary = fuel.fuel_sales_volume.annual_summary;
  const availableYears = selectedYears.filter((y) => fuelSummary[String(y)]);
  const latestYear = String(Math.max(...availableYears));

  const monthlyData = fuel.fuel_sales_volume.monthly;
  const fuelMix = fuel.fuel_sales_volume.fuel_type_mix[latestYear];

  const yoyGrowth = fuelSummary[latestYear].yoy_growth_percent ?? 19.1;

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Fuel Sales Volume</h2>
        <p className="text-text-secondary">Track liters sold, fuel mix, and LPG performance</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          icon="🛢️"
          label="Total Volume"
          value={`${(fuelSummary[latestYear].total_liters / 1e9).toFixed(2)}B Liters`}
          delta={`+${yoyGrowth.toFixed(1)}% YoY`}
        />
        <KpiCard icon="📊" label="Avg Daily" value={`${(fuelSummary[latestYear].avg_daily_liters / 1e6).toFixed(2)}M L`} delta="Growing" />
        <KpiCard icon="🔥" label="LPG Sales" value={`${fuelSummary[latestYear].lpg_tons.toLocaleString()} Tons`} delta="+21.6% YoY" />
        <KpiCard icon="⛽" label="PMS Share" value={`${fuelMix.pms_percent.toFixed(1)}%`} delta="Dominant" />
      </div>

      <ChartContainer title="Monthly Volume Trends" className="mb-4">
        <ResponsiveContainer width="100%" height={380}>
          <LineChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="month" stroke="#94A3B8" />
            <YAxis stroke="#94A3B8" tickFormatter={(v: unknown) => `${(Number(v) / 1e6).toFixed(0)}M`} />
            <Tooltip formatter={(value: unknown) => `${(Number(value) / 1e6).toFixed(1)}M liters`} />
            <Legend />
            <Line type="monotone" dataKey="pms_liters" name="PMS" stroke="#E8760A" strokeWidth={2} />
            <Line type="monotone" dataKey="diesel_liters" name="Diesel" stroke="#F59E0B" strokeWidth={2} />
            <Line type="monotone" dataKey="kerosene_liters" name="Kerosene" stroke="#D4600A" strokeWidth={2} strokeDasharray="5 5" />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title={`Fuel Mix (${latestYear})`}>
          <ResponsiveContainer width="100%" height={340}>
            <PieChart>
              <Pie
                data={[
                  { name: 'PMS (Petrol)', value: fuelMix.pms_percent },
                  { name: 'Diesel', value: fuelMix.diesel_percent },
                  { name: 'Kerosene', value: fuelMix.kerosene_percent },
                ]}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
                label={(entry: unknown) => {
                  const e = entry as { name: string; percent: number | undefined };
                  return `${e.name} ${((e.percent ?? 0) * 100).toFixed(1)}%`;
                }}
              >
                {FUEL_COLORS.map((color, i) => (
                  <Cell key={i} fill={color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: unknown) => `${Number(value).toFixed(1)}%`} />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="LPG Sales Trend">
          <ResponsiveContainer width="100%" height={340}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="month" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip formatter={(value: unknown) => `${Number(value).toLocaleString()} tons`} />
              <Bar dataKey="lpg_tons" name="LPG Tons" fill="#F59E0B" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>
    </div>
  );
}
