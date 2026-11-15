# CausalEvidence Guard: protocol execution audit

![Reproducibility checks](https://github.com/javed110/protocol-execution-audit-demo/actions/workflows/checks.yml/badge.svg)

Synthetic Python demonstration of restricted protocol-to-execution auditing, amendment handling and artifact checks, with 9 tests.

**Scope:** an executable teaching and research-methods demonstrator using invented fixtures. Runs a narrow point-treatment fixture, records the actual supported configuration, input/code digests and selected synthetic IDs, and compares the receipt with independent local recomputation. It detects changed follow-up windows and changed artifacts, accepts a supplied approved amendment and refuses unsupported designs.

## Run

Python 3.10 or later; standard library only.

```text
python prototype.py
python -m unittest -v test_prototype.py
```

The demonstration prints synthetic examples to the terminal. It starts no server, contacts no service and writes no patient records.

## Example

```python
from prototype import fixture, run, audit
protocol, records = fixture()
receipt = run(protocol, records)
print(audit(protocol, receipt, records)["status"])  # pass
changed = dict(protocol, followup_days=60)
print(audit(protocol, run(changed, records), records)["status"])  # deviation
```

## What the checks establish

The 9 supplied tests check supported examples, refusal boundaries and relevant numerical or artifact edge cases. They were rerun on Python 3.12.14 for this public edition. CI repeats the tests and demonstration on Python 3.12. These are author-defined regression cases; no real-world accuracy or comparative superiority is established.

## Interpretation

Audit success establishes fidelity within the restricted local contract. It does not identify a causal effect, resolve confounding, implement an adjusted estimator, or provide secure remote attestation. Amendment authorization is supplied by the trusted local caller; there is no authenticated approval service.

Only the code, tests and necessary documentation are included. Application forms, personal contacts, unpublished manuscripts and private source-package history remain outside this edition.

## Provenance and credit

This edition preserves the original prototype and tests from the reviewed PCC26 preparatory package. [Source manifest](SOURCE_MANIFEST.json) records their source snapshot and byte hashes. Javed Ashraf maintains this repository. See [credit and rights](CREDIT_AND_RIGHTS.md) for the supplied project attribution and licensing status.

Related work: [synthetic healthcare workshop](https://github.com/javed110/synthetic-healthcare-ml-workshop), [health data science portfolio](https://github.com/javed110/health-data-science-portfolio).
