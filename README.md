# Goil Ghana Financial Dashboard

A comprehensive financial analytics dashboard for Goil Ghana Limited, built with both **Streamlit (Python)** and **React + TypeScript**.

## Features

- **Revenue Analytics** - Track revenue streams, growth trends, and regional performance
- **Expense Management** - Monitor costs, optimize spending, and analyze expense breakdowns
- **Profitability Analysis** - View margins, ROE, ROA, and EBITDA metrics
- **Fuel Sales Volume** - Monitor liters sold, fuel mix, and LPG performance
- **Balance Sheet** - Assets, liabilities, and equity tracking
- **Cash Flow** - Operating, investing, and financing cash flows
- **Operations** - Station network, employee metrics, and KPIs
- **Regional Analytics** - Performance by region

## Tech Stack

### React Dashboard (`/goil-dashboard`)
- React 19 + TypeScript
- Vite 8 (build tool)
- Tailwind CSS 4
- Framer Motion (animations)
- Recharts (charts)
- Lucide React (icons)

### Streamlit Dashboard (root)
- Streamlit
- Plotly (charts)
- Pandas

## Quick Start

### React Dashboard

```bash
cd goil-dashboard
npm install
npm run dev
```

Open **http://localhost:3000**

### Streamlit Dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Production Build

```bash
cd goil-dashboard
npm run build
npm run preview
```

## Project Structure

```
Host/
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
├── data/                           # JSON data files (used by Streamlit)
│   ├── revenue.json
│   ├── expenses.json
│   ├── fuel_sales_volume.json
│   ├── operational_metrics.json
│   ├── balance_sheet.json
│   └── cash_flow.json
└── goil-dashboard/                # React + TypeScript dashboard
    ├── src/
    │   ├── components/             # UI components
    │   │   ├── OverviewTab.tsx
    │   │   ├── RevenueTab.tsx
    │   │   ├── ExpensesTab.tsx
    │   │   ├── ProfitabilityTab.tsx
    │   │   ├── FuelSalesTab.tsx
    │   │   ├── BalanceSheetTab.tsx
    │   │   ├── CashFlowTab.tsx
    │   │   ├── OperationsTab.tsx
    │   │   ├── RegionalTab.tsx
    │   │   ├── Sidebar.tsx
    │   │   ├── UI.tsx
    │   │   ├── ErrorBoundary.tsx
    │   │   └── NotFound.tsx
    │   ├── hooks/
    │   │   └── useDashboardData.ts
    │   ├── types/
    │   │   └── index.ts
    │   ├── utils/
    │   │   └── helpers.ts
    │   ├── App.tsx
    │   └── main.tsx
    ├── public/data/                # JSON data (used by React)
    └── package.json
```

## Data Files

The dashboard uses JSON data files stored in two locations:
- `data/` - Used by Streamlit dashboard
- `goil-dashboard/public/data/` - Used by React dashboard

## License

MIT
