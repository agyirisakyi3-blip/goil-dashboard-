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
import { KpiCard, ChartContainer } from './UI';
import { formatGhs } from '../utils/helpers';
import type { RevenueData, ExpenseData } from '../types';

interface RegionalTabProps {
  revenue: RevenueData;
  expenses: ExpenseData;
  selectedYears: number[];
}

const PRIMARY = '#E8760A';
const SECONDARY = '#F59E0B';
const ACCENT = '#D4600A';
const ACCENT2 = '#FFB347';

const ORANGE_PALETTE = [PRIMARY, SECONDARY, ACCENT2, ACCENT, '#FF8C42', '#FF6B35'];

function formatRegionName(region: string): string {
  return region.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

export function RegionalTab({ revenue, expenses: _expenses, selectedYears }: RegionalTabProps) {
  const revenueByRegion = revenue.revenue.revenue_by_region || {};

  const allRegions = Object.keys(revenueByRegion[selectedYears[0]] || {});

  const totalRegionalRevenue = selectedYears.reduce((sum, year) => {
    const yearData = revenueByRegion[year] || {};
    return sum + Object.values(yearData).reduce((s: number, v: any) => s + (v || 0), 0);
  }, 0);

  const regionTotals: Record<string, number> = {};
  allRegions.forEach(region => {
    regionTotals[region] = selectedYears.reduce((sum, year) => {
      return sum + (revenueByRegion[year]?.[region] || 0);
    }, 0);
  });

  const topRegion = Object.entries(regionTotals).sort((a, b) => b[1] - a[1])[0];
  const topRegionName = topRegion ? formatRegionName(topRegion[0]) : 'N/A';
  const regionsCount = allRegions.length;
  const avgRevenuePerRegion = regionsCount > 0 ? totalRegionalRevenue / regionsCount : 0;

  const barData = allRegions.map(region => {
    const entry: any = { region: formatRegionName(region) };
    selectedYears.forEach(year => {
      entry[year] = revenueByRegion[year]?.[region] || 0;
    });
    return entry;
  });

  const latestYear = Math.max(...selectedYears);
  const pieData = Object.entries(revenueByRegion[latestYear] || {})
    .filter(([, v]) => v > 0)
    .map(([region, value]) => ({
      name: formatRegionName(region),
      value: value as number,
    }));

  const top5Regions = Object.entries(regionTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([region]) => region);

  const lineData = selectedYears.map(year => {
    const entry: any = { year: year.toString() };
    top5Regions.forEach(region => {
      entry[formatRegionName(region)] = revenueByRegion[year]?.[region] || 0;
    });
    return entry;
  });

  const metricsData = allRegions.map(region => {
    const currentYear = selectedYears[selectedYears.length - 1];
    const prevYear = selectedYears[selectedYears.length - 2];
    const currentRevenue = revenueByRegion[currentYear]?.[region] || 0;
    const prevRevenue = prevYear ? (revenueByRegion[prevYear]?.[region] || 0) : 0;
    const growth = prevRevenue > 0 ? ((currentRevenue - prevRevenue) / prevRevenue) * 100 : 0;
    const share = totalRegionalRevenue > 0 ? (regionTotals[region] / totalRegionalRevenue) * 100 : 0;

    return {
      label: formatRegionName(region),
      value: formatGhs(regionTotals[region]),
      sub: `${growth >= 0 ? '+' : ''}${growth.toFixed(1)}% YoY`,
      extra: `${share.toFixed(1)}% of total`,
    };
  }).sort((a, b) => {
    const aVal = regionTotals[allRegions.find(r => formatRegionName(r) === a.label) || ''] || 0;
    const bVal = regionTotals[allRegions.find(r => formatRegionName(r) === b.label) || ''] || 0;
    return bVal - aVal;
  });

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card-bg border border-card-border rounded-lg p-3 shadow-lg">
          <p className="text-text-primary font-medium">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {formatGhs(entry.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const PieTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card-bg border border-card-border rounded-lg p-3 shadow-lg">
          <p className="text-text-primary font-medium">{payload[0].name}</p>
          <p className="text-text-primary">
            {formatGhs(payload[0].value)} ({(payload[0].percent * 100).toFixed(1)}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          icon="💰"
          label="Total Regional Revenue"
          value={formatGhs(totalRegionalRevenue)}
          delta="Across all years"
        />
        <KpiCard
          icon="🏆"
          label="Top Region"
          value={topRegionName}
          delta={topRegion ? formatGhs(topRegion[1]) : 'N/A'}
        />
        <KpiCard
          icon="🗺️"
          label="Regions Count"
          value={regionsCount.toString()}
          delta="Active regions"
        />
        <KpiCard
          icon="📊"
          label="Avg Revenue Per Region"
          value={formatGhs(avgRevenuePerRegion)}
          delta="Per region average"
        />
      </div>

      <ChartContainer title="Regional Revenue Comparison">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={barData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis
              dataKey="region"
              tick={{ fill: '#9CA3AF', fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis tick={{ fill: '#9CA3AF' }} tickFormatter={(v) => formatGhs(v)} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ color: '#9CA3AF' }} />
            {selectedYears.map((year, index) => (
              <Bar
                key={year}
                dataKey={year.toString()}
                name={year.toString()}
                fill={ORANGE_PALETTE[index % ORANGE_PALETTE.length]}
                radius={[4, 4, 0, 0]}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartContainer title={`Revenue Share by Region (${latestYear})`}>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name} (${((entry.percent ?? 0) * 100).toFixed(1)}%)`}
                outerRadius={140}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={ORANGE_PALETTE[index % ORANGE_PALETTE.length]} />
                ))}
              </Pie>
              <Tooltip content={<PieTooltip />} />
              <Legend wrapperStyle={{ color: '#9CA3AF' }} />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Top 5 Regions - Revenue Trends">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={lineData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="year" tick={{ fill: '#9CA3AF' }} />
              <YAxis tick={{ fill: '#9CA3AF' }} tickFormatter={(v) => formatGhs(v)} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ color: '#9CA3AF' }} />
              {top5Regions.map((region, index) => (
                <Line
                  key={region}
                  type="monotone"
                  dataKey={formatRegionName(region)}
                  stroke={ORANGE_PALETTE[index % ORANGE_PALETTE.length]}
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <div className="bg-card-bg border border-card-border rounded-lg p-6">
        <h3 className="text-text-primary text-lg font-semibold mb-4">Regional Performance</h3>
        <div className="space-y-1">
          {metricsData.map((metric, index) => (
            <div key={index} className="flex items-center justify-between py-2 border-b border-card-border last:border-b-0">
              <div>
                <span className="text-text-primary font-medium">{metric.label}</span>
                <span className="ml-3 text-text-secondary text-sm">{metric.extra}</span>
              </div>
              <div className="text-right">
                <span className="text-text-primary font-semibold">{metric.value}</span>
                <span className={`ml-3 text-sm font-medium ${metric.sub.startsWith('+') ? 'text-primary' : 'text-danger'}`}>
                  {metric.sub}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
