import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { prepareExistingReport } from './publish-report.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const docs = path.join(root, 'docs');
const sitePath = '/agent-acceleration-research/';
const siteOrigin = 'https://reading-site.invalid';
const problems = [];
const parsedFiles = new Map();
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const relative = file => path.relative(root, file).split(path.sep).join('/');
const problem = (location, message) => problems.push(`${location}: ${message}`);

function readJSON(file) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { problem(relative(file), error.message); return null; }
}

function inDirectory(base, file) {
  const rel = path.relative(base, file);
  return rel === '' || (!rel.startsWith(`..${path.sep}`) && rel !== '..' && !path.isAbsolute(rel));
}

function repositoryFile(value, label, base = root) {
  if (typeof value !== 'string' || !value || path.isAbsolute(value)) {
    problem(label, 'expected a nonempty relative file path');
    return null;
  }
  const file = path.resolve(base, value);
  if (!inDirectory(base, file)) {
    problem(label, 'file path leaves the expected directory');
    return null;
  }
  try {
    if (!fs.statSync(file).isFile()) throw new Error('not a file');
    return file;
  } catch (error) {
    problem(label, `missing file ${relative(file)} (${error.code || error.message})`);
    return null;
  }
}

// Decode entities in attribute values only. Formula text never enters URL checks.
function entities(text) {
  const named = { amp: '&', quot: '"', apos: "'", lt: '<', gt: '>', colon: ':', sol: '/', bsol: '\\', Tab: '\t', NewLine: '\n' };
  return text.replace(/&(#x[\da-f]+|#\d+|[A-Za-z]+);/gi, (whole, name) => {
    if (name[0] !== '#') return named[name] ?? whole;
    const number = name[1].toLowerCase() === 'x' ? parseInt(name.slice(2), 16) : parseInt(name.slice(1), 10);
    return Number.isInteger(number) && number > 0 && number <= 0x10ffff ? String.fromCodePoint(number) : '\ufffd';
  });
}

