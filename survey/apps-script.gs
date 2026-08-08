/**
 * Backend for the Cuba family experience survey (2019–2026).
 *
 * Deploy: Extensions > Apps Script from the target Sheet, paste this, then
 * Deploy > New deployment > Web app, "Execute as: Me",
 * "Who has access: Anyone". Copy the /exec URL into index.html (ENDPOINT).
 *
 * Field names in index.html MUST match FIELDS below exactly and in this order.
 */

var SHEET_NAME = 'responses';
var MIN_SECONDS = 15;
var MAX_PER_TOKEN = 3;

var FIELDS = [
  'received_utc', 'token', 'elapsed_s',
  'resides', 'province_group', 'left_year', 'age_band',
  'uncles_aunts', 'cousins', 'children',
  'fam_left_2019_2026', 'fam_died_2019_2026', 'fam_died_60plus',
  'consent'
];

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};

    if (p.website) return _ok('dropped');
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
    return _ok('error');
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
