# JSON tool-boundary lab

An original deterministic diagnostic of an intentionally mismatched approval/execution boundary. This is not a deployed-product finding or an MCP transport test. No LLM is called in the primary matrix.

## Question and design

A raw tool call has a name and three arguments. Policy allows only saving a new draft. The local executor can also simulate an outbox write or replacing an existing note; it never sends anything. Every path is hardcoded beneath a fresh temporary test directory.

Compare explicit first-occurrence approval followed by ordinary Python last-occurrence execution, recursive duplicate rejection, and one last-occurrence parse shared by approval/execution. The first design is deliberately constructed, not an allegation about any vendor. The other two differ in which duplicate-containing inputs they admit.

20 authored texts:8 conflicting-duplicate attacks,8 benign cases (4unique,4duplicates) and4 negative controls. Cross with3policies once each:60 sequential observations. Escaped aliases are compared after JSON decoding. These are coverage cases, not a sampled population. See PROTOCOL.md for the complete frozen contract and scope.

## Reproduce

Python3.12 standard library is sufficient for acceptance and audit. No packages or credentials for execution. All fixtures are original, synthetic and MIT licensed. Charts alone require Matplotlib.

```sh
python3 -B tests/check.py
python3 -B audit.py
```

To make a fresh primary run in a clean tested Git checkout after inspecting the protocol:

```sh
python3 -B run.py --out results/my-run
python3 -B audit.py results/my-run
```

Never overwrite results/primary or change frozen.json to make a modified implementation appear equivalent. The runner refuses an existing destination and requires unchanged frozen hashes and a clean Git state. Scientific frozen hashes include runner,auditor,implementation,tests,fixtures,protocol,order and source/version manifests. Issue records precede each invocation. Before/after file contents are saved as hexadecimal; events record callback arguments and actual target. Auditor imports none of adapter,sink or runner, independently reduces pair-preserving JSON trees and checks filesystem evidence and labels.

## Validation and limits

12fixed acceptance groups include input/schema/Unicode handling, direct forbidden controls, nested/escaped/equal duplicate semantics, same-object execution and callback-error propagation. A separate reference adapter passes the evaluator; a deliberately ungated control fails. Control verdicts in evidence/grader-controls.json. INVARIANT's bounded semantic review is code review, not a separate scientific replication.

Host version and local decoder hash in evidence/versions.json. Online Python3.12 documentation may reflect a newer patch release. The baseline and both alternatives use the same decoder with explicit hooks. This does not test two deployed parser libraries, an LLM choosing calls, distributed handoff, human UI rendering, downstream reparsing, concurrent mutation or arbitrary executables. Parsing once only preserves the tested object's interpretation; trusted policy and execution containment still matter. No network, real messages, credentials or user data are used. No paid API calls or model downloads.

## Sources

Primary-source URLs, read scope and dates are recorded in SOURCES.json. RFC8259 describes duplicate-name interoperability; Python documents last-value behavior. MCP tools only motivates the validation/authorization boundary. The Check Point article motivated candidate discovery; this is not a replication of its LLM guardrail experiment.

## Results

Pending primary measurement. No numbers are claimed before the frozen run.
