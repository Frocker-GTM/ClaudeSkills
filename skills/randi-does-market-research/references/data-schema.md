# Data schema

The JSON file is the source of truth. The viewer renders it and holds no logic the data doesn't carry. Validate and build with `scripts/build_viewer.py`. A complete worked example is in `assets/example-data.json` (fictional, marked `fixture: true`).

## Top level

```json
{
  "meta": {},
  "stage": {},
  "tests": [],
  "open_questions": []
}
```

## meta

| Key | Type | Notes |
|---|---|---|
| `company_name` | string, required | As confirmed in Stage 2 |
| `product_name` | string, required | As confirmed in Stage 2 |
| `research_date` | string, required | `YYYY-MM-DD`. Freshness is measured from this date |
| `claim_origin` | `"user"` or `"proposed"`, required | Whether the user supplied the claim or picked it from Claude's candidates |
| `names_note` | string | Renames, acquisitions, or name collisions found while confirming names |
| `fixture` | boolean | True only for sample data. The viewer shows a banner |

## stage (the top of the viewer)

What the company says, recorded without judgment. Every section carries its own `sources`.

**Source** (used throughout `stage`):
```json
{ "source": "URL or description", "date": "YYYY-MM-DD or undated", "label": "optional short name" }
```

```json
{
  "claim": {
    "statement": "The claim under test, one sentence",
    "company_says": ["What the company has published about it"],
    "sources": [Source]
  },
  "icp": {
    "summary": "One or two sentences",
    "details": ["Industries, sizes, roles, use cases"],
    "sources": [Source]
  },
  "core_messaging": {
    "promise": "The main promise in the company's words",
    "supporting_lines": ["Secondary messages"],
    "tone_voice": "Two or three sentences",
    "sources": [Source]
  },
  "differentiators": [
    { "id": "D1", "statement": "string", "source": "URL or description", "date": "YYYY-MM-DD or undated" }
  ]
}
```

List every differentiator the company claims, tested or not. The viewer marks which ones have a test.

## tests (the body of the viewer)

Required: exactly one test of each kind `claim`, `icp_experience`, `core_messaging`, plus one `differentiator` test per differentiator the user selected. IDs are `T1`, `T2`, and so on.

```json
{
  "id": "T1",
  "kind": "claim | icp_experience | core_messaging | differentiator",
  "differentiator_id": "D2",
  "subject": "The statement being tested",
  "standard": {
    "validated": "What had to be true, as locked in Stage 3",
    "plausible_unconfirmed": "string",
    "invalidated": "string"
  },
  "verdict": "validated | plausible unconfirmed | invalidated",
  "bottom_line": "One sentence for the card",
  "reasoning": "One or two sentences citing the evidence that decided the verdict",
  "evidence": [Evidence]
}
```

- `differentiator_id` is required for `differentiator` tests and must match an id in `stage.differentiators`. Omit it otherwise.
- `standard` is copied exactly as locked. Don't edit it after the fact.

### Evidence

```json
{
  "finding": "What the source shows, framed around the customer problem or outcome",
  "direction": "validates | invalidates | context",
  "source_type": "independent | company | vendor-funded",
  "source": "URL or description",
  "date": "YYYY-MM-DD or undated",
  "sentiment": "happy | content | frustrated | angry",
  "notes": "optional"
}
```

- `sentiment` is required on `icp_experience` evidence whose direction is not `context`, and ignored elsewhere.
- Don't compute staleness. The build script adds `age` (`fresh`, `stale` over 12 months, `aged` over 24 months, or `undated`) from `research_date`.
- Don't sort. The build script orders evidence newest first, undated last.

## What the build script checks

Errors (no file written):
- Missing required keys, bad enums, bad dates.
- Test kinds missing or duplicated; a differentiator test pointing at an unknown `D#`.
- `icp_experience` evidence missing `sentiment`.
- A Validated or Invalidated verdict where every piece of evidence on the deciding side is over 24 months old. Aged evidence can support a verdict but can't decide one alone.

Warnings (decide on each):
- Em dashes or banned filler anywhere.
- Undated sources.
- Validated with fewer than three independent `validates` items, or Invalidated with fewer than three independent `invalidates` items and no company-owned contradiction. Either the locked standard allows it (say so in `reasoning`) or the verdict should be Plausible Unconfirmed.
- A test with no evidence at all.
- A test that has evidence on only one side. Confirm you looked for the other side.

## open_questions

Array of strings. Anything uncertain or worth the user's second look. Optional.
