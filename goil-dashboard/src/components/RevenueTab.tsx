import { useState } from 'react';
import {
  ResponsiveContainer,
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
import type { RevenueData } from '../types';


interface RevenueTabProps {
  revenue: RevenueData;
  selectedYears: number[];
}

export function RevenueTab({ revenue, selectedYears }: RevenueTabProps) {
  const [showTable, setShowTable] = useState(false);
  const revSummary = revenue.revenue.annual_summary;
  const availableYears = selectedYears.filter((y) => revSummary[String(y)]);
  const latestYear = String(Math.max(...availableYears));

  const quarterlyData = revenue.revenue.quarterly;
  const regions = revenue.revenue.revenue_by_region[latestYear] || {};
  const sortedRegions = Object.entries(regions)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 6)
    .map(([region, value]) => ({ name: region.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase()), value }));

  const qoqData = quarterlyData.map((q, i) => {
    const prev = i > 0 ? quarterlyData[i - 1].total_revenue : q.total_revenue;
    return {
      quarter: q.quarter,
      growth: i === 0 ? 0 : ((q.total_revenue - prev) / prev) * 100,
    };
  });

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-3xl font-bold text-text-primary">Revenue Analytics</h2>
        <p className="text-text-secondary">Detailed breakdown of revenue streams and growth trends</p>
      </div>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <KpiCard
          icon="📊"
          label="Annual Revenue"
          value={formatGhs(revSummary[latestYear].total_revenue)}
          delta={`${revSummary[latestYear].yoy_growth?.toFixed(1) ?? 0}% Growth`}
        />
        <KpiCard
          icon="⛽"
          label="Fuel Revenue"
          value={formatGhs(revSummary[latestYear].fuel_sales)}
          delta={`${((revSummary[latestYear].fuel_sales / revSummary[latestYear].total_revenue) * 100).toFixed(1)}% of Total`}
        />
        <KpiCard
          icon="🛢️"
          label="Non-Fuel Revenue"
          value={formatGhs(
            revSummary[latestYear].lubricants +
              revSummary[latestYear].convenience_store +
              revSummary[latestYear].fleet_services +
              revSummary[latestYear].other_income
          )}
          delta="Diversifying"
        />
      </div>

      <ChartContainer title="Quarterly Revenue Breakdown" className="mb-4">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={quarterlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="quarter" stroke="#94A3B8" />
            <YAxis stroke="#94A3B8" tickFormatter={(v: number) => formatGhs(v)} />
            <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
            <Legend />
            <Bar name="Fuel Sales" dataKey="fuel_sales" stackId="a" fill="#E8760A" />
            <Bar name="Lubricants" dataKey="lubricants" stackId="a" fill="#F59E0B" />
            <Bar name="Convenience Store" dataKey="convenience_store" stackId="a" fill="#D4600A" />
            <Bar name="Fleet Services" dataKey="fleet_services" stackId="a" fill="#FFB347" />
            <Bar name="Other Income" dataKey="other_income" stackId="a" fill="#EF4444" />
          </BarChart>
        </ResponsiveContainer>
      </ChartContainer>

      <div className="mb-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ChartContainer title="Quarter-over-Quarter Growth">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={qoqData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="quarter" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" tickFormatter={(v: unknown) => `${Number(v).toFixed(0)}%`} />
              <Tooltip formatter={(value: unknown) => `${Number(value).toFixed(1)}%`} />
              <Bar dataKey="growth" name="QoQ Growth" fill="#E8760A" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>

        <ChartContainer title="Revenue by Region (Top 6)">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sortedRegions} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#94A3B8" tickFormatter={(v: unknown) => formatGhs(Number(v))} />
              <YAxis type="category" dataKey="name" stroke="#94A3B8" width={120} />
              <Tooltip formatter={(value: unknown) => formatGhs(Number(value))} />
              <Bar dataKey="value" fill="#E8760A" name="Revenue" />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      <div className="rounded-xl border border-card-border bg-card-bg">
        <button
          onClick={() => setShowTable(!showTable)}
          className="w-full px-6 py-4 text-left text-lg font-semibold text-text-primary hover:bg-card-border/50"
        >
          {showTable ? '▾' : '▸'} Revenue Detail Table
        </button>
        {showTable && (
          <div className="overflow-x-auto px-6 pb-6">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-card-border">
                  <th className="px-4 py-2 text-left text-text-secondary">Quarter</th>
                  <th className="px-4 py-2 text-right text-text-secondary">Fuel Sales</th>
                  <th className="px-4 py-2 text-right text-text-secondary">Lubricants</th>
                  <th className="px-4 py-2 text-right text-text-secondary">Convenience</th>
                  <th className="px-4 py-2 text-right text-text-secondary">Fleet</th>
                  <th className="px-4 py-2 text-right text-text-secondary">Other</th>
                  <th className="px-4 py-2 text-right text-text-secondary">Total</th>
                </tr>
              </thead>
              <tbody>
                {quarterlyData.map((row) => (
                  <tr key={row.quarter} className="border-b border-card-border/50">
                    <td className="px-4 py-2 text-text-primary">{row.quarter}</td>
                    <td className="px-4 py-2 text-right text-text-primary">{formatGhs(row.fuel_sales)}</td>
                    <td className="px-4 py-2 text-right text-text-primary">{formatGhs(row.lubricants)}</td>
                    <td className="px-4 py-2 text-right text-text-primary">{formatGhs(row.convenience_store)}</td>
                    <td className="px-4 py-2 text-right text-text-primary">{formatGhs(row.fleet_services)}</td>
                    <td className="px-4 py-2 text-right text-text-primary">{formatGhs(row.other_income)}</td>
                    <td className="px-4 py-2 text-right font-semibold text-text-primary">{formatGhs(row.total_revenue)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
