# ARK-OS

ARK-OS is an independent operating-system project focused on building an understandable, maintainable, and developer-oriented operating system with a Swift-first userspace and a Linux kernel foundation.

The project is designed to combine the accessibility and cohesive user experience of modern consumer platforms with the transparency, openness, and customizability of a modular Unix-like system. Its architecture emphasizes strong process isolation, a minimal and audit-friendly system foundation, and deliberate separation between core system components.

ARK-OS is currently in an early architectural baseline stage. No source code, toolchain binaries, or bootable system images are implemented yet.

---

## Current Status

- **Status:** Architectural Baseline (Specification and Organization)
- **Source Code Implementation:** Not implemented
- **Build System Implementation:** Not implemented
- **Bootable Artifacts:** None
- **Initial Target Architecture:** x86_64 (Planned)
- **Secondary Target Architecture:** ARM64 (Future milestone, not yet implemented)

All component descriptions, interfaces, and boot flows in this repository represent architectural specifications and engineering intent. They do not represent functional software at this time.

---

## Architectural Principles

ARK-OS is structured around five core engineering principles:

1. **Linux Kernel Foundation:** Leverage the hardware support, driver ecosystem, and virtual memory capabilities of the Linux kernel rather than attempting an unverified custom kernel.
2. **Swift-First Userspace:** Implement core system libraries, process management, system services, and the default shell in Swift where technically suitable, maximizing safety, structured error handling, and maintainability.
3. **Strict Component Boundaries:** Maintain clear isolation between the kernel, the init process and runtime, shared system libraries, system daemons, user-facing shells, and applications.
4. **Minimal System Footprint:** Avoid unnecessary background daemons, complex legacy frameworks, and bloated dependencies. Keep each component small, auditable, and single-purpose.
5. **Verifiable Engineering:** Never claim functionality, performance, or security guarantees without concrete implementation and recorded verification.

---

## Repository Structure

The repository is organized into distinct areas of responsibility:

- `components/`: First-party operating system components.
  - `components/apps/`: Applications designed to execute on ARK-OS (Planned).
  - `components/boot/`: Boot integration and early system handoff assets (Planned).
  - `components/libraries/libark/`: Core first-party shared library providing system abstractions (Planned).
  - `components/runtime/arkrt/`: Primary system runtime and initialization process (PID 1) (Planned).
  - `components/services/`: First-party system daemons and background services (Planned).
  - `components/shell/sash/`: First-party command-line shell interface (Planned).
- `host-tools/`: Tools executed on the development host during system preparation.
  - `host-tools/aake/`: The ARK-OS compilation and build orchestration tool (Planned).
  - `host-tools/signing/`: Host-side cryptographic signing utilities (Planned).
- `devtools/`: Developer support scripts and static checks.
  - `devtools/check/`: Repository structure and formatting validation (Planned).
  - `devtools/release/`: Release preparation tooling (Planned).
- `docs/`: Canonical project documentation.
  - `docs/architecture/`: System design, component contracts, and boot architecture.
  - `docs/bringup/`: Platform bring-up guides for virtual and physical hardware.
  - `docs/decisions/`: Architecture Decision Records (ADRs) and unresolved decisions.
  - `docs/development/`: Contributor environment setup, workflows, and conventions.
  - `docs/licensing/`: Third-party compliance, legal obligations, and license tracking.
- `external/`: Tracking and coordination of upstream third-party dependencies.
- `manifests/`: Declarative component definitions, pinned source locks, and target profiles.
- `packaging/`: Root filesystem recipes and image assembly specifications.
- `sdk/`: Software development kit headers and target metadata (Planned).
- `tests/`: Unit, integration, and boot-stage verification test suites (Planned).

---

## Target Platforms

| Architecture | Target Profile | Status | Notes |
| :--- | :--- | :--- | :--- |
| x86_64 | `manifests/targets/x86_64.toml` | Planned | Primary development target under QEMU/KVM. |
| ARM64 | `manifests/targets/arm64.toml` | Planned | Future milestone; no active bring-up. |

---

## Development Prerequisites

When implementation begins, developing ARK-OS will require the following host environment components:

- **Host Operating System:** Linux (Ubuntu 22.04 LTS or newer, Debian 12 or newer, or compatible distribution)
- **Swift Toolchain:** Swift 5.10 or newer with static Linux SDK support
- **C/C++ Compiler:** Clang 16 or newer (or GCC 12 or newer)
- **Build Tools:** CMake 3.24+, Ninja 1.11+, and standard POSIX utilities
- **Emulation & Virtualization:** QEMU (`qemu-system-x86_64`) with KVM support
- **Image Utilities:** `mtools`, `parted`, and standard Linux filesystem tools

---

## Getting Started

Because ARK-OS is currently at the architectural baseline stage, there are no build artifacts to compile or execute.

Developers and contributors should begin by reviewing the project documentation:

1. **AI & Engineering Rules:** Read [AGENTS.md](file:///home/aarav/repo/arkos/AGENTS.md) for mandatory repository standards, safety invariants, and constraints.
2. **System Architecture:** Review [docs/architecture/overview.md](file:///home/aarav/repo/arkos/docs/architecture/overview.md) for component boundaries and execution flow.
3. **Component Documentation:** Inspect specifications in [docs/architecture/components/](file:///home/aarav/repo/arkos/docs/architecture/components/).
4. **Architectural Decisions:** Review accepted decisions and open questions in [docs/decisions/](file:///home/aarav/repo/arkos/docs/decisions/).
5. **Development Workflow:** Refer to [docs/development/index.md](file:///home/aarav/repo/arkos/docs/development/index.md) for contributor setup guidance.

---

## Verification and Testing

No automated builds, tests, or boot simulations are available at this time. 

All verification currently consists of static file inspection and documentation review. Commands that execute builds, test runs, or kernel boots must not be invoked until functional implementations and harnesses are committed and authorized.

---

## Governance and Licensing

- **License:** Apache License 2.0 (Copyright 2026 Aarav Ravindra Kharade). See [LICENSE](file:///home/aarav/repo/arkos/LICENSE) and [docs/licensing/index.md](file:///home/aarav/repo/arkos/docs/licensing/index.md).
- **Contributing:** See [CONTRIBUTING.md](file:///home/aarav/repo/arkos/CONTRIBUTING.md).
- **Security Policy:** See [SECURITY.md](file:///home/aarav/repo/arkos/SECURITY.md).
- **Credits & Attribution:** See [CREDITS.md](file:///home/aarav/repo/arkos/CREDITS.md).
