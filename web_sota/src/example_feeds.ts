/**
 * Curated Atom/RSS URLs for demos (third-party sites; URLs may change — verify in browser).
 * Default example: Simon Willison (full blog Atom).
 */
export type ExampleFeed = {
  id: string;
  title: string;
  url: string;
  focus: string;
};

export const EXAMPLE_FEEDS: ExampleFeed[] = [
  {
    id: "simonwillison",
    title: "Simon Willison",
    url: "https://simonwillison.net/atom/everything/",
    focus: "LLMs, data, Django, tools",
  },
  {
    id: "schneier",
    title: "Bruce Schneier",
    url: "https://www.schneier.com/feed/",
    focus: "security, crypto, policy",
  },
  {
    id: "jvns",
    title: "Julia Evans",
    url: "https://jvns.ca/atom.xml",
    focus: "systems, debugging, zines",
  },
  {
    id: "danluu",
    title: "Dan Luu",
    url: "https://danluu.com/atom.xml",
    focus: "performance, eng culture",
  },
  {
    id: "rachelbythebay",
    title: "rachel by the bay",
    url: "https://rachelbythebay.com/w/feed",
    focus: "systems, stories",
  },
  {
    id: "pragmatic",
    title: "The Pragmatic Engineer",
    url: "https://blog.pragmaticengineer.com/rss/",
    focus: "Big Tech, eng practices",
  },
  {
    id: "krebs",
    title: "Krebs on Security",
    url: "https://krebsonsecurity.com/feed/",
    focus: "cybercrime, breaches",
  },
  {
    id: "fowler",
    title: "Martin Fowler",
    url: "https://martinfowler.com/feed.atom",
    focus: "architecture, refactoring",
  },
  {
    id: "hnrss",
    title: "Hacker News (front page via hnRSS)",
    url: "https://hnrss.org/frontpage",
    focus: "aggregator, not a personal blog",
  },
];

export const DEFAULT_EXAMPLE_FEED_URL = EXAMPLE_FEEDS[0].url;

/** Web reader “add subscription” URLs (raw Atom/RSS URLs are unreadable in a normal browser tab). */
export function feedlySubscribeUrl(feedUrl: string): string {
  return `https://feedly.com/i/subscription/feed/${encodeURIComponent(feedUrl)}`;
}

export function inoreaderSubscribeUrl(feedUrl: string): string {
  return `https://www.inoreader.com/feed/${encodeURIComponent(feedUrl)}`;
}
