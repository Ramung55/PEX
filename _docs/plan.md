# Personal Expense Analyzer — Project Scope

## Purpose

Build a personal expense tracking website that shows where money goes through monthly spending totals, category breakdowns, and comparisons across months.

## Selected technology and hosting

- Django for authentication, forms, business rules, reports, and CSV export.
- PostgreSQL for persistent data storage.
- HTMX for interactive forms and filters.
- Chart.js for category and trend charts.
- An owned server for hosting; the server and domain will be selected later.
- Server-side scheduling for recurring expenses and Trash cleanup, independent of whether the website is open.

## Access and devices

- One private account for personal use; public registration is disabled.
- Login is remembered between visits on personal devices.
- A responsive website usable on phone and computer.
- Online storage makes the same records available across devices.
- Asia/Qyzylorda (UTC+5) determines the current date, reporting month, and recurring due dates.

## Expense entry

- Manual entry with amount in Kazakhstani tenge (KZT), date, category, and optional note.
- One currency, with no conversion.
- Edit existing entries to correct their details.
- Merchant, payment method, and tags are outside the simple entry format.

## Categories

- Provide a customizable starter list and allow category creation and renaming.
- Archive categories rather than deleting their historical associations.
- Archived categories remain visible in past records and reports but are hidden from new-entry choices.
- The final starter list is still to be confirmed.

## Dashboard and analysis

- Open the dashboard on the current month.
- Show total spending and a category breakdown for the selected month.
- Show a 12-month spending trend by default, allowing comparison across months.
- Exclude Trash entries from active spending totals and charts.
- A dedicated daily spending report is outside this version.

## Recurring expenses

- Support weekly, monthly, and yearly schedules.
- Record payments automatically on their scheduled dates and count them immediately as spending, assuming payment occurred.
- When the scheduled day does not exist in a month, use that month's last day.
- After downtime, automatically record missed payments with their original due dates.
- Changing a recurring amount applies to future and linked past payments, except past amounts the user manually adjusted.
- Cancelling a schedule stops future payments and keeps past records.
- Deleting a generated payment while its schedule is active causes the scheduler to recreate it; cancel the schedule to stop future generation.
- Generation must avoid duplicate active payments for the same schedule and due date.

## Trash

- Deleted expenses go to Trash and can be restored during a 30-day retention window.
- After 30 days, they are permanently deleted automatically.
- A recurring payment's deleted record must not be restored alongside an active replacement for the same occurrence.

The last rule is a supporting design choice to reconcile restoration with automatic recreation and prevent double counting.

## CSV export

- Download all active expenses by default, rather than only the selected month.
- Retain archived category names in exported historical records.
- CSV provides spreadsheet access and an expense-data copy; a complete system backup is a separate deployment concern.
- Exact CSV columns and any optional export filters remain implementation details to finalize.

## Outside the first version

- Bank or card statement imports.
- Budget limits and remaining-budget tracking.
- Savings advice or recommendations on cutting back.
- Household sharing, public registration, and a product designed for multiple users.
- Multiple currencies and currency conversion.
- Detailed entry fields such as merchant, payment method, and tags.
- Dedicated daily spending reports.
- Payment confirmation before recurring entries count toward spending.

## Main workflow

1. Log in from a phone or computer.
2. Enter a KZT amount, date, category, and optional note.
3. Customize or archive categories as needed.
4. Set up weekly, monthly, or yearly recurring expenses.
5. The server records due payments automatically and catches up after downtime.
6. Review the current-month summary and the 12-month trend.
7. Edit records, use Trash for deletion and recovery, or export complete expense history as CSV.

## Proposed implementation defaults

The backlog proposes the following defaults; they were not explicitly selected during brainstorming and must be reviewed during the relevant issue:

- Positive amounts stored as exact decimals with two decimal places.
- Hourly server scheduling.
- Renewable 30-day login sessions.
- Food, Transport, Shopping, and Bills as starter categories.
- A trend window ending with the selected dashboard month.
- Preserving the original recurring day anchor after a short-month adjustment.
- Tracking manual amount overrides separately from changes to other fields.

## Still to define

- Detailed screen layouts and chart presentation.
- Login identifier, session expiry, and account recovery details.
- Final starter categories.
- Exact CSV columns and optional export filtering.
- Recurring schedule changes beyond amount updates and cancellation, including changes to category, frequency, and due date.
- Hosting provider, server, domain, and deployment details.

## Work organization

Implementation tasks are [GitHub issues](https://github.com/Ramung55/PEX/issues), handled one at a time. Follow `_docs/process.md`, read acceptance criteria before starting and before closing, and commit regularly. `_docs/tasks.md` is a local reference to the issue backlog.

Implementation has not started; these documents define the planned product.
