---
name: randi-does-market-research
description: >
  Tests what a company says about one of its products the way James Randi tested psychics: agree on the test conditions first, then check the claim against evidence. Stages the company's own story (ICP, core messaging, tone and voice, claimed differentiators, what it says about a claim), locks a falsification standard with the user, then tests the claim, whether the ICP enjoys the product, whether the core messaging is true, and whether the differentiators are real. Verdicts are Validated, Plausible Unconfirmed, or Invalidated, with every source logged for and against, delivered as JSON plus a published drill-in viewer. Use whenever the user wants to test, verify, fact-check, or disprove a product claim, messaging, or differentiator; asks "is this claim true" or "do customers really like X"; or says "do a Randi" or "Randi Does Market Research". Also for competitive intel and interview prep. One product per run.
---

# Randi Does Market Research

James Randi exposed charlatans by agreeing on the test conditions before the test. The claimant signed off on what success and failure would look like, so a failed result could not be explained away afterward. This skill does the same to product marketing: stage what the company says, agree on what would prove it true or false, then test it.

The goal is not to research everything. It is to test a small number of things the company says and reach a defensible verdict on each. Research that doesn't move a verdict is out of scope.

## Scope and working rules

- **One product per run.** For another product or competitor, start a fresh conversation. Mixing products conflates evidence.
- **Human in the loop.** Claude is the research assistant; the user is the product marketer. There are three required checkpoints (end of Stages 2, 3, and before Stage 5). Do not skip them.
- **Burden of proof sits on the company.** A claim with no independent evidence is not Validated. It is Plausible Unconfirmed.
- **Fair test.** Search for evidence that would validate the claim as hard as evidence that would invalidate it. A test that only looks one way is rigged, and a rigged test is worth nothing in front of a skeptical buyer or hiring manager.
- **Constructive framing.** Write findings around customer problems and outcomes ("Mid-market teams report migrations taking 3 to 6 months, against a promised 2 weeks"), never as attacks on the company.
- **House style for everything Claude writes into the JSON:** no em dashes, no filler ("unlock", "elevate", "seamless", "robust", "game-changer", "in today's landscape"). The build script flags both. The company's own quoted wording is exempt; it's evidence.

---

## Stage 1: Staging

Ask the user three things, in one message:

1. Which company?
2. Which product?
3. Which claim do you want to test? (Optional. "No specific claim" is a valid answer.)

If there is no specific claim, note that Stage 2 will spend extra effort on what the company says the product does and for whom, then propose candidate claims.

Do not research until you have at least the company and product.

---

## Stage 2: Initial pass (the company's own story)

This stage records what the company says. It does not judge it yet.

### Confirm the names first

Confirm the exact company name and product name as the company uses them today. Watch for renames, acquisitions, rebrands, and name collisions (a different company with the same name, which is common in analyst reports and review sites). If the names don't resolve cleanly, stop and ask.

### Where to look

Company-owned sources only in this stage:
- Resources or content library
- Blog
- Customer stories and case studies
- Product release notes, changelog, "what's new", launch announcements
- Product pages and anything describing how the product is used
- Help center, docs, and getting-started guides

### What to capture

1. **ICP** as the company describes it: industries, company size, buyer and user roles, use cases.
2. **Core messaging:** the main promise, in the company's own words. Record **tone and voice** in two or three sentences (formal or casual, technical or aspirational, confident or measured).
3. **Strengths and differentiators** the company claims. Capture all of them, numbered D1, D2, and so on.
4. **The claim:** everything the company has published about it, with sources.

**If there is no user-supplied claim:** go deeper on what the product does for whom. Then propose three to five candidate claims, each a single testable sentence tied to a source. Prefer claims that are specific, consequential to the buyer, and checkable ("Cuts page load times in half for high-traffic sites" beats "Built for the modern web").

Every item needs a source URL and a date where one is findable.

### Checkpoint 1

Present the findings in chat, compactly: names confirmed, ICP, core messaging with tone and voice, the full numbered differentiator list, and what the company says about the claim (or the candidate claims). Then ask:

- If there are candidate claims: which one to test.
- Which differentiators to test. Present every one; the user chooses. Recommend the two or three most consequential, but do not pre-filter the list.
- Any corrections.

Lock with: *"Respond with edits, or say 'confirmed' to lock this."*

---

## Stage 3: Test conditions

Before any testing, write the standard for each test. There is always:

- **T1 Claim:** the locked claim.
- **T2 ICP experience:** will the ICP actually enjoy using the product?
- **T3 Core messaging:** is the main promise true?
- **T4 onward, Differentiators:** one test per differentiator the user selected.

