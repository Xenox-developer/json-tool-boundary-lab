Can a tool call pass authorization and still execute different arguments?

I built a note-writing tool with one rule: create a new draft. A separate local executor also supported an outbox folder and overwriting an existing note.

The baseline deliberately used different JSON interpretations: the approval step kept the first occurrence of each key; execution kept the last. I compared it with rejecting duplicate keys and with parsing once, then authorizing and executing the same object.

Across 8 conflicting-duplicate inputs, forbidden file changes were:
• First-value approval / last-value execution: 8/8.
• Reject duplicates: 0/8.
• Parse once: 0/8.

Allowed writes across 8 benign inputs were 8/8, 4/8 and 8/8 respectively. All three produced zero forbidden changes on 4/4 negative controls.

One input repeated the folder key: draft first, outbox last. The baseline approved the draft interpretation and wrote to outbox. Escaping a letter in the repeated key did not change that outcome.

Duplicate rejection also discarded four benign inputs whose final interpretations were allowed. That is a compatibility choice in this fixture set, not a model accuracy score.

The run covered 60 sequential cases and 28 actual file writes. A separate auditor checked every input, decision and before/after file snapshot. All effects stayed in temporary test folders; nothing was sent.

This is a constructed Python 3.12.1 boundary test, not a finding in an MCP product or a deployment failure rate. No LLM generated the calls. Parsing once does not establish that the authorization policy itself is correct or protect later reparsing.

INVARIANT coordinated adapter implementation, 14 fixed checks and code review. Its first candidate was rejected before measurement; both attempts are retained.

Code, raw results and chart:
https://github.com/Xenox-developer/json-tool-boundary-lab

Tool — INVARIANT:
https://github.com/Xenox-developer/invariant

Primary references:
https://www.rfc-editor.org/rfc/rfc8259
https://docs.python.org/3.12/library/json.html
