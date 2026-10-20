# Crew Math

Staffing and rota arithmetic. Keeping 2 posts staffed 24 hours a day, 7 days a week is 336 hours a week, which takes 9 people at 40 hours each.

## What it computes

All inputs are whole numbers.

- **The cover truth** - the hours a week that posts need (posts 1 to 50, hours a day 1 to 24, days a week 1 to 7), the people needed at a number of hours each (1 to 80), and the spare hours across the team.
- **The rota truth** - crews (1 to 20) taking turns in blocks of 1 to 14 days: the rest length, the cycle length, the average days on duty a week, and how many days until the pattern lines up with the calendar week again.
- **The leave truth** - a team's average number on duty on a workday given leave days, the team size that keeps a chosen number on duty on average, and whether the team is over or short.

## Boundary

Arithmetic only. It adds up hours, days and people from the numbers the owner types. It does not know labour rules, contracts, breaks, skills, sickness or who may work when, and gives no verdict on whether any rota is legal, safe or fair. Leave that bunches up makes some days worse than the average.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers).
- `oracle.py` - the Python mirror (hands out hours one at a time, walks the rota day by day, searches the team size upward) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (214 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/crewmath/
Repo: https://github.com/iLanis-agent/crewmath
