# Personal Expense Analyzer — Project Scope

## Purpose

Build a personal expense tracking website that helps you understand where your money goes, through spending by category and comparisons across months.

## Agreed first-version scope

### Audience and access

- For your personal use.
- A website usable on both phone and computer.
- Online data storage with a login.
- The same expenses available across your devices.

### Currency

- One currency: Kazakhstani tenge (KZT).
- No currency conversion.

### Expense entry

- Enter expenses manually.
- Each expense includes amount, date, category, and an optional note.
- Bank or card statement uploads are outside the first-version scope.
- Merchant, payment method, and tags are outside the chosen simple entry format.

### Categories

- Provide a starter list of categories.
- Allow you to create and rename categories to suit your spending.
- Possible starter categories discussed: food, transport, shopping, and bills. The final starter list is still to be defined.

### Spending analysis

- Monthly total spending.
- Monthly breakdown by category.
- Spending comparisons and trends across months.
- A dedicated daily spending view is outside the chosen reporting scope.

### Recurring expenses

- Support weekly, monthly, and yearly schedules.
- Set an amount and schedule for each recurring expense.
- Add expenses automatically on their scheduled dates.
- Count them toward spending immediately, assuming payment occurred.
- No payment confirmation or pending-payment review is required.

### Export

- Download expense data as CSV.
- Use the export in Excel or retain it as a backup.

## Proposed supporting behavior

The scope summary proposed editing and deleting expense entries. These are sensible supporting functions, but were not separately selected in the brainstorming questions.

## Outside the first version

- Bank or card statement imports.
- Budget limits and remaining-budget tracking.
- Savings recommendations or advice on cutting back.
- Household sharing or a product designed for multiple users.
- Multiple currencies and currency conversion.
- Detailed entry fields such as merchant, payment method, and tags.
- Dedicated daily spending reports.
- Confirmation of recurring payments before counting them as spending.

These exclusions keep the first version focused; they can be revisited later.

## How the tool should work

1. Log in from your phone or computer.
2. Enter an expense with its KZT amount, date, category, and optional note.
3. Customize the starter categories when needed.
4. Set up weekly, monthly, or yearly recurring expenses.
5. The tool automatically records recurring expenses when their scheduled dates arrive.
6. Review monthly totals, category breakdowns, and comparisons across months.
7. Export your expense data as CSV whenever needed.

## Decisions recorded

| Topic | Selected option |
| --- | --- |
| Intended audience | Just you |
| Expense input | Manual entry |
| Primary purpose | Understand where your money goes |
| Entry detail | Amount, date, category, optional note |
| Devices | Phone and computer |
| Categories | Customizable starter list |
| Reports | Monthly summary and trends |
| Currency support | One currency |
| Storage | Online with a login and device sync |
| Currency | KZT |
| Download | CSV export |
| Recurring expenses | Automatically scheduled entries |
| Recurring schedules | Weekly, monthly, yearly |
| Counting recurring expenses | Automatically on the scheduled date |

## Still to define

- Screens and the daily workflow.
- Chart types, comparison periods, and filters.
- Recurring expense edge cases, including month-end dates, missed schedules, changes, and cancellation.
- Login method.
- Final starter categories.
- CSV columns and export filtering.

## Next brainstorming options

Choose one topic to explore next:

1. Screens and daily workflow.
2. Charts and spending insights.
3. Recurring expense rules and edge cases.

Continue brainstorming with one question at a time and short responses.
