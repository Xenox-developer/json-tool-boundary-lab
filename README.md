# JSON tool-boundary lab

An original deterministic diagnostic of an intentionally mismatched approval/execution boundary. This is not a deployed-product finding or an MCP transport test. No LLM is called in the primary matrix.

## Question and design

A raw tool call has a name and three arguments. Policy allows only saving a new draft. The local executor can also simulate an outbox write or replacing an existing note; it never sends anything. Every path is hardcoded beneath a fresh temporary test directory.

Compare explicit first-occurrence approval followed by ordinary Python last-occurrence execution, recursive duplicate rejection, and one last-occurrence parse shared by approval/execution. The first design is deliberately constructed, not an allegation about any vendor. The other two differ in which duplicate-containing inputs they admit.

20 authored texts: 8 conflicting-duplicate attacks, 8 benign cases (4 unique, 4 duplicates) and 4 negative controls. Cross with 3 policies once each: 60 sequential observations. Escaped aliases are compared after JSON decoding. These are coverage cases, not a sampled population. See PROTOCOL.md for the complete frozen contract and scope.

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

14 fixed acceptance groups include input/schema/Unicode handling, direct forbidden controls, nested/escaped/equal duplicate semantics, same-object execution and callback-error propagation. A separate reference adapter passes the evaluator; a deliberately ungated control fails. Control verdicts in evidence/grader-controls.json. INVARIANT's bounded semantic review is code review, not a separate scientific replication.

Host version and local decoder hash in evidence/versions.json. Online Python3.12 documentation may reflect a newer patch release. The baseline and both alternatives use the same decoder with explicit hooks. This does not test two deployed parser libraries, an LLM choosing calls, distributed handoff, human UI rendering, downstream reparsing, concurrent mutation or arbitrary executables. Parsing once only preserves the tested object's interpretation; trusted policy and execution containment still matter. No network, real messages, credentials or user data are used. No paid API calls or model downloads.

## Sources

Primary-source URLs, read scope and dates are recorded in SOURCES.json. RFC8259 describes duplicate-name interoperability; Python documents last-value behavior. MCP tools only motivates the validation/authorization boundary. The Check Point article motivated candidate discovery; this is not a replication of its LLM guardrail experiment.

## Results

| Policy | Forbidden changes /8 attack | Allowed writes /8 benign | Forbidden changes /4 negative |
| --- | ---: | ---: | ---: |
| First approval / last execution | 8/8 | 8/8 | 0/4 |
| Reject duplicate names | 0/8 | 4/8 | 0/4 |
| Parse once | 0/8 | 8/8 | 0/4 |

Completed 60/60 planned observations, 28 actual writes, no errors or omitted cells. Primary data in results/primary, independently recalculated results/audit.json, chart from plot.py. No primary reruns. Audit controls reject a missing observation, altered filesystem snapshot and altered approved object; intact evidence passes.

The four strict-mode benign rejections are duplicate-containing inputs. The first/last baseline admits all 8 conflicting pairs; this is an explicitly authored parser disagreement, not evidence that a deployed guard/executor uses this combination. Parsing once denies their final meanings under the trusted policy. It does not validate policy quality or downstream components.

## INVARIANT provenance

INVARIANT 0.3.1 coordinated native adapter implementation, protected acceptance evaluation, semantic review and guarded application. v1 study-3f988f3254de428eabc5dc79b592d600 passed 12 checks but review rejected uncaught deep-input RecursionError; not applied, primary had not started. v2 study-49c36459f52c4527ad9a19807f0ba2da passed 14 checks and semantic review, application verified. See evidence/invariant.json for exact prefixed IDs, hashes, receipts and verdicts. Added 2 regression groups before primary; fixed 20-case matrix unchanged. Original candidate and private native logs retained outside the public repository; sanitized structured receipts retain operational proof without unrelated runtime paths.

Total development across BOTH attempts: 4 native sessions, 11 individual model responses, 125326 returned tokens (122710 input, 2616 output; 66560 cached-input and 545 reasoning-output are subsets). Complete usage in evidence/development-usage.json. Native model gpt-6.1-terra, medium; current Codex subscription. Host chat usage unavailable. Zero measured LLM calls and no paid API calls. Session and response totals must not be added together.

Initial Docker network-pool preparation error occurred before task registration. After checking NOT_FOUND, retried the same request following reversible release of one demonstrably empty, unreferenced bridge. Its original equivalent settings were restored and verified after each native task. No container endpoints or references were affected. Private recovery inventories are excluded.

Premeasurement tested commit: 6752ef72a4dc20d6de71c14f0499b77a108b8e71. 14 frozen scientific hashes. Native adapter reviewed in full and 14 checks passed on host before primary. A fresh hosted clone must pass the same checks/audit before publication.

Tool:https://github.com/Xenox-developer/invariant

