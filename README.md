# Program Health Dashboard: Project Beacon

A steering-committee status dashboard for a fictional rollout of an AI clinical documentation platform to 10 hospitals. It brings together the schedule, cost, and risk views a program manager reports on every month, built on standard PMO methods.

**Live demo:** [add your live link here]

> **All data is synthetic.** Project Beacon is fictional, and no names, dates or figures come from a real program or employer.

## What it shows

- **Program health strip:** schedule performance index (SPI), cost performance index (CPI), estimate at completion against budget, go-live slip, milestones complete, and open high risks, each with a red/amber/green status and an overall program rating
- **Milestone schedule:** baseline against forecast for every milestone, critical-path milestones highlighted, slip in days, percent complete, dependencies on hover, and a status-date line. Filter by workstream.
- **Cumulative cost curve:** planned baseline, actual spend to date, and forecast to completion, with the budget at completion (BAC) and estimate at completion (EAC) labeled
- **Risk heatmap:** open risks placed on a 5 × 5 probability × impact grid
- **RAID log:** risks, assumptions, issues and dependencies with owners, next actions, scores, due dates and overdue flags. Filter by type.

## PMO methods used

| Measure | Formula | Value at status date |
|---|---|---|
| Schedule performance index | SPI = EV ÷ PV | 0.92 (behind schedule) |
| Cost performance index | CPI = EV ÷ AC | 0.86 (over budget) |
| Estimate at completion | Actuals to date + bottom-up forecast | $2.60M against $2.40M budget |
| Risk score | Probability (1 to 5) × impact (1 to 5) | 12 or above goes to steering committee |

Status thresholds: green at 0.95 or above, amber from 0.90 to 0.95, red below 0.90.

## Project structure

```
pmo-program-dashboard/
├── index.html               # the dashboard (plain HTML, CSS, JavaScript; no framework)
├── data/
│   ├── milestones.csv       # 11 milestones: baseline, forecast, % complete, critical path, dependencies
│   ├── budget.csv           # monthly and cumulative planned, actual, forecast ($K)
│   ├── raid_log.csv         # 14 RAID items with owners, scores, status, mitigation
│   └── dashboard_data.json  # same data shaped for the page
└── scripts/generate_data.py # creates the dataset and calculates earned value
```

## Run it locally

```bash
python scripts/generate_data.py   # optional: regenerate the data
# then open index.html in a browser
```

## Skills demonstrated

Program and portfolio reporting · earned value management · critical-path scheduling · RAID and risk management · executive status reporting · data visualization · Python

---
Built by **Kritika Kaushik** · CSPO, CSM · [LinkedIn](add-your-link)
