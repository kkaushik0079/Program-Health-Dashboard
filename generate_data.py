"""
Generate the synthetic dataset for the Program Health Dashboard.

All data is SYNTHETIC: a fictional 10-hospital clinical documentation platform
rollout ("Project Beacon"). No names, dates or figures come from a real program.

Usage:
    python scripts/generate_data.py
Outputs:
    data/milestones.csv, data/budget.csv, data/raid_log.csv, data/dashboard_data.json
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

STATUS_DATE = "2026-10-31"

# id, workstream, milestone, planned_start, planned_finish, forecast_finish, pct_complete, critical_path, depends_on
milestones = [
    ("M01", "Governance", "Program charter and steering committee approved", "2026-01-05", "2026-01-30", "2026-01-30", 100, True, ""),
    ("M02", "Requirements", "Clinical workflow requirements signed off", "2026-02-02", "2026-03-20", "2026-03-27", 100, True, "M01"),
    ("M03", "Integration", "EHR interface build (HL7/FHIR)", "2026-03-23", "2026-06-12", "2026-06-26", 100, True, "M02"),
    ("M04", "Data", "Historical note migration and reconciliation", "2026-04-06", "2026-07-31", "2026-08-14", 100, False, "M02"),
    ("M05", "Security", "HIPAA risk assessment and access controls", "2026-04-20", "2026-06-30", "2026-06-30", 100, False, "M02"),
    ("M06", "Testing", "System and integration testing", "2026-06-15", "2026-08-28", "2026-09-18", 100, True, "M03"),
    ("M07", "Testing", "User acceptance testing (3 pilot sites)", "2026-08-31", "2026-10-09", "2026-10-30", 90, True, "M06"),
    ("M08", "Training", "Super-user and provider training", "2026-09-14", "2026-11-13", "2026-11-20", 60, False, "M07"),
    ("M09", "Deployment", "Wave 1 go-live (4 hospitals)", "2026-11-16", "2026-11-20", "2026-12-04", 0, True, "M07"),
    ("M10", "Deployment", "Wave 2 go-live (6 hospitals)", "2027-01-11", "2027-01-22", "2027-02-05", 0, True, "M09"),
    ("M11", "Adoption", "Hypercare and adoption tracking", "2026-11-23", "2027-03-12", "2027-03-26", 0, False, "M09"),
]

BUDGET_TOTAL = 2_400_000
months = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07",
          "2026-08", "2026-09", "2026-10", "2026-11", "2026-12", "2027-01", "2027-02", "2027-03"]
planned_monthly = [60, 90, 120, 170, 190, 210, 200, 190, 180, 200, 230, 180, 170, 120, 90]  # $K
actual_monthly = [58, 96, 131, 182, 205, 224, 214, 201, 196, 214]                           # $K through Oct
forecast_monthly = [0] * 10 + [240, 205, 185, 140, 105]                                     # $K remaining
assert sum(planned_monthly) * 1000 == BUDGET_TOTAL

budget, cp, ca, cf = [], 0, 0, 0
for i, m in enumerate(months):
    cp += planned_monthly[i]
    if i < len(actual_monthly):
        ca += actual_monthly[i]; cf = ca
        budget.append({"month": m, "planned_k": planned_monthly[i], "actual_k": actual_monthly[i], "forecast_k": "",
                       "cum_planned_k": cp, "cum_actual_k": ca, "cum_forecast_k": ca})
    else:
        cf += forecast_monthly[i]
        budget.append({"month": m, "planned_k": planned_monthly[i], "actual_k": "", "forecast_k": forecast_monthly[i],
                       "cum_planned_k": cp, "cum_actual_k": "", "cum_forecast_k": cf})

# Earned value at status date, in $K
pv = sum(planned_monthly[:10])
ac = sum(actual_monthly)
ev = round(pv * 0.92)  # 92% of planned work actually done
evm = {"pv_k": pv, "ev_k": ev, "ac_k": ac, "cpi": round(ev / ac, 2), "spi": round(ev / pv, 2),
       "bac_k": BUDGET_TOTAL // 1000, "eac_k": cf}

# id, type, title, workstream, owner, probability(1-5), impact(1-5), status, due, mitigation
raid = [
    ("R01", "Risk", "Wave 1 go-live slips if UAT defects are not closed by Nov 6", "Testing", "QA Lead", 4, 5, "Open", "2026-11-06", "Daily defect triage; add two testers from vendor"),
    ("R02", "Risk", "Provider adoption below 80% target at pilot sites", "Adoption", "Clinical Champion", 3, 4, "Open", "2026-12-18", "Super-user coverage on every unit during hypercare"),
    ("R03", "Risk", "Interface volume exceeds vendor capacity at peak hours", "Integration", "Integration Architect", 2, 5, "Open", "2026-11-13", "Load test at 2x peak; scale message queue"),
    ("R04", "Risk", "Budget overrun from extended vendor support", "Governance", "Program Manager", 3, 3, "Open", "2026-11-30", "Change request for scope; renegotiate support rate"),
    ("R05", "Risk", "Training seats unfilled due to clinical staffing", "Training", "Training Lead", 4, 3, "Open", "2026-11-13", "Add evening and e-learning sessions"),
    ("R06", "Risk", "Data migration mismatches in historical notes", "Data", "Data Lead", 2, 4, "Closed", "2026-08-14", "Source-to-target reconciliation reached 99.7% match"),
    ("R07", "Risk", "Access role mapping errors expose PHI", "Security", "Security Officer", 1, 5, "Open", "2026-11-13", "Role-based access audit before each wave"),
    ("A01", "Assumption", "Each pilot site releases 6 super-users for 3 weeks", "Training", "Site Directors", 0, 0, "Validated", "2026-09-30", ""),
    ("A02", "Assumption", "No EHR upgrade freeze during Wave 2 window", "Deployment", "IT Change Board", 0, 0, "Open", "2026-12-15", ""),
    ("I01", "Issue", "Speech-to-text accuracy below threshold in ED notes", "Testing", "Vendor PM", 0, 4, "Open", "2026-11-04", "Vendor model update scheduled; retest in pilot ED"),
    ("I02", "Issue", "Two pilot sites missing test patient records", "Testing", "Data Lead", 0, 3, "Resolved", "2026-10-16", "Test data loaded and verified"),
    ("I03", "Issue", "Steering committee approval for Wave 2 scope pending", "Governance", "Program Sponsor", 0, 3, "Open", "2026-11-20", "Decision memo sent with three options"),
    ("D01", "Dependency", "EHR vendor interface certification", "Integration", "EHR Vendor", 0, 0, "Complete", "2026-06-26", ""),
    ("D02", "Dependency", "Network upgrade at Wave 2 hospitals", "Deployment", "Infrastructure", 0, 0, "On track", "2026-12-18", ""),
]

def write(name, rows, cols):
    with open(DATA / name, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols); w.writerows(rows)

ms_cols = ["id", "workstream", "milestone", "planned_start", "planned_finish", "forecast_finish", "pct_complete", "critical_path", "depends_on"]
raid_cols = ["id", "type", "title", "workstream", "owner", "probability", "impact", "status", "due", "mitigation"]
write("milestones.csv", milestones, ms_cols)
write("raid_log.csv", raid, raid_cols)
with open(DATA / "budget.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(budget[0].keys())); w.writeheader(); w.writerows(budget)

with open(DATA / "dashboard_data.json", "w") as f:
    json.dump({"statusDate": STATUS_DATE,
               "milestones": [dict(zip(ms_cols, m)) for m in milestones],
               "budget": budget, "evm": evm,
               "raid": [dict(zip(raid_cols, r)) for r in raid]}, f, separators=(",", ":"))
print("EVM:", evm)
