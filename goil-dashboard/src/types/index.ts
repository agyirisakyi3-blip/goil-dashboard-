export interface QuarterlyRevenue {
  quarter: string;
  year: number;
  month: number;
  fuel_sales: number;
  lubricants: number;
  convenience_store: number;
  fleet_services: number;
  other_income: number;
  total_revenue: number;
}

export interface AnnualRevenueSummary {
  [year: string]: {
    fuel_sales: number;
    lubricants: number;
    convenience_store: number;
    fleet_services: number;
    other_income: number;
    total_revenue: number;
    yoy_growth: number | null;
  };
}

export interface RevenueData {
  company: string;
  currency: string;
  period: string;
  revenue: {
    quarterly: QuarterlyRevenue[];
    annual_summary: AnnualRevenueSummary;
    revenue_by_region: { [year: string]: { [region: string]: number } };
  };
}

export interface QuarterlyExpense {
  quarter: string;
  cost_of_goods_sold: number;
  employee_costs: number;
  transport_logistics: number;
  marketing_advertising: number;
  maintenance_repairs: number;
  utilities: number;
  insurance: number;
  depreciation: number;
  administrative: number;
  interest_expense: number;
  taxes_levies: number;
  other_expenses: number;
  total_expenses: number;
}

export interface AnnualExpenseSummary {
  [year: string]: {
    cost_of_goods_sold: number;
    employee_costs: number;
    transport_logistics: number;
    marketing_advertising: number;
    maintenance_repairs: number;
    utilities: number;
    insurance: number;
    depreciation: number;
    administrative: number;
    interest_expense: number;
    taxes_levies: number;
    other_expenses: number;
    total_expenses: number;
    cogs_percentage: number;
    opex_percentage: number;
  };
}

export interface ExpenseData {
  company: string;
  currency: string;
  period: string;
  expenses: {
    quarterly: QuarterlyExpense[];
    annual_summary: AnnualExpenseSummary;
  };
}

export interface QuarterlyKPI {
  quarter: string;
  gross_profit_margin: number;
  net_profit_margin: number;
  ebitda_margin: number;
  return_on_equity: number;
  return_on_assets: number;
  inventory_turnover: number;
}

export interface StationNetwork {
  [year: string]: {
    total_stations: number;
    company_owned: number;
    dealer_owned: number;
    franchise: number;
    new_stations_opened: number;
    operational_uptime_percent: number;
  };
}

export interface EmployeeMetrics {
  [year: string]: {
    total_employees: number;
    management: number;
    supervisors: number;
    attendants: number;
    administrative: number;
    avg_salary_ghs: number;
    employee_turnover_percent: number;
    training_hours_per_employee: number;
    safety_incidents: number;
  };
}

export interface CustomerMetrics {
  [year: string]: {
    loyalty_program_members: number;
    active_fleet_accounts: number;
    customer_satisfaction_score: number;
    nps_score: number;
    avg_transaction_value_ghs: number;
    repeat_customer_rate: number;
  };
}

export interface OperationalData {
  operational_metrics: {
    kpis: {
      quarterly: QuarterlyKPI[];
    };
    station_network: StationNetwork;
    employee_metrics: EmployeeMetrics;
    customer_metrics: CustomerMetrics;
  };
}

export interface FuelAnnualSummary {
  [year: string]: {
    pms_liters: number;
    diesel_liters: number;
    kerosene_liters: number;
    lpg_tons: number;
    total_liters: number;
    avg_daily_liters: number;
    yoy_growth_percent?: number;
  };
}

export interface FuelSalesVolume {
  fuel_sales_volume: {
    annual_summary: FuelAnnualSummary;
    monthly: {
      month: string;
      year: number;
      pms_liters: number;
      diesel_liters: number;
      kerosene_liters: number;
      lpg_tons: number;
      total_liters: number;
    }[];
    fuel_type_mix: {
      [year: string]: {
        pms_percent: number;
        diesel_percent: number;
        kerosene_percent: number;
      };
    };
  };
}

export interface BalanceSheetData {
  balance_sheet: {
    annual: {
      [year: string]: {
        assets: {
          current_assets: {
            cash_and_equivalents: number;
            short_term_investments: number;
            accounts_receivable: number;
            inventory: number;
            prepaid_expenses: number;
            other_current_assets: number;
            total_current_assets: number;
          };
          non_current_assets: {
            property_plant_equipment: number;
            accumulated_depreciation: number;
            net_ppe: number;
            intangible_assets: number;
            long_term_investments: number;
            deferred_tax_assets: number;
            other_non_current_assets: number;
            total_non_current_assets: number;
          };
          total_assets: number;
        };
        liabilities: {
          current_liabilities: {
            accounts_payable: number;
            short_term_debt: number;
            accrued_expenses: number;
            taxes_payable: number;
            deferred_revenue: number;
            other_current_liabilities: number;
            total_current_liabilities: number;
          };
          non_current_liabilities: {
            long_term_debt: number;
            deferred_tax_liabilities: number;
            pension_obligations: number;
            other_non_current_liabilities: number;
            total_non_current_liabilities: number;
          };
          total_liabilities: number;
        };
        equity: {
          share_capital: number;
          retained_earnings: number;
          treasury_stock: number;
          other_comprehensive_income: number;
          total_equity: number;
        };
        total_liabilities_and_equity: number;
      };
    };
    key_ratios: {
      [year: string]: {
        current_ratio: number;
        quick_ratio: number;
        debt_to_equity: number;
        debt_to_assets: number;
        equity_multiplier: number;
        working_capital: number;
      };
    };
  };
}

export interface CashFlowData {
  cash_flow: {
    annual_summary: {
      [year: string]: {
        net_cash_from_operations: number;
        net_cash_from_investing: number;
        net_cash_from_financing: number;
        net_change_in_cash: number;
        free_cash_flow: number;
        capex: number;
        dividends_paid: number;
      };
    };
    quarterly: {
      quarter: string;
      operating_activities: {
        net_income: number;
        depreciation_amortization: number;
        changes_in_working_capital: number;
        other_operating_activities: number;
        net_cash_from_operations: number;
      };
      investing_activities: {
        capital_expenditures: number;
        asset_sales: number;
        investments_purchases: number;
        other_investing_activities: number;
        net_cash_from_investing: number;
      };
      financing_activities: {
        debt_proceeds: number;
        debt_repayments: number;
        dividends_paid: number;
        other_financing_activities: number;
        net_cash_from_financing: number;
      };
      net_change_in_cash: number;
      free_cash_flow: number;
    }[];
  };
}
