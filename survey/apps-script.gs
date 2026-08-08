/**
 * Backend for the Cuba family experience survey (2019–2026).
 *
 * DEPLOY
 * 1. Create a private Google Sheet (only you have access).
 * 2. Extensions → Apps Script → paste this file → Save.
 * 3. Deploy → New deployment → Web app → Execute as ME, Access ANYONE.
 * 4. Copy the /exec URL into survey/index.html (ENDPOINT).
 * 5. Optional: Project settings → Script properties → ADMIN_KEY = long random string
 *    (enables read-only stats via doGet; see README).
 *
 * WHERE RESPONSES GO
 * - Valid rows  → Sheet tab "responses" (private; never publish this Sheet).
 * - Rejected    → Sheet tab "audit" (reason + timestamp only; no payload stored).
 * - Weekly roll-up → run refreshSummary() manually or on a time trigger.
 *
 * Field names in index.html MUST match FIELDS below exactly and in this order.
 */

var SHEET_NAME = 'responses';
var AUDIT_SHEET = 'audit';
var SUMMARY_SHEET = 'summary';

var MIN_SECONDS = 15;
var MAX_SECONDS = 7200;       // 2 h — replay / automated sessions
var MAX_PER_TOKEN = 2;          // same browser, max 2 stored (was 3)
var MAX_ROWS_PER_DAY = 250;     // global flood cap (raise if viral)

var FIELDS = [
  'received_utc', 'token', 'elapsed_s',
  'resides', 'province_group', 'left_year', 'age_band',
  'uncles_aunts', 'cousins', 'children',
  'fam_left_2019_2026', 'fam_died_2019_2026', 'fam_died_60plus',
  'consent'
];

var ENUMS = {
  resides: ['cuba', 'abroad'],
  province_group: ['occidente', 'habana', 'centro', 'oriente', 'isla', 'na'],
  left_year: ['', 'pre2019', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026'],
  age_band: ['15_29', '30_44', '45_59', '60_74', '75plus']
};

var NUM_LIMITS = {
  uncles_aunts: [0, 80],
  cousins: [0, 200],
  children: [0, 25],
  fam_left_2019_2026: [0, 200],
  fam_died_2019_2026: [0, 200],
  fam_died_60plus: [0, 200]
};

// ── Public write endpoint (form POST) ─────────────────────────────────────

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    if (p.website) return _drop('honeypot');
    if (p.consent !== 'yes') return _drop('no_consent');

    var elapsed = Number(p.elapsed_s || 0);
    if (elapsed < MIN_SECONDS) return _drop('too_fast');
    if (elapsed > MAX_SECONDS) return _drop('too_slow');

    if (!_validToken(p.token)) return _drop('bad_token');

    var err = _validatePayload(p);
    if (err) return _drop(err);

    var lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      var sh = _sheet(SHEET_NAME, FIELDS);
      if (_tokenCount(sh, p.token) >= MAX_PER_TOKEN) return _drop('token_cap');
      if (_todayCount(sh) >= MAX_ROWS_PER_DAY) return _drop('daily_cap');

      var row = FIELDS.map(function (f) {
        if (f === 'received_utc') return new Date().toISOString();
        if (f === 'elapsed_s') return String(elapsed);
        return (p[f] === undefined) ? '' : String(p[f]).slice(0, 200);
      });
      sh.appendRow(row);
    } finally {
      lock.releaseLock();
    }
    return _ok('stored');
  } catch (err) {
    _audit('error');
    return _ok('error');
  }
}

// ── Optional read-only stats (owner only if ADMIN_KEY set) ────────────────

function doGet(e) {
  var p = (e && e.parameter) ? e.parameter : {};
  var key = PropertiesService.getScriptProperties().getProperty('ADMIN_KEY');
  if (!key || p.key !== key) {
    return ContentService.createTextOutput('ok').setMimeType(
      ContentService.MimeType.TEXT);
  }
  return ContentService.createTextOutput(JSON.stringify(refreshSummary(), null, 2))
    .setMimeType(ContentService.MimeType.JSON);
}

// ── Run from Apps Script editor: weekly check or time-driven trigger ───────

function refreshSummary() {
  var sh = _sheet(SHEET_NAME, FIELDS);
  var last = sh.getLastRow();
  var n = Math.max(0, last - 1);
  var stats = {
    updated_utc: new Date().toISOString(),
    total_stored: n,
    target_n: 200,
    target_on_island: 80,
    by_resides: { cuba: 0, abroad: 0, other: 0 },
    last_7_days: 0,
    median_fam_left: null,
    median_fam_died: null
  };

  if (n === 0) {
    _writeSummary(stats);
    return stats;
  }

  var data = sh.getRange(2, 1, last, FIELDS.length).getValues();
  var col = {};
  FIELDS.forEach(function (f, i) { col[f] = i; });

  var lefts = [];
  var dieds = [];
  var weekAgo = Date.now() - 7 * 86400000;

  for (var i = 0; i < data.length; i++) {
    var row = data[i];
    var res = row[col.resides];
    if (res === 'cuba') stats.by_resides.cuba++;
    else if (res === 'abroad') stats.by_resides.abroad++;
    else stats.by_resides.other++;

    var ts = Date.parse(row[col.received_utc]);
    if (!isNaN(ts) && ts >= weekAgo) stats.last_7_days++;

    lefts.push(Number(row[col.fam_left_2019_2026]));
    dieds.push(Number(row[col.fam_died_2019_2026]));
  }

  lefts.sort(function (a, b) { return a - b; });
  dieds.sort(function (a, b) { return a - b; });
  stats.median_fam_left = _median(lefts);
  stats.median_fam_died = _median(dieds);

  _writeSummary(stats);
  return stats;
}

