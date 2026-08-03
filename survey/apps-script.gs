/**
 * Backend for the Cuba demography survey: appends one row per response to a
 * Google Sheet.
 *
 * Deploy: Extensions > Apps Script from the target Sheet, paste this, then
 * Deploy > New deployment > Web app, "Execute as: Me",
 * "Who has access: Anyone". Copy the /exec URL into index.html (ENDPOINT).
 *
 * PRIVACY — the design constraints, not decoration:
 *  - Apps Script cannot read the client IP, so no IP can reach the Sheet even
 *    by accident. (Google's own infrastructure logs still exist and are subject
 *    to legal process; that is unavoidable with any hosted backend and must be
 *    stated on the landing page.)
 *  - No field collects a name, address, municipality, or contact detail.
 *  - The Sheet must stay private. The deployment URL is a public WRITE endpoint;
 *    it is not a read endpoint, and doGet returns nothing useful.
 *
 * ABUSE — the endpoint is public, so:
 *  - a honeypot field ("website") must be empty;
 *  - responses completed in under MIN_SECONDS are dropped as bots;
 *  - a client-generated token allows duplicate detection without identifying
 *    anyone (it is random per browser, not per person).
 */

var SHEET_NAME = 'responses';
var MIN_SECONDS = 20;          // nobody answers this instrument honestly faster
var MAX_PER_TOKEN = 3;         // same browser resubmitting

var FIELDS = [
  'received_utc', 'token', 'elapsed_s',
  // respondent context (coarse by design — no municipality)
  'resides', 'province_group', 'left_year', 'age_band',
  // household roster anchored at Dec 2021
  'hh_2021', 'hh_now_abroad', 'hh_now_dead', 'hh_dead_60plus',
  // network scale-up: "how many people do you know who..."
  'net_size_known', 'net_left_since2021', 'net_died_2024_2025',
  'net_died_60plus_2024_2025',
  // NSUM calibration groups (known population sizes, used to estimate degree)
  'cal_teachers', 'cal_twins', 'cal_dialysis',
  // sibling survival (robust to the respondent's own migration)
  'sibs_born', 'sibs_alive', 'sibs_abroad',
  // free-form kept deliberately absent; only a coarse comment flag
  'consent'
];

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    if (p.website) return _ok('dropped');                       // honeypot
    if (Number(p.elapsed_s || 0) < MIN_SECONDS) return _ok('dropped');
    if (p.consent !== 'yes') return _ok('dropped');

    var lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      var sh = _sheet();
      if (_tokenCount(sh, p.token) >= MAX_PER_TOKEN) return _ok('dropped');
      var row = FIELDS.map(function (f) {
        if (f === 'received_utc') return new Date().toISOString();
        return (p[f] === undefined) ? '' : String(p[f]).slice(0, 200);
      });
      sh.appendRow(row);
    } finally {
      lock.releaseLock();
    }
    return _ok('stored');
  } catch (err) {
    return _ok('error');   // never leak a stack trace to a public endpoint
  }
}

function doGet() {
  return ContentService.createTextOutput('ok').setMimeType(
    ContentService.MimeType.TEXT);
}

function _sheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(FIELDS);
  }
  return sh;
}

function _tokenCount(sh, token) {
  if (!token) return 0;
  var last = sh.getLastRow();
  if (last < 2) return 0;
  var col = FIELDS.indexOf('token') + 1;
  var vals = sh.getRange(2, col, last - 1, 1).getValues();
  var n = 0;
  for (var i = 0; i < vals.length; i++) if (vals[i][0] === token) n++;
  return n;
}

function _ok(status) {
  return ContentService.createTextOutput(JSON.stringify({ status: status }))
    .setMimeType(ContentService.MimeType.JSON);
}
