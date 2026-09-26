# Security Policy

## Supported versions

Security fixes go into the latest `v1` release of this action (currently `v1.0.0`), and the floating `v1` tag is moved to it. Pin the action to a full commit SHA if you need a fixed version.

## Reporting a vulnerability

**Please do not open a public issue, discussion or pull request for a security problem.**

Report it privately through GitHub: **Security → Advisories → "Report a vulnerability"** on this repository (<https://github.com/SigmaHQ/sigma-rules-validator/security/advisories/new>).
If you cannot use GitHub, open a public issue that says only that you have a security report and asks for a private contact. Do not include any details in that issue.

Please include:

- the action version or commit, the calling workflow snippet, and the input that reproduces the problem;
- the impact you see (see the scope below) and, if you have one, a proposed fix.

## What we treat as a vulnerability

This is a GitHub Action that validates Sigma rules against the Sigma JSON schema inside other projects' CI pipelines. It runs with the permissions of the calling workflow. The following are in scope:

- **Command or script injection:** action inputs, rule file names or rule content that can execute commands in the calling workflow.
- **Supply chain:** code, schemas or dependencies that the action downloads or installs at run time and that an outsider could replace, and weaknesses in how releases and tags of this action are published.
- **Privilege and secrets exposure:** steps that run with more privileges than needed or could expose the calling workflow's tokens or secrets.

**Out of scope (report publicly as bugs):**

- Rules that are wrongly accepted or rejected by the schema without a security impact. Schema issues belong in [SigmaHQ/sigma-specification](https://github.com/SigmaHQ/sigma-specification).

## Our process

| Step                                                                          | Target                                        |
| ----------------------------------------------------------------------------- | --------------------------------------------- |
| Acknowledge the report                                                        | within 5 working days                         |
| Initial assessment and severity (CVSS 3.1)                                    | within 14 days                                |
| Fix developed in the advisory's temporary private fork                        | as soon as practical, normally within 90 days |
| Coordinated release, then GitHub Security Advisory published (CVE via GitHub) | at the fix release                            |

- We credit reporters in the advisory unless they ask not to be credited.
- When a fix affects other SigmaHQ projects, we may coordinate their releases.
- We ask reporters to keep details private until the advisory is published or 90 days have passed, whichever comes first, unless agreed otherwise.
