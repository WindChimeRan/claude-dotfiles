---
name: bibtex-collector
description: Collect BibTeX entries from Google Scholar using the Chrome browser extension. Use when the user asks to find, collect, or add BibTeX entries for papers referenced in LaTeX files. CRITICAL - this skill enforces zero-hallucination by only using verbatim BibTeX from Google Scholar, never generating entries from memory.
user_invocable: true
---

# BibTeX Collector via Google Scholar + Chrome

## First Principle: ZERO HALLUCINATION

**Never compose, guess, or fill in any BibTeX field from memory.** Every BibTeX entry must be copied verbatim from Google Scholar's BibTeX export page. If you cannot obtain an entry from Scholar, STOP and tell the user. There is no fallback.

## When Things Go Wrong: STOP, Don't Improvise

At ANY point if you encounter:
- Chrome extension not responding or tab errors → STOP, tell user
- Google Scholar CAPTCHA or bot detection → STOP, tell user
- Paper not found on Google Scholar → STOP, tell user (do NOT try to write BibTeX yourself)
- Cite button or BibTeX link not working → STOP, tell user
- Ambiguous search results (not sure which paper is correct) → STOP, show user the candidates and ask
- Page not loading or timeout → STOP, tell user
- Any unexpected state → STOP, tell user

The user is a human who can help clear any blocker (dismiss CAPTCHAs, confirm the right paper, etc.). Always prefer stopping and asking over proceeding with uncertainty.

## Workflow

### Step 0: Identify Papers

Read the LaTeX source file the user specifies. Extract paper titles from footnotes (or wherever the user indicates). List them for the user to confirm before proceeding.

Typical footnote format:
```
\footnote{Author et al., ``Paper Title,'' Venue, Year.}
```

### Step 1: Set Up Chrome

1. Call `tabs_context_mcp` to check for existing tabs
2. If no usable tab exists, create one with `tabs_create_mcp`
3. Navigate to `https://scholar.google.com`
4. Take a screenshot to verify Scholar loaded
5. If Scholar did not load → STOP, tell user

### Step 2: Search for a Paper (repeat for each paper)

1. Find the search bar using `find` tool (query: "search bar")
2. Enter the paper title + first author last name + year using `form_input`
3. Click the search button or press Enter
4. Wait 3 seconds, then take a screenshot
5. **Verify the results:**
   - Check that search results loaded (not still on homepage)
   - Check that the first result matches the paper (title, author, venue)
   - If no match or ambiguous → STOP, show user the screenshot and ask

### Step 3: Get BibTeX

1. Click the "Cite" link (the quotation-mark icon with "Cite" text) under the correct result
2. Wait 2 seconds for the Cite dialog to appear
3. Take a screenshot to verify the dialog opened
4. Click the "BibTeX" link at the bottom of the Cite dialog
5. Wait 3 seconds for the BibTeX page to load
6. Use `get_page_text` to extract the BibTeX entry verbatim
7. **Verify:** The extracted text must start with `@` and look like valid BibTeX
8. If anything is wrong → STOP, tell user

### Step 4: Save to .bib File

1. Append the BibTeX entry to the target .bib file (default: `claude.bib` in the project root)
2. Format with proper indentation (2-space indent for fields)
3. Add a blank line between entries

### Step 5: Navigate Back

1. Navigate back to `https://scholar.google.com` for the next paper
2. If there's a popup/banner, dismiss it before searching

### Step 6: Report

After processing all papers (or stopping on an error), report to the user:
- Which entries were successfully added (with cite keys)
- Which entries failed and why
- Remind the user to verify all entries manually

## Output Format for .bib

```bibtex
@type{citekey,
  title={...},
  author={...},
  booktitle={...},
  pages={...},
  year={...}
}
```

All fields are exactly as Google Scholar provides them. Do not add, remove, or modify any fields.

## Important Notes

- Google Scholar may rate-limit after many searches. If searches start failing, STOP and tell the user to wait.
- Some papers (especially very recent preprints) may not be on Scholar yet. That's OK — just report it and skip.
- The footnote's author attribution may differ from Scholar (e.g., footnote says "Boudin et al." but Boudin is 4th author). Use Scholar's data as ground truth, but flag discrepancies to the user.
- Always take screenshots at key steps so the user can verify the process visually.
- Process papers one at a time. Do not batch or parallelize Scholar searches.
