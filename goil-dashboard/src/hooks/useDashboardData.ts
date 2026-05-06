import { useState, useEffect } from 'react';
import { loadJson } from '../utils/helpers';
import type {
  RevenueData,
  ExpenseData,
  FuelSalesVolume,
  OperationalData,
  BalanceSheetData,
  CashFlowData,
} from '../types';

interface DashboardData {
  revenue: RevenueData | null;
  expenses: ExpenseData | null;
  fuel: FuelSalesVolume | null;
  ops: OperationalData | null;
  balanceSheet: BalanceSheetData | null;
  cashFlow: CashFlowData | null;
  loading: boolean;
  error: string | null;
}

export function useDashboardData(): DashboardData {
  const [data, setData] = useState<DashboardData>({
    revenue: null,
    expenses: null,
    fuel: null,
    ops: null,
    balanceSheet: null,
    cashFlow: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      const files = [
        { key: 'revenue', loader: () => loadJson<RevenueData>('revenue.json') },
        { key: 'expenses', loader: () => loadJson<ExpenseData>('expenses.json') },
        { key: 'fuel', loader: () => loadJson<FuelSalesVolume>('fuel_sales_volume.json') },
        { key: 'ops', loader: () => loadJson<OperationalData>('operational_metrics.json') },
        { key: 'balanceSheet', loader: () => loadJson<BalanceSheetData>('balance_sheet.json') },
        { key: 'cashFlow', loader: () => loadJson<CashFlowData>('cash_flow.json') },
      ];

      const results = await Promise.allSettled(files.map(f => f.loader()));

      if (cancelled) return;

      const newData: Partial<DashboardData> = { loading: false };
      const errors: string[] = [];

      results.forEach((result, index) => {
        const key = files[index].key as keyof DashboardData;
        if (result.status === 'fulfilled') {
          (newData as Record<string, unknown>)[key] = result.value;
        } else {
          errors.push(files[index].key);
          (newData as Record<string, unknown>)[key] = null;
        }
      });

      newData.error = errors.length > 0 ? `Failed to load: ${errors.join(', ')}` : null;

      setData(prev => ({ ...prev, ...newData }));
    }

    loadData();

    return () => { cancelled = true; };
  }, []);

  return data;
}
