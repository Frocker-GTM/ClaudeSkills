# Randi Does Market Research

A Claude skill that tests what a company says about its product, the way James Randi tested psychics: agree on the test conditions first, then check the claim against evidence.

## What it does

Pick one product. The skill records what the company says about it, locks a pass/fail standard with you before any research starts, then tests four things:

1. **The claim** you want to check (or one it proposes)
2. **ICP experience:** do the customers the company targets actually enjoy the product?
3. **Core messaging:** is the main promise true?
4. **Differentiators:** are the claimed strengths real, and actually unique?

Each test gets one of three verdicts: **Validated**, **Plausible Unconfirmed**, or **Invalidated**. Every source is logged, both for and against.

## What you get

- A JSON file with every finding, source, date, and verdict
- A drill-in HTML viewer: the company's story on top, one card per test below, each opening to its standard, reasoning, and sources

## How it works

1. **Staging.** You name the company, product, and (optionally) a claim.
2. **The company's story.** Claude gathers the ICP, messaging, tone and voice, and differentiators from company-owned sources only. You confirm or correct.
3. **Test conditions.** Claude proposes what each verdict would require. You lock the standards. They don't change once testing starts.
4. **Testing.** Claude searches for evidence in both directions and assigns verdicts strictly against the locked standards.
5. **Build.** With your permission, Claude builds the viewer.

You approve at three checkpoints. Nothing moves forward without you.

## Rules the skill follows

- **One product per run.** Start a new conversation for the next one.
- **The burden of proof is on the company.** A claim with no independent evidence is Plausible Unconfirmed, not Validated.
- **Fair test.** It searches as hard for validation as for invalidation.
- **Vendor-funded research counts as a company claim**, not independent proof.
- **Constructive framing.** Findings describe customer problems and outcomes, not attacks on the company.

## Install

**Claude.ai or Claude Desktop:** Zip the `randi-does-market-research` folder, then upload the zip in your Skills settings. Code execution must be turned on.

**Claude Code:** Copy the `randi-does-market-research` folder into `~/.claude/skills/`.

## Use it

Say "do a Randi" or "Randi Does Market Research," or ask Claude to test, verify, or fact-check a product claim. It also works for competitive intel and interview prep.

## Requirements

Python 3, used by `scripts/build_viewer.py` to build the viewer. Claude runs it in its own environment.

## Credit

Named for James "The Amazing" Randi (1928 to 2020), magician and skeptic. Through his One Million Dollar Paranormal Challenge, claimants agreed in advance on what success and failure would look like, so a failed test couldn't be explained away afterward. This skill applies his method to product marketing.

## Author

Bryan Finfrock · [LinkedIn](https://www.linkedin.com/in/bryanfinfrock/)
