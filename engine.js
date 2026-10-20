// Crew Math engine: how many people a staffed post needs, how a rotation lines up with the week, and how leave shrinks a team. Exact integers.
function _int(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,4}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
function _gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
function _tenths(num, den) { // num/den to one decimal, half up, trailing .0 dropped
  var v = Math.floor((2 * num * 10 + den) / (2 * den));
  var f = v % 10, s = String(Math.floor(v / 10));
  return f === 0 ? s : s + "." + f;
}

function _avgDays(t) { return t + " " + (t === "1" ? "day" : "days"); }

function coverTruth(posts, hoursDay, daysWeek, weekHours) {
  var p = _int(posts, "the posts must be a whole number from 1 to 50", 1, 50);
  var h = _int(hoursDay, "the open hours per day must be a whole number from 1 to 24", 1, 24);
  var d = _int(daysWeek, "the open days per week must be a whole number from 1 to 7", 1, 7);
  var w = _int(weekHours, "the hours per person per week must be a whole number from 1 to 80", 1, 80);
  var cov = p * h * d, people = Math.floor((cov + w - 1) / w), spare = people * w - cov;
  return "Keeping " + _plural(p, "post", "posts") + " staffed " + _plural(h, "hour", "hours") + " a day, " + _plural(d, "day", "days") + " a week is " + _plural(cov, "hour", "hours") + " a week. At " + _plural(w, "hour", "hours") + " a person that takes " + _plural(people, "person", "people") + ", with " + _plural(spare, "spare hour", "spare hours") + " across the team.";
}
function rotTruth(crews, blockDays) {
  var n = _int(crews, "the crews must be a whole number from 1 to 20", 1, 20);
  var b = _int(blockDays, "the block length must be a whole number from 1 to 14 days", 1, 14);
  if (n === 1) return "1 crew in blocks of " + _plural(b, "day", "days") + " covers every day, with no rest days.";
  var cycle = n * b, rest = (n - 1) * b, repeat;
  repeat = cycle * 7 / _gcd(cycle, 7);
  return _plural(n, "crew", "crews") + " taking turns in blocks of " + _plural(b, "day", "days") + ": each crew works " + _plural(b, "day", "days") + " then rests " + _plural(rest, "day", "days") + ", a cycle of " + _plural(cycle, "day", "days") + ". A crew averages " + _avgDays(_tenths(7, n)) + " on duty a week. The pattern lines up with the calendar week again after " + _plural(repeat, "day", "days") + " (" + _plural(repeat / 7, "week", "weeks") + ").";
}
function leaveTruth(people, workDays, leaveDays, mustOn) {
  var p = _int(people, "the people must be a whole number from 1 to 1000", 1, 1000);
  var w = _int(workDays, "the workdays per person must be a whole number from 1 to 366", 1, 366);
  var l = _int(leaveDays, "the leave days must be a whole number from 0 to one less than the workdays", 0, w - 1);
  var m = _int(mustOn, "the people to keep on duty must be a whole number from 1 to 1000", 1, 1000);
  var avail = _tenths(p * (w - l), w);
  var need = Math.floor((m * w + (w - l) - 1) / (w - l));
  var tail = p === need ? "You have exactly that many." : p > need ? "You have " + p + ", which is " + (p - need) + " more than that." : "You have " + p + ", which is " + (need - p) + " short.";
  return "A team of " + _plural(p, "person", "people") + ", each taking " + _plural(l, "leave day", "leave days") + " out of " + _plural(w, "workday", "workdays") + ", has " + avail + " on duty on an average workday. To keep " + m + " on duty on an average workday takes " + _plural(need, "person", "people") + ". " + tail;
}
