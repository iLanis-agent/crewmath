#!/usr/bin/env python3
# Crew Math oracle - mirrors engine.js by simulation: hours are handed to people one at a time, the rotation is walked day by day against the weekday, and the team size is found by searching upward.
import json, re, random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

def num(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def pl(n, a, b): return f"{n} {a if n == 1 else b}"
def tenths(fr):
    s = format((Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP), "f")
    return s[:-2] if s.endswith(".0") else s

def cover(p, h, d, w):
    p = num(p, "the posts must be a whole number from 1 to 50", 1, 50)
    h = num(h, "the open hours per day must be a whole number from 1 to 24", 1, 24)
    d = num(d, "the open days per week must be a whole number from 1 to 7", 1, 7)
    w = num(w, "the hours per person per week must be a whole number from 1 to 80", 1, 80)
    cov = sum(h for _ in range(d) for _ in range(p))
    people = 0; held = 0
    while held < cov: people += 1; held += w
    spare = held - cov
    return f"Keeping {pl(p,'post','posts')} staffed {pl(h,'hour','hours')} a day, {pl(d,'day','days')} a week is {pl(cov,'hour','hours')} a week. At {pl(w,'hour','hours')} a person that takes {pl(people,'person','people')}, with {pl(spare,'spare hour','spare hours')} across the team."
def rot(n, b):
    n = num(n, "the crews must be a whole number from 1 to 20", 1, 20)
    b = num(b, "the block length must be a whole number from 1 to 14 days", 1, 14)
    if n == 1: return f"1 crew in blocks of {pl(b,'day','days')} covers every day, with no rest days."
    # walk days: crew 0 is on duty in block 0; find first day t>0 where the rotation position and weekday are both back at the start
    cycle = n * b; t = 0
    while True:
        t += 1
        if t % cycle == 0 and t % 7 == 0: break
    avg = tenths(Fraction(7, n))
    avg = avg + (" day" if avg == "1" else " days")
    return f"{pl(n,'crew','crews')} taking turns in blocks of {pl(b,'day','days')}: each crew works {pl(b,'day','days')} then rests {pl((n-1)*b,'day','days')}, a cycle of {pl(cycle,'day','days')}. A crew averages {avg} on duty a week. The pattern lines up with the calendar week again after {pl(t,'day','days')} ({pl(t//7,'week','weeks')})."
def leave(p, w, l, m):
    p = num(p, "the people must be a whole number from 1 to 1000", 1, 1000)
    w = num(w, "the workdays per person must be a whole number from 1 to 366", 1, 366)
    l = num(l, "the leave days must be a whole number from 0 to one less than the workdays", 0, w - 1)
    m = num(m, "the people to keep on duty must be a whole number from 1 to 1000", 1, 1000)
    avail = tenths(Fraction(p * (w - l), w))
    need = 1
    while need * (w - l) < m * w: need += 1
    tail = "You have exactly that many." if p == need else f"You have {p}, which is {p-need} more than that." if p > need else f"You have {p}, which is {need-p} short."
    return f"A team of {pl(p,'person','people')}, each taking {pl(l,'leave day','leave days')} out of {pl(w,'workday','workdays')}, has {avail} on duty on an average workday. To keep {m} on duty on an average workday takes {pl(need,'person','people')}. {tail}"

FNS = {"coverTruth": cover, "rotTruth": rot, "leaveTruth": leave}

def cases():
    c = []; rnd = random.Random(700)
    for a in [["2","24","7","40"],["1","1","1","1"],["1","8","5","40"],["1","8","5","8"],["1","8","5","7"],["3","12","7","36"],["50","24","7","1"],["50","24","7","80"],["1","24","7","80"],["2","24","7","41"],["1","8","5","80"],
              ["0","8","5","40"],["51","8","5","40"],["1","0","5","40"],["1","25","5","40"],["1","8","0","40"],["1","8","8","40"],["1","8","5","0"],["1","8","5","81"],["x","8","5","40"],["1","8","5",""],["1","8","5","4.5"],[" 2 "," 24 "," 7 "," 40 "],["-1","8","5","40"],["10000","8","5","40"]]:
        c.append(("coverTruth", a))
    for _ in range(25): c.append(("coverTruth", [str(rnd.randint(1,50)), str(rnd.randint(1,24)), str(rnd.randint(1,7)), str(rnd.randint(1,80))]))
    for n in range(1, 21):
        for b in (1, 3, 7, 14): c.append(("rotTruth", [str(n), str(b)]))
    for a in [["0","4"],["21","4"],["3","0"],["3","15"],["x","4"],["3",""],["3","1.5"],[" 3 "," 4 "]]: c.append(("rotTruth", a))
    for _ in range(20): c.append(("rotTruth", [str(rnd.randint(1,20)), str(rnd.randint(1,14))]))
    for a in [["20","230","25","15"],["10","230","25","15"],["17","230","25","15"],["16","230","25","15"],["1","1","0","1"],["1","2","1","1"],["2","2","1","1"],["1000","366","365","1000"],["1000","366","0","1000"],["1000","366","0","1"],["1","366","365","1"],["5","5","4","1"],["5","10","3","4"],["7","261","20","5"],
              ["0","230","25","15"],["1001","230","25","15"],["20","0","0","15"],["20","367","25","15"],["20","230","230","15"],["20","230","229","15"],["20","230","-1","15"],["20","230","25","0"],["20","230","25","1001"],["x","230","25","15"],["20","230","","15"],[" 20 "," 230 "," 25 "," 15 "]]:
        c.append(("leaveTruth", a))
    for _ in range(30):
        w = rnd.randint(1, 366); c.append(("leaveTruth", [str(rnd.randint(1,300)), str(w), str(rnd.randint(0, w-1)), str(rnd.randint(1,300))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
