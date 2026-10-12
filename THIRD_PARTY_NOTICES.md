# Third-Party Notices and Disclaimers

## Overview

ARK-OS utilizes third-party open-source software and upstream tooling to build and run the operating system. This document tracks external components, their licensing terms, copyright notices, and compliance obligations.

---

## Current Repository Dependency Status

- **Vendored Sources:** None currently present in `external/` or any other repository directory.
- **Pinned Source Manifests:** `manifests/sources.lock.toml` is currently empty.
- **Active Third-Party Code:** No third-party source code, binary objects, or firmware blobs are currently committed to the repository.

---

## Planned Upstream Dependencies and Anticipated Obligations

When implementation proceeds and dependencies are retrieved or linked, the following licenses and compliance requirements will apply:

### 1. The Linux Kernel
- **Upstream Origin:** https://kernel.org
- **License:** GNU General Public License version 2 (GPL-2.0)
- **Source Pinning Status:** Unresolved (no specific kernel version or git tree pinned in `manifests/sources.lock.toml`).
- **Compliance Obligations:**
  - Complete, corresponding source code for any distributed kernel binary and modifications must be made available under GPL-2.0.
  - The Linux kernel COPYING and licensing files must accompany binary distributions.
  - User-space applications communicating strictly via standard Linux system call interfaces (`__NR_syscall`) are treated as normal userspace programs under the Linux system call exception (Linux syscall note).

### 2. The Swift Runtime and Standard Library
- **Upstream Origin:** https://github.com/swiftlang/swift
- **License:** Apache License 2.0 with LLVM Exception
- **Source Pinning Status:** Unresolved (no specific toolchain release pinned).
- **Compliance Obligations:**
  - Retention of copyright notices and license text.
  - Software built with Swift toolchains is exempt from requirements to provide source code under the LLVM Exception, but notices must be retained where applicable.

---

## Tracking and Maintenance Rules

As defined in [AGENTS.md](file:///home/aarav/repo/arkos/AGENTS.md) Section 10 and [docs/licensing/index.md](file:///home/aarav/repo/arkos/docs/licensing/index.md):

1. **Manifest Lock:** Every external dependency must be recorded with its upstream URL, pinned revision, and hash in `manifests/sources.lock.toml`.
2. **Notice Retention:** When third-party code is included or packaged into system images, its complete copyright notice and license text must be incorporated into this file or a generated software bill of materials (SBOM).
3. **Patch Tracking:** Local modifications to upstream projects must be tracked as explicit patch files in `external/` rather than undocumented direct edits.
4. **Legal Compliance:** The existence of this file does not certify full legal compliance. Full compliance requires ongoing verification whenever dependency revisions are pinned or updated.