function auditReport() {
  var sh = _sheet(AUDIT_SHEET, ['received_utc', 'reason']);
  var last = sh.getLastRow();
  if (last < 2) return { total_dropped: 0, by_reason: {} };
  var data = sh.getRange(2, 1, last, 2).getValues();
  var by = {};
  for (var i = 0; i < data.length; i++) {
    var r = String(data[i][1]);
    by[r] = (by[r] || 0) + 1;
  }
  return { total_dropped: data.length, by_reason: by };
}

// ── Validation ───────────────────────────────────────────────────────────

function _validatePayload(p) {
  for (var k in ENUMS) {
    var v = (p[k] === undefined) ? '' : String(p[k]);
    if (ENUMS[k].indexOf(v) === -1) return 'bad_enum_' + k;
  }
  if (p.resides === 'cuba' && p.left_year && p.left_year !== '' && p.left_year !== 'pre2019') {
    return 'cuba_left_year';
  }
  for (var field in NUM_LIMITS) {
    if (!_validInt(p[field], NUM_LIMITS[field][0], NUM_LIMITS[field][1])) {
      return 'bad_num_' + field;
    }
  }
  if (Number(p.fam_died_60plus) > Number(p.fam_died_2019_2026)) {
    return 'dead_60_gt_total';
  }
  return null;
}

function _validInt(v, lo, hi) {
  if (v === '' || v === undefined) return false;
  var n = Number(v);
  return n === Math.floor(n) && n >= lo && n <= hi;
}

function _validToken(t) {
  if (!t || typeof t !== 'string') return false;
  t = t.trim();
  return t.length >= 16 && t.length <= 64 && /^[a-zA-Z0-9-]+$/.test(t);
}

// ── Sheets helpers ─────────────────────────────────────────────────────────

function _sheet(name, header) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    sh.appendRow(header);
  }
  return sh;
}

function _audit(reason) {
  var sh = _sheet(AUDIT_SHEET, ['received_utc', 'reason']);
  sh.appendRow([new Date().toISOString(), String(reason).slice(0, 80)]);
}

function _drop(reason) {
  _audit(reason);
  return _ok('dropped');
}

function _tokenCount(sh, token) {
  if (!token) return 0;
  var last = sh.getLastRow();
  if (last < 2) return 0;
  var col = FIELDS.indexOf('token') + 1;
  var vals = sh.getRange(2, col, last, col).getValues();
  var n = 0;
  for (var i = 0; i < vals.length; i++) {
    if (vals[i][0] === token) n++;
  }
  return n;
}

function _todayCount(sh) {
  var last = sh.getLastRow();
  if (last < 2) return 0;
  var col = FIELDS.indexOf('received_utc') + 1;
  var vals = sh.getRange(2, col, last, col).getValues();
  var today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
  var n = 0;
  for (var i = 0; i < vals.length; i++) {
    var s = vals[i][0];
    if (!s) continue;
    var d = s instanceof Date ? s : new Date(s);
    if (Utilities.formatDate(d, Session.getScriptTimeZone(), 'yyyy-MM-dd') === today) n++;
  }
  return n;
}

function _writeSummary(stats) {
  var sh = _sheet(SUMMARY_SHEET, ['key', 'value']);
  sh.clearContents();
  sh.appendRow(['key', 'value']);
  sh.appendRow(['updated_utc', stats.updated_utc]);
  sh.appendRow(['total_stored', stats.total_stored]);
  sh.appendRow(['target_n', stats.target_n]);
  sh.appendRow(['target_on_island', stats.target_on_island]);
  sh.appendRow(['on_island', stats.by_resides.cuba]);
  sh.appendRow(['abroad', stats.by_resides.abroad]);
  sh.appendRow(['last_7_days', stats.last_7_days]);
  sh.appendRow(['median_fam_left', stats.median_fam_left]);
  sh.appendRow(['median_fam_died', stats.median_fam_died]);
}

function _median(sorted) {
  if (!sorted.length) return null;
  var m = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[m] : (sorted[m - 1] + sorted[m]) / 2;
}

function _ok(status) {
  return ContentService.createTextOutput(JSON.stringify({ status: status }))
    .setMimeType(ContentService.MimeType.JSON);
}
