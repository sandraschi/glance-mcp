# Why glance-mcp does not ship TV Tropes / Anna’s Archive scrapers

## TV Tropes (`tvtropes.org`)

The site is **hostile to automated access** (rate limits, structural changes, and terms that discourage bulk scraping). Building a “friendly” MCP on top of **roboscraping** would be brittle, rude to operators, and a maintenance trap. A legitimate integration would need **official API or explicit permission** — neither is a stable public option today.

**Alternatives:** Use the **MediaWiki API** on wikis that expose it, or link users to **manual** pages (open in browser) from your agent.

## Anna’s Archive

Aggregates **copyright-sensitive** material. An MCP that automates search/download could **facilitate misuse** and create **legal and platform risk** for users and maintainers. **Not in scope** for this fleet’s utilities.

That is a **product and risk posture** choice, not a claim about what is or is not lawful where you live. Enforcement and private-party risk (rightsholders, platforms) vary widely.

### Legal disclaimer (not legal advice)

This document is **general information**, not legal advice. Laws change; courts disagree; facts matter. **Consult a qualified lawyer** for your situation. The authors and maintainers are **not** responsible for how you use third-party sites or tools.

### Hosting and platform reality (GitHub, US)

- **GitHub** is operated from the **United States**. Repository content and issues are subject to **GitHub Terms of Service**, **DMCA** takedowns, and other US legal processes, **regardless of where contributors or users reside**.
- A project can be “international” in audience while still **subject to US platform rules** and **cross-border enforcement** (e.g. rightsholder complaints, account/repo restrictions).

### Why “it’s relaxed where I am” doesn’t settle it

- **Criminal vs civil vs platform risk** are different channels. Low public enforcement in one country does not eliminate **copyright claims**, **ISP/platform actions**, or **liability when traveling** or using US-hosted services.
- **EU / Austria:** National law implements the **copyright acquis**; exceptions (e.g. private copying where applicable) are **narrow and fact-specific**. “Authorities don’t prioritize X” is not the same as “lawful for every use case.”
- **Japan:** Rightsholders and publishers have been **aggressive** regarding unauthorized distribution of manga, light novels, and similar works; **personal use** vs **uploading/sharing** are treated differently. Do not assume other regions’ norms apply.
- **India:** Statutory text, case law, and enforcement **vary**; commercial scale and type of work matter. Treat any one-line summary as **non-authoritative**.
- **United States:** **Copyright** is federal; **DMCA** safe harbors apply to platforms, not a blanket license for users to infringe. **Willful** large-scale infringement can be criminal in some circumstances.

### Regional snapshot (illustrative only, non-exhaustive)

| Region | Rough theme (verify locally) |
|--------|------------------------------|
| EU (incl. AT) | Harmonized copyright rules + national exceptions; enforcement intensity differs by member state and rightsholder action. |
| US | Strong rightsholder tooling (DMCA); platform responses common. |
| Japan | High publisher sensitivity; manga/anime unauthorized sharing is a known enforcement focus. |
| India | Mixed; don’t infer from anecdotes—check current statute and your use case. |

If you need Anna’s Archive–class workflows, the **safe** pattern for an MCP is: **user-controlled** tools outside this repo, **explicit** user acknowledgment of risk, and **no** bundled automation that targets a specific grey aggregator unless you have **clear legal clearance**.

**See also (long-form, central hub):** [mcp-central-docs `integrations/annas-archive-mcp-stance.md`](https://github.com/sandraschi/mcp-central-docs/blob/master/integrations/annas-archive-mcp-stance.md) — MCP fit, public-domain vs in-copyright examples, PD-first alternatives (Gutenberg, Open Library, Internet Archive).

## Principle

**glance-mcp** sticks to **documented HTTP APIs**, **feeds users opt into**, and **local fleet probes** — not circumvention tooling.
