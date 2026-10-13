# Personal Expense Analyzer — Task Backlog

Tasks migrated to [GitHub Issues](https://github.com/Ramung55/PEX/issues) in the public [PEX repository](https://github.com/Ramung55/PEX). This file retains the original handoff descriptions and links to each issue. GitHub issues are the source for current task status, discussion, and acceptance criteria; this file is not a separate status tracker.

This backlog covers `_docs/plan.md` plus the decisions made during brainstorming. Each task is intended for one implementation session; its description repeats the context needed for handoff. Dependencies are existing project components, not knowledge of other task descriptions. Implementation has not started. Follow `_docs/process.md`: work on one issue at a time, read acceptance criteria before starting and before closing, and commit regularly. Ask before adding dependencies to `pyproject.toml`.

Selected stack: Django, PostgreSQL, HTMX, and Chart.js. Hosting: an owned server, to be selected later. Access: one private account, no public registration, persistent login. Currency: KZT. Timezone: Asia/Qyzylorda. Excluded: bank imports, budgets, savings advice, household sharing, and multiple currencies.

Proposed implementation defaults to review during the relevant task: positive amounts stored as exact decimals with two decimal places; hourly server scheduling; a renewable 30-day login session; Food, Transport, Shopping, and Bills as starter categories. These defaults were not explicitly selected during brainstorming.

## 1. Set up an empty project with a passing test
GitHub issue: https://github.com/Ramung55/PEX/issues/1
Goal: Establish a minimal Django project that starts and passes a smoke test.
Description: Create the project skeleton, dependency configuration, and a minimal page without expense features. Add a smoke test that checks the page responds successfully, and document how to start the project and run the test from a clean checkout.

## 2. Configure PostgreSQL and environment settings
GitHub issue: https://github.com/Ramung55/PEX/issues/2
Goal: Connect Django to PostgreSQL using configuration outside source code.
Description: Provide local database setup and an example environment file with credential placeholders. Configure Asia/Qyzylorda as the application timezone and verify that migrations run against PostgreSQL.

## 3. Establish automated checks
GitHub issue: https://github.com/Ramung55/PEX/issues/3
Goal: Make existing tests and basic code checks reproducible.
Description: Configure formatting, linting, and an automated test workflow using a disposable PostgreSQL database. Document the commands and verify that the initial smoke test passes without real credentials.

## 4. Build the responsive page shell
GitHub issue: https://github.com/Ramung55/PEX/issues/4
Goal: Provide consistent navigation on phone and computer.
Description: Create a shared Django layout for Dashboard, Expenses, Categories, Recurring Expenses, and Trash, using placeholder pages where needed. Include HTMX and accessible loading, error, and empty-state patterns, and verify navigation at phone and desktop widths.

## 5. Add private login and persistent sessions
GitHub issue: https://github.com/Ramung55/PEX/issues/5
Goal: Restrict access to one private account while remembering login between visits.
Description: Use Django authentication for login and logout without public registration, and document private account provisioning. Protect all application pages and data endpoints, and verify login survives browser closure while logout invalidates the session.

## 6. Define category storage and starter categories
GitHub issue: https://github.com/Ramung55/PEX/issues/6
Goal: Store customizable categories while preserving historical labels.
Description: Add an account-owned category model with name and archive status, plus an idempotent starter-category initialization step. Use Food, Transport, Shopping, and Bills as the proposed initial list, and verify initialization neither duplicates nor overwrites customized categories.

## 7. Build category creation and renaming
GitHub issue: https://github.com/Ramung55/PEX/issues/7
Goal: Let the user add categories and rename existing ones.
Description: Build authenticated category list, create, and rename screens using Django forms and HTMX where useful. Validate blank and duplicate names, show field-level errors, and preserve expense links when names change.

## 8. Add category archiving and restoration
GitHub issue: https://github.com/Ramung55/PEX/issues/8
Goal: Hide retired categories from new entries while preserving history.
Description: Archive categories instead of deleting them, and allow archived categories to be restored. Hide them from new-expense choices, retain their labels in reports, and keep an existing archived assignment valid when editing an unrelated expense field.

## 9. Define expense storage and validation
GitHub issue: https://github.com/Ramung55/PEX/issues/9
Goal: Store manual expenses accurately with ownership and deletion metadata.
Description: Add exact KZT amount, local expense date, category, optional note, creation timestamp, and nullable Trash timestamp. Enforce account ownership and valid amounts and categories, and verify decimal storage rather than floating-point arithmetic.

## 10. Build manual expense entry
GitHub issue: https://github.com/Ramung55/PEX/issues/10
Goal: Add a spending record from phone or computer.
Description: Create an authenticated form for amount, date, category, and optional note, defaulting the date to today in Asia/Qyzylorda. Show validation and success feedback, and verify valid submissions create one record while invalid submissions preserve entered values.

## 11. Build the expense list and month filter
GitHub issue: https://github.com/Ramung55/PEX/issues/11
Goal: Browse recorded expenses for a selected month.
Description: Show active expenses in date order with KZT amount, category, and note, defaulting to the current local month. Add month selection and pagination, exclude Trash, and verify month boundaries and empty results.

## 12. Add expense editing
GitHub issue: https://github.com/Ramung55/PEX/issues/12
Goal: Correct an expense without replacing its identity.
Description: Build an authenticated edit form for amount, date, category, and note. For generated recurring expenses, track manual overrides by field so a manually adjusted amount survives later schedule amount changes, while editing a note alone does not freeze the amount.

## 13. Add Trash and restoration
GitHub issue: https://github.com/Ramung55/PEX/issues/13
Goal: Recover deleted expenses during a 30-day retention window.
Description: Move expenses to Trash, exclude them from reports and ordinary lists, and display deleted entries with a restore action. Restore the original record unless an active replacement exists for the same recurring occurrence, in which case explain why restoration is blocked to prevent double counting.

## 14. Add automatic Trash cleanup
GitHub issue: https://github.com/Ramung55/PEX/issues/14
Goal: Permanently remove expenses after 30 days in Trash.
Description: Implement a repeatable cleanup command deleting entries only when their Trash timestamp is at least 30 days old. Test the retention boundary and preserve recurring occurrence identifiers outside deleted expense records so scheduled history remains consistent.

## 15. Define recurring schedule and occurrence storage
GitHub issue: https://github.com/Ramung55/PEX/issues/15
Goal: Represent recurring rules and generated payments without duplicates.
Description: Add account-owned schedules with amount, category, optional note, weekly/monthly/yearly frequency, first due date, and cancellation status, plus occurrence records uniquely identified by schedule and original due date. Track generated and superseded expenses through occurrences so each due payment has at most one active expense, including after Trash cleanup.

## 16. Implement recurring due-date calculation
GitHub issue: https://github.com/Ramung55/PEX/issues/16
Goal: Calculate weekly, monthly, and yearly dates consistently.
Description: Calculate due dates in Asia/Qyzylorda and use the last day of a target month when the original day does not exist. Preserve the original day anchor so January 31 returns to March 31 after February, and test short months, leap years, yearly February 29 schedules, and year boundaries.

## 17. Build recurring schedule creation and listing
GitHub issue: https://github.com/Ramung55/PEX/issues/17
Goal: Create and inspect automatic expense schedules.
Description: Build forms and a list for amount, category, optional note, frequency, and first due date, supporting weekly, monthly, and yearly recurrence. Display the next due date, validate ownership and available categories, and explain that scheduled payments count automatically without payment confirmation.

## 18. Generate due payments and catch up after downtime
GitHub issue: https://github.com/Ramung55/PEX/issues/18
Goal: Record due recurring payments exactly once without an open browser.
Description: Add a repeatable server command generating all unrecorded occurrences through today's local date with their original due dates. Catch up after downtime and test that repeated or overlapping runs cannot duplicate active payments, including schedules using archived categories.

## 19. Recreate deleted recurring payments
GitHub issue: https://github.com/Ramung55/PEX/issues/19
Goal: Keep active recurring schedules as the source of truth for their payments.
Description: Recreate deleted occurrences on the next scheduler run while the schedule is active, even when the original expense remains in Trash. Link the old record as superseded, prevent restoring it alongside a replacement, and test recreation after the old Trash record is permanently removed.

## 20. Edit recurring amounts and update linked history
GitHub issue: https://github.com/Ramung55/PEX/issues/20
Goal: Apply new recurring amounts to future and eligible past payments.
Description: Allow schedule amount changes and update previously generated linked entries, including eligible Trash records, except amounts manually adjusted by the user. Preserve manual amount overrides even when they equal the old schedule amount, and verify that reports and replacement generation use the appropriate updated amount.

## 21. Cancel recurring schedules
GitHub issue: https://github.com/Ramung55/PEX/issues/21
Goal: Stop future automatic payments while keeping past records.
Description: Add cancellation that preserves existing expenses and occurrence history but stops generation, catch-up, and deleted-payment recreation for that schedule. Display cancelled status clearly and verify repeated cancellation does not change historical spending.

## 22. Calculate monthly totals and category breakdowns
GitHub issue: https://github.com/Ramung55/PEX/issues/22
Goal: Produce accurate reporting data for a selected month.
Description: Create account-scoped queries for total spending and category totals using exact KZT arithmetic and expense dates. Include active manual and generated expenses and archived category labels, exclude Trash, and test month boundaries and empty months.

## 23. Build the current-month dashboard
GitHub issue: https://github.com/Ramung55/PEX/issues/23
Goal: Open the application on a useful summary of current spending.
Description: Show the current month in Asia/Qyzylorda with total spending and category totals using the reporting queries. Add a month selector, links to relevant expenses, and empty states, and verify usability on phone and computer.

## 24. Add the category spending chart
GitHub issue: https://github.com/Ramung55/PEX/issues/24
Goal: Visualize selected-month spending by category.
Description: Use Chart.js to display category totals with readable labels and a table or text equivalent. Format values as KZT, include archived categories with active historical expenses, and handle zero spending and many categories without breaking the layout.

## 25. Calculate the 12-month spending trend
GitHub issue: https://github.com/Ramung55/PEX/issues/25
Goal: Supply a complete month-by-month spending series.
Description: Query 12 consecutive calendar months ending with the selected dashboard month, using exact KZT totals and zeros for empty months. Exclude Trash, label the current month as partial where applicable, and test year boundaries and historical recurring amount changes.

## 26. Add the monthly trend chart
GitHub issue: https://github.com/Ramung55/PEX/issues/26
Goal: Show spending changes across 12 months by default.
Description: Render the trend series with Chart.js and a readable table equivalent, updating it when the selected dashboard month changes. Format KZT values, distinguish an incomplete current month, and verify chart updates do not accumulate duplicate instances.

## 27. Add complete-history CSV export
GitHub issue: https://github.com/Ramung55/PEX/issues/27
Goal: Download all active expense records by default.
Description: Provide an authenticated CSV download containing date, amount, currency, category, note, and manual-or-recurring origin in consistent order. Export all history rather than only the dashboard month, exclude Trash, retain archived category labels, and test Unicode, quoting, exact amounts, and spreadsheet formula-like text.

## 28. Verify account isolation and data-changing requests
GitHub issue: https://github.com/Ramung55/PEX/issues/28
Goal: Keep records and actions accessible only to the authenticated account.
Description: Audit expense, category, recurring, Trash, reporting, and export endpoints for login enforcement, ownership checks, and Django CSRF protection. Add targeted tests for unauthorized reads and writes, including HTMX requests and guessed identifiers.

## 29. Verify the complete user workflow
GitHub issue: https://github.com/Ramung55/PEX/issues/29
Goal: Confirm that the main features work together on phone and computer.
Description: Run and document a workflow covering persistent login, manual entry, editing, archiving, recurring generation, reports, Trash, restoration, and CSV export. Include recurring replacement and blocked duplicate restoration, and record remaining defects as separate follow-up tasks.

## 30. Prepare deployment configuration for an owned server
GitHub issue: https://github.com/Ramung55/PEX/issues/30
Goal: Make deployment repeatable before choosing or provisioning a server.
Description: Prepare a documented production arrangement for Django, PostgreSQL, a production application server, and an HTTPS reverse proxy, using persistent database storage and environment-based secrets. Include static asset handling, disabled debug mode, and deployment commands, and verify locally without publishing the application.

## 31. Configure server scheduling and failure visibility
GitHub issue: https://github.com/Ramung55/PEX/issues/31
Goal: Run payment generation and Trash cleanup reliably in production.
Description: Configure a documented hourly server job using Asia/Qyzylorda date rules regardless of the host timezone. Prevent overlapping runs, record failures in logs, and verify restarting the scheduler catches up missed payments without duplicates.

## 32. Add backup and restore procedures
GitHub issue: https://github.com/Ramung55/PEX/issues/32
Goal: Recover application data if the server or database fails.
Description: Document automated PostgreSQL backups, retention, storage outside the application server, and credential handling, noting that CSV alone is not a complete backup. Test restoration into a disposable database and verify expenses, categories, recurring occurrences, and Trash before calling the procedure complete.

## 33. Deploy and perform a production smoke check
GitHub issue: https://github.com/Ramung55/PEX/issues/33
Goal: Bring the completed application online once hosting is selected.
Description: Configure HTTPS, persistent database storage, the private account, scheduled jobs, and backups on the selected server using the deployment instructions. Verify login, an expense, reporting, CSV export, and scheduler execution, and document rollback; this task waits for server/domain details and authorization to deploy.