function attributes(tag, offset) {
  const result = new Map();
  const expression = /([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
  expression.lastIndex = offset;
  let match;
  while ((match = expression.exec(tag))) {
    const name = match[1].toLowerCase();
    if (!result.has(name)) result.set(name, entities(match[2] ?? match[3] ?? match[4] ?? ''));
  }
  return result;
}

// A tag scanner is sufficient here and avoids treating embedded JSON, JavaScript,
// CSS or escaped LaTeX as markup. In particular, a regex over the entire document
// would incorrectly inspect HTML snippets stored inside report data scripts.
function parseHTML(file) {
  if (parsedFiles.has(file)) return parsedFiles.get(file);
  const html = fs.readFileSync(file, 'utf8');
  const ids = new Set(), links = [], errors = [], executableScripts = [];
  let cursor = 0;
  while (cursor < html.length) {
    const start = html.indexOf('<', cursor);
    if (start < 0) break;
    if (html.startsWith('<!--', start)) {
      const close = html.indexOf('-->', start + 4);
      cursor = close < 0 ? html.length : close + 3;
      continue;
    }
    if (html.startsWith('<![CDATA[', start)) {
      const close = html.indexOf(']]>', start + 9);
      cursor = close < 0 ? html.length : close + 3;
      continue;
    }
    const match = /^<(\/?)([a-z][\w:-]*)\b/i.exec(html.slice(start));
    if (!match) { cursor = start + 1; continue; }
    let end = start + match[0].length, quote = '';
    for (; end < html.length; end++) {
      const char = html[end];
      if (quote) { if (char === quote) quote = ''; }
      else if (char === '"' || char === "'") quote = char;
      else if (char === '>') break;
    }
    cursor = end + 1;
    if (match[1]) continue;
    const tagName = match[2].toLowerCase();
    const attrs = attributes(html.slice(start, end), match[0].length);
    if (attrs.has('id')) ids.add(attrs.get('id'));
    if (tagName === 'a' && attrs.has('name')) ids.add(attrs.get('name'));
    if ((attrs.get('class') || '').split(/\s+/).includes('katex-error')) errors.push('KaTeX error element');
    for (const attribute of ['href', 'src', 'xlink:href']) {
      if (attrs.has(attribute)) links.push({ value: attrs.get(attribute), attribute, tagName });
    }
    if (['script', 'style', 'textarea', 'title'].includes(tagName)) {
      const close = new RegExp(`</${tagName}\\s*>`, 'ig');
      close.lastIndex = cursor;
      const closing = close.exec(html);
      if (tagName === 'script' && !attrs.has('src') && ['', 'module', 'text/javascript', 'application/javascript'].includes(attrs.get('type') || '')) {
        executableScripts.push(html.slice(cursor, closing ? closing.index : html.length));
      }
      cursor = closing ? close.lastIndex : html.length;
    }
  }
  if (/READERSLOT[A-Z0-9]/.test(html)) errors.push('unexpanded READERSLOT placeholder');
  const parsed = { html, ids, links, errors, executableScripts };
  parsedFiles.set(file, parsed);
  return parsed;
}

function localURL(file, value) {
  const base = siteOrigin + sitePath + path.relative(docs, file).split(path.sep).map(encodeURIComponent).join('/');
  let url;
  try { url = new URL(value, base); }
  catch { problem(relative(file), `invalid URL ${JSON.stringify(value)}`); return null; }
  const host = url.hostname.toLowerCase();
  if (url.protocol === 'file:' || /^(?:localhost|.*\.localhost|127(?:\.\d+){3}|0\.0\.0\.0|\[::1\])$/.test(host)) {
    problem(relative(file), `runtime local-machine URL in markup: ${JSON.stringify(value)}`);
    return null;
  }
  if (url.origin !== siteOrigin) return null; // External links are not fetched.
  if (!url.pathname.startsWith(sitePath)) {
    problem(relative(file), `local URL leaves the GitHub Pages project path: ${JSON.stringify(value)}`);
    return null;
  }
  let pathname, fragment;
  try {
    pathname = decodeURIComponent(url.pathname.slice(sitePath.length));
    fragment = decodeURIComponent(url.hash.slice(1));
  } catch {
    problem(relative(file), `invalid URL percent encoding: ${JSON.stringify(value)}`);
    return null;
  }
  let target = path.resolve(docs, pathname);
  if (!inDirectory(docs, target)) {
    problem(relative(file), `local URL resolves outside docs/: ${JSON.stringify(value)}`);
    return null;
  }
  try {
    if (fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
    if (!fs.statSync(target).isFile()) throw new Error('not a file');
  } catch {
    problem(relative(file), `missing local target ${JSON.stringify(value)} → ${relative(target)}`);
    return null;
  }
  if (fragment && /\.html?$/i.test(target) && !parseHTML(target).ids.has(fragment)) {
    problem(relative(file), `missing anchor ${JSON.stringify(fragment)} in ${relative(target)} (link ${JSON.stringify(value)})`);
  }
  return { target, fragment };
}

function htmlFiles(directory) {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(item => {
    const full = path.join(directory, item.name);
    return item.isDirectory() ? htmlFiles(full) : item.isFile() && /\.html?$/i.test(item.name) ? [full] : [];
  });
}

const catalog = readJSON(path.join(here, 'catalog.json'));
const manifest = readJSON(path.join(docs, 'site-manifest.json'));
let reportCount = 0, preservedReports = 0, localLinks = 0, totalLinks = 0, dynamicActionLinks = 0;
if (catalog && manifest) {
  if (!Array.isArray(catalog) || !Array.isArray(manifest.reports)) {
    problem('catalog/manifest', 'expected a catalog array and manifest.reports array');
  } else {
    const records = new Map();
    for (const record of manifest.reports) {
      if (records.has(record.slug)) problem('docs/site-manifest.json', `duplicate slug ${record.slug}`);
      records.set(record.slug, record);
    }
    const catalogSlugs = new Set();
    for (const entry of catalog) {
      const label = `catalog: ${entry.slug}`;
      if (catalogSlugs.has(entry.slug)) problem(label, 'duplicate slug');
      catalogSlugs.add(entry.slug);
      const record = records.get(entry.slug);
      if (!record) { problem(label, 'missing manifest record'); continue; }
      reportCount++;
      if (record.source !== entry.source) problem(label, 'manifest source differs from catalog');
      if (record.htmlSource !== (entry.htmlSource || null)) problem(label, 'manifest htmlSource differs from catalog');
      const source = repositoryFile(entry.source, label);
      const output = repositoryFile(entry.slug, label, docs);
      if (source && record.sourceHash !== hash(fs.readFileSync(source))) problem(label, 'sourceHash mismatch; source changed after build');
      if (output) {
        const bytes = fs.readFileSync(output);
        if (record.outputHash !== hash(bytes)) problem(label, 'outputHash mismatch; output changed after build');
        if (record.bytes !== bytes.byteLength) problem(label, 'output byte count differs from manifest');
      }
      if (entry.htmlSource) {
        const original = repositoryFile(entry.htmlSource, label);
        if (original) {
          const bytes = fs.readFileSync(original);
          if (record.htmlSourceHash !== hash(bytes)) problem(label, 'htmlSourceHash mismatch; existing report changed after build');
          if (output) {
            const expected = prepareExistingReport(entry, bytes.toString('utf8'));
            if (fs.readFileSync(output, 'utf8') !== expected) problem(label, 'published HTML differs from prepareExistingReport; original content preservation failed');
            else preservedReports++;
          }
        }
      } else if (record.htmlSourceHash !== null) problem(label, 'unexpected htmlSourceHash without htmlSource');
    }
    for (const slug of records.keys()) if (!catalogSlugs.has(slug)) problem('docs/site-manifest.json', `unexpected report ${slug}`);
  }
}

const files = htmlFiles(docs);
if (!files.length) problem('docs/', 'no HTML files; build the reading site first');
const homepageTargets = new Set();
const slideFiles = new Set(Array.isArray(catalog) ? catalog.filter(entry => entry.kind === 'slide' && entry.htmlSource).map(entry => path.resolve(docs, entry.slug)) : []);
for (const file of files) {
  const parsed = parseHTML(file);
  for (const error of parsed.errors) problem(relative(file), error);
  for (const link of parsed.links) {
    totalLinks++;
    if (!link.value.trim()) continue;
    // The existing slide deck uses #back as an action returning to lastMain.
    // It is not a fragment destination. Limit this exception to published slide
    // entries with the verified click handler; do not waive other missing IDs.
    if (slideFiles.has(file) && link.tagName === 'a' && link.attribute === 'href' && link.value === '#back' && parsed.executableScripts.some(script =>
      /document\.addEventListener\(\s*['"]click['"]/.test(script) &&
      /a\.getAttribute\(\s*['"]href['"]\s*\)\s*===\s*['"]#back['"]\s*\)\s*\{\s*e\.preventDefault\(\)\s*;\s*show\(lastMain\)/.test(script)
    )) {
      dynamicActionLinks++;
      continue;
    }
    const result = localURL(file, link.value);
    if (result) {
      localLinks++;
      if (file === path.join(docs, 'index.html') && link.attribute === 'href') homepageTargets.add(result.target);
    }
  }
}
if (!fs.existsSync(path.join(docs, 'index.html'))) problem('docs/index.html', 'homepage is missing');
if (Array.isArray(catalog)) for (const entry of catalog) {
  if (!homepageTargets.has(path.resolve(docs, entry.slug))) problem('docs/index.html', `missing report entry ${entry.slug}`);
}

if (problems.length) {
  console.error(`Reading site validation failed (${problems.length} problems):\n${problems.map(item => `- ${item}`).join('\n')}`);
  process.exitCode = 1;
} else {
  console.log(JSON.stringify({ ok: true, reports: reportCount, htmlFiles: files.length, preservedExistingReports: preservedReports, checkedMarkupURLs: totalLinks, localTargetsAndAnchors: localLinks, verifiedDynamicActionLinks: dynamicActionLinks, externalLinksFetched: 0 }, null, 2));
}