For each test, propose what **Validated**, **Plausible Unconfirmed**, and **Invalidated** would look like. A good standard is:
- **Observable.** It names the kind of evidence that counts (ICP-matched reviews, benchmark data, the company's own docs, release notes, independent coverage).
- **Thresholded.** It says how much is enough, using the evidence weights below.
- **Decisive.** Validated and Invalidated can't both be true at once, and Plausible Unconfirmed covers everything in between.

Example, for a differentiator "Only platform with native multi-region failover":
- Validated: independent sources (three or more) confirm the capability and no named competitor documents an equivalent.
- Invalidated: one or more competitors publicly document an equivalent capability, or the company's own docs limit it to a tier or region that contradicts "native".
- Plausible Unconfirmed: the capability is confirmed but uniqueness can't be established either way.

### The ICP experience standard

Sort ICP-matched customers into four types:

| Type | Enjoys the experience | Gets the outcome |
|---|---|---|
| Happy | Yes | Yes |
| Content | No | Yes |
| Frustrated | Yes | No |
| Angry | No | No |

Propose which pattern produces which verdict. Default proposal: Validated when Happy is the dominant pattern; Invalidated when Frustrated plus Angry dominate; Plausible Unconfirmed when Content dominates or no pattern emerges. The user can change it. Note that Content and Frustrated also tell you which half of the company's promise breaks: Content means the experience claims fail, Frustrated means the outcome claims fail.

### Checkpoint 2

Present all standards as a numbered list and lock with: *"Respond with edits, or say 'confirmed' to lock these standards."* Once locked, the standards do not change during testing. If testing shows a standard was badly written, flag it to the user; don't quietly reinterpret it.

---

## Stage 4: Testing

### Evidence rules

- **Weight.** One independent source is a signal. Three or more consistent independent sources are a finding. Verdicts of Validated or Invalidated normally rest on findings, not signals, unless the locked standard says otherwise.
- **Source types.** Tag each piece of evidence `independent`, `company`, or `vendor-funded`. Vendor-funded research (commissioned analyst studies, sponsored reports, paid reviews) counts as a company claim, never as independent validation. One exception on direction: a company's own docs, pricing, or release notes contradicting its marketing is strong evidence against the marketing.
- **Freshness.** Recent beats old. Record a date for every source. Older than 12 months is stale and gets flagged. Older than 24 months can support a verdict but cannot decide one alone.
- **Direction.** Every piece of evidence is tagged `validates`, `invalidates`, or `context`. Log both directions. The drill-down shows both sides; an empty "validates" column should mean you looked and found nothing, not that you didn't look.

### Where to look, by test

- **Claim, core messaging, differentiators:** independent reviews (G2, TrustRadius, Capterra, Gartner Peer Insights), independent benchmarks, trade press, analyst coverage (check who funded it), competitor documentation (for uniqueness claims), the company's own docs and release notes (for gaps between marketing and product), public status pages and incident history, community forums, Reddit, GitHub issues.
- **ICP experience:** reviews filtered to the claimed ICP's role, company size, and industry wherever the platform allows it. Community and forum threads from ICP-matched users. Help docs and support forums for friction signals (workarounds, long setup guides, recurring unanswered questions). Tag each item with its customer type: `happy`, `content`, `frustrated`, or `angry`. Exclude reviewers clearly outside the ICP, or tag them `context`.

### During testing

- Keep the search count proportionate. A test with a clean finding after a few searches is done.
- If something big invalidates a claim early, tell the user in chat before continuing.
- Assign each verdict strictly against its locked standard, and write one or two sentences of reasoning that cite the evidence that decided it.

When testing is complete, give a short chat summary: each test's verdict in one line, plus anything that surprised you. Then ask Checkpoint 3.

### Checkpoint 3

Ask permission before building: *"Ready to build the viewer? It will be a private link you can share."* Wait for a yes.

---

## Stage 5: Build and publish the viewer

The viewer has two layers:
- **Top: the stage.** Company, product, ICP, core messaging, tone and voice, claimed differentiators (tested ones marked), and what the company says about the claim.
- **Body: the tests.** One card per test with its verdict and a one-line bottom line. Each card drills in to the locked standard (with the met condition highlighted), the reasoning, and every source split into validates, invalidates, and context, newest first. The ICP experience test also shows the four customer types.

Steps:
1. Assemble the JSON per `references/data-schema.md`. A worked example is in `assets/example-data.json`.
2. Save to `/mnt/user-data/outputs/randi-mr-<company-slug>.json`.
3. Run `python <skill-dir>/scripts/build_viewer.py <data.json> <output.html>`. Fix every error. For warnings: rewrite em dashes and filler in your own prose, but leave the company's quoted language as published, since it's evidence; fill missing dates from what you found, never guess; for a verdict flagged as thin on evidence, either confirm the locked standard justifies it (and say so in `reasoning`) or change the verdict.
4. Publish the HTML with the Artifact tool if available; otherwise present it with `present_files`. Present the JSON with `present_files` either way. It is the source of truth for updates and for feeding battlecards, decks, or other downstream work.
5. In chat, two or three sentences: the strongest verdict, the weakest evidence, and anything the user should double-check. No recap of the research.

To update later, edit the JSON (or re-run one test) and rebuild. The viewer holds no logic the data doesn't carry.
