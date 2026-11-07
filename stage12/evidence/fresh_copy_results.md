# Stage 12 fresh-copy check and console demo: Lem's results

**Tester:** Lemuel Legaspi (not the release author)
**Date:** Thu 5 Nov 2026, about 15:40 to 16:02
**Machine:** Windows, PowerShell, Python 3.13.17 (the course's verified baseline), pytest 8.3.5
**Candidate tested:** `78affeaedcafadda2a5c60df8be1801f259e2276` ("Stage 12: fix stale Stage 6 TODO docstring in find_patient (release finding)")

## Setup (section F)

| Step | Result | Screenshot |
|---|---|---|
| Fresh clone into new folder `Desktop\smartcare-fresh`, checkout of the candidate | `git rev-parse HEAD` = `78affeaedcafadda2a5c60df8be1801f259e2276` | 01 |
| New venv `python -m venv .venv` | Created | 02 |
| Activate `.venv\Scripts\Activate.ps1` | **Blocked by Windows execution policy** (see finding 1); worked after the workaround. Python runs from `smartcare-fresh\.venv\Scripts\python.exe` | 03, 04 |
| `cd project`, `python --version` | Python 3.13.17 | 05 |
| `python -m pip install -r requirements-dev.txt` | Successfully installed pytest-8.3.5 (+ colorama, iniconfig, packaging, pluggy) | 06 |
| `python main.py` | `A1: P1 with DR1, 2026-10-01 09:00, scheduled` / `Session-only data: records are lost on exit.` matches | 07 |
| `python -m pytest -q` | **31 passed in 0.32s** matches | 08 |

No files were changed, committed or pushed from the fresh copy.

## Console demo (section D), `python main.py --interactive`

Every one of the 21 rows matched the expected result.

| # | Input | Actual output | Match | Shot |
|---|---|---|---|---|
| 1 | 1: P1, Alex Example | Registered patient P1: Alex Example | Yes | 09 |
| 2 | 3: D1, Taylor Example, General | Registered practitioner D1: Taylor Example (General) | Yes | 09/10 |
| 3 | 3: D2, Morgan Example, General | Registered practitioner D2: Morgan Example (General) | Yes | 10 |
| 4 | 2: P1 | Found patient P1: Alex Example | Yes | 10 |
| 5 | 4: D1 | Found practitioner D1: Taylor Example (General) | Yes | 11 |
| 6 | 5: A1, P1, D1, 2026-10-01 09:00 | Booked A1: P1 with D1, 2026-10-01 09:00, scheduled | Yes | 11 |
| 7 | 5: A9, P1, D1, 2026-10-01 09:00 | Error: Practitioner already has a SCHEDULED appointment at this time | Yes | 11 |
| 8 | 5: A2, P1, D2, 2026-10-01 09:00 | Booked A2: P1 with D2, 2026-10-01 09:00, scheduled | Yes | 12 |
| 9 | 7: A9 | Error: Appointment not found | Yes | 12 |
| 10 | 6: A1 | Cancelled A1: P1 with D1, 2026-10-01 09:00, cancelled | Yes | 13 |
| 11 | 6: A1 | Error: Only SCHEDULED appointments may be cancelled | Yes | 14 |
| 12 | 7: A1 | A1: P1 with D1, 2026-10-01 09:00, cancelled | Yes | 15 |
| 13 | 8: D1, (blank) | A1: P1 with D1, 2026-10-01 09:00, cancelled | Yes | 16 |
| 14 | 8: D1, Scheduled | No matching appointments. | Yes | 17 |
| 15 | 8: D9, (blank) | Error: Practitioner not found | Yes | 18 |
| 16 | 8: D1, bogus | Error: Status must be blank, scheduled, cancelled or completed | Yes | 19 |
| 17 | 5: A4, P1, D1, 2026-13-01 09:00 | Error: Invalid calendar date/time; use YYYY-MM-DD HH:MM | Yes | 20 |
| 18 | 9 | Unknown option; choose 0-8. | Yes | 21 |
| 19 | 5: A3, P1, D1, 2026-10-01 09:00 | Booked A3: P1 with D1, 2026-10-01 09:00, scheduled | Yes | 22 |
| 20 | 8: D1, (blank) | A1 ... cancelled, then A3 ... scheduled (time, then ID) | Yes | 23 |
| 21 | 0 | Goodbye. Session-only data: records are lost on exit. | Yes | 24 |

After every error the menu carried on, and no record was created or changed.

## Answers

**Did I only need the README to set up and run it?**
Mostly yes. The only things I needed beyond `project/README.md` were the commands to create and activate a virtual environment, plus the Windows workaround in finding 1.

**Was anything missing, wrong or confusing in the README?**
1. **Windows activation blocked:** `.venv\Scripts\Activate.ps1` failed with "running scripts is disabled on this system". It worked after `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, which only applies to that PowerShell window and changes no files. (Screenshot 03)
2. **No venv commands:** "Environment" says "Activate your virtual environment first" but doesn't say how. Suggest adding `python -m venv .venv`, then Windows `.venv\Scripts\Activate.ps1` and Mac `source .venv/bin/activate`, and a note about finding 1.
3. **Slightly confusing wording:** "Running SmartCare" says "All commands run from this `project/` directory", but the first command is `cd project` (and the last is `cd ..`), so the block actually starts at the repo root. Suggest "From the repository root:".
4. **Observation, not a defect:** in row 14 I typed `Scheduled` with a capital S and it was accepted, so status input is case-insensitive. The README only shows lowercase, which is fine; mention it if you like.

**Did any step not match the "Expected" column?**
No. All setup checks and all 21 demo rows matched. The only extra step was the Windows activation workaround.

**Code defects found:** none.
