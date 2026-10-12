# ARK-OS Security Policy

## Overview

ARK-OS is an operating-system project currently in the initial architectural baseline stage. The repository contains component specifications and directory organization, but does not yet contain executable code, running daemons, or deployed system images.

This policy defines the security expectations, intended vulnerability handling process, scope, and known architectural security limitations for the project.

---

## Reporting a Vulnerability

### Reporting Channel

- **Status:** Unresolved
- **Designated Contact:** Not currently configured in the repository.

There is currently no dedicated security email address, PGP key, or private disclosure platform established for ARK-OS. Do not report sensitive vulnerabilities via public issue trackers or pull requests.

Until an official security contact is established by the project maintainers, security disclosures must be directed to the repository owner or primary maintainer through private repository channels if available.

### Required Details

When submitting a security report, provide:

1. A clear description of the vulnerability, design flaw, or memory-safety hazard.
2. The affected component, file, or architectural specification.
3. Steps to reproduce the vulnerability, a proof of concept, or an explanation of the theoretical exploit mechanism.
4. An assessment of the potential impact on system isolation, memory integrity, or privilege boundaries.

### Response and Disclosure Expectations

- **Response Time Guarantee:** None currently established.
- **Bug Bounty Program:** No bug bounty or financial compensation program exists for this project.
- **Coordinated Disclosure:** The project aims to follow coordinated vulnerability disclosure. Maintainers will review reports, verify their impact against the architecture or implementation, and coordinate remediation prior to public disclosure.

---

## Vulnerability Scope

| Area / Component | Current Status | Security Scope |
| :--- | :--- | :--- |
| Core Architecture Specifications | Implemented | Architectural flaws, privilege escalation designs, or unsafe IPC models |
| `components/runtime/arkrt` | Planned | Process management isolation, PID 1 signal safety, virtual filesystem permissions |
| `components/libraries/libark` | Planned | Buffer overflows, memory safety invariants, unsafe pointer handling |
| `components/shell/sash` | Planned | Command injection, environment variable leakage, file descriptor leakage |
| `host-tools/signing` | Planned | Key management, trust anchors, signature verification logic |
| External Upstream Dependencies | External | Must be reported directly to upstream vendors (e.g., Linux kernel, Swift project) |

---

## Intended Trust Boundaries

When components are implemented, ARK-OS intends to enforce the following trust boundaries:

1. **Kernel vs. Userspace:** The Linux kernel operates in privileged supervisor mode. All ARK-OS userspace processes run unprivileged in user mode.
2. **System Runtime (`arkrt`):** Executes with required system supervisor privileges to manage process lifecycles and early boot mounting. Drops privileges where possible.
3. **System Daemons (`components/services`):** Each daemon executes under dedicated unprivileged system users with narrowly scoped capabilities.
4. **Applications (`components/apps`):** Sandboxed user applications isolated from raw system resources and direct inter-process memory sharing.
5. **Host vs. Target:** Development tools running on the host (`host-tools/`, `devtools/`) are strictly separated from target code to prevent host contamination.

---

## Known Security Limitations

The following limitations currently exist and must be recognized:

- **No Executable Code:** No cryptographic verification, sandbox enforcement, or runtime permission checking is currently implemented or functional.
- **No Secure Boot or Verified Boot:** While cryptographic image signing is planned via `host-tools/signing`, there is no verified boot chain, TPM measurement, or hardware root-of-trust integration currently in place.
- **No Hardened Kernel Profiles:** No SELinux, AppArmor, or Seccomp profiles are currently defined or enforced.
- **No Automated Vulnerability Scanning:** No static analysis, fuzzing, or dependency vulnerability scanning is active in repository continuous integration workflows.

Users and developers must not treat ARK-OS as hardened, production-ready, or suitable for security-sensitive workloads.
