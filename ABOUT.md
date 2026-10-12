# ABOUT ARK-OS

## 1. Project Identity

ARK-OS is an independent operating-system development project focused on building a maintainable, transparent, developer-oriented operating system with a Swift-first userspace and a Linux-based foundation.

The project is intended to provide a coherent environment for systems programming, operating-system experimentation, software development, and deeper control over the software stack.

ARK-OS is a long-term engineering project. Its architecture, implementation, supported hardware, and feature set must be documented according to what has actually been implemented and verified, not what is merely planned.

## 2. Mission

The mission of ARK-OS is to build an operating system whose internals are understandable, whose components have clearly defined responsibilities, and whose development process remains reproducible and maintainable.

The project prioritizes:

- A Swift-first userspace where technically appropriate.
- Clear boundaries between operating-system components.
- Explicit boot, runtime, service, library, and shell responsibilities.
- A maintainable build and development workflow.
- Transparent licensing and third-party attribution.
- Accurate documentation and verifiable engineering claims.
- Minimal unnecessary complexity, dependencies, and code.
- A development process that preserves working implementations.

ARK-OS must not sacrifice correctness, maintainability, or architectural clarity merely to add features quickly.

## 3. Intended Platform

The initial development target is x86_64.

ARM64 is a future target, not a capability that should be claimed as supported until it has been implemented and verified.

Development may involve emulators, virtual machines, development boards, and physical hardware as appropriate. Actual hardware support must be recorded according to tested configurations.

The project is not assumed to be a complete, production-ready operating system. Its maturity must be described honestly.

## 4. Kernel and System Foundation

ARK-OS is intended to use Linux as its kernel foundation unless an explicit architectural decision establishes otherwise.

Linux kernel functionality, kernel configuration, boot integration, userspace interfaces, and upstream source management must remain clearly distinguished.

The project must document which responsibilities belong to the Linux kernel, which belong to ARK-OS components, and which are provided by third-party software.

No custom kernel implementation, kernel fork, bootloader, firmware integration, or hardware driver should be claimed to exist without evidence in the repository.

## 5. First-Party Components

The repository organizes first-party work into the following areas.

### `components/boot`

Boot-related integration and components needed to start the system. Exact responsibilities depend on the established boot architecture.

### `components/runtime/arkrt`

`arkrt` is the intended ARK-OS runtime and central system-process component. Its precise responsibilities and relationship to Linux process management, initialization, and system services must be documented explicitly.

It must not be described as replacing Linux kernel functionality unless that is technically accurate.

### `components/libraries/libark`

`libark` contains first-party library functionality shared by ARK-OS components. Its public interfaces, supported consumers, and responsibilities must be documented as they are established.

### `components/shell/sash`

`sash` is the intended ARK-OS shell. Its supported commands, scripting capabilities, compatibility goals, and current implementation status must be stated accurately.

### `components/services`

This area contains first-party system services. Each service must have a clear purpose, interface, lifecycle, and security boundary where applicable.

### `components/apps`

This area contains applications developed for ARK-OS. Applications must remain distinct from core runtime components and system services.

### `host-tools/aake`

`aake` is the intended build and compilation management tool for ARK-OS development. Its actual capabilities, supported workflows, and integration with existing toolchains must be documented from the implementation.

It must not be assumed to replace SwiftPM, Linux kernel build systems, or other upstream build systems without an explicit technical decision.

### `host-tools/signing`

This area contains host-side signing tools and related functionality. Signing responsibilities, key handling, trust assumptions, and security implications must be documented accurately.

These descriptions establish project intent, not proof that every component is implemented or functional.

## 6. Build and Development Philosophy

ARK-OS should have a predictable development workflow with explicit component ownership and documented dependencies.

The project should prefer:

- Reproducible inputs and pinned external sources.
- Explicit target configurations and build responsibilities.
- Small, reviewable changes.
- Automated checks that do not unexpectedly modify the repository.
- Tests appropriate to each component and development stage.
- Clear separation between host tools, target software, and upstream projects.

Build commands, tests, and validation procedures must be documented, but must not be executed by an AI agent unless explicitly authorized.

## 7. Third-Party Software and Licensing

ARK-OS may depend on upstream projects and existing open-source software.

Every included dependency must have a known source, version or revision, license, and documented integration method appropriate to its distribution.

The project must preserve applicable license notices and source-distribution obligations. Relevant records belong in the repository's licensing documentation, `CREDITS.md`, `THIRD_PARTY_NOTICES.md`, and other appropriate files.

No dependency, license, copyright holder, compliance status, or upstream permission may be invented or assumed.

Licensing claims must be verified against the actual source and applicable license terms.

## 8. Security Philosophy

Security documentation must describe real trust boundaries, interfaces, threat assumptions, known limitations, and reporting procedures.

Security features must not be claimed merely because a design intends to support them.

In particular, the project must not claim secure boot, verified boot, cryptographic integrity, sandboxing, memory safety, vulnerability-free code, or production readiness unless the relevant implementation and evidence support those claims.

Security decisions and unresolved risks should be recorded explicitly.

## 9. Documentation Philosophy

Documentation is part of the engineering work, not a substitute for it.

All documentation must distinguish between:

- **Implemented:** Present in the repository and supported by evidence.
- **Verified:** Tested under a documented configuration with recorded results.
- **Planned:** Intended future work that has not yet been completed.
- **Proposed:** An idea that has not yet been accepted as a project decision.
- **Unresolved:** A decision requiring further investigation or approval.

The same component names, architectural boundaries, supported platforms, and status descriptions must be used consistently throughout the repository.

Documentation must never imply that planned functionality already exists.

## 10. Current Repository Organization

The project currently uses these principal areas:

- `components/`: First-party operating-system components.
- `host-tools/`: Host-side development and build tools.
- `devtools/`: Development checks and release-related tooling.
- `docs/architecture/`: System architecture and component responsibilities.
- `docs/bringup/`: Boot and platform bring-up documentation.
- `docs/decisions/`: Architectural decision records.
- `docs/development/`: Developer workflows and technical guidance.
- `docs/licensing/`: Licensing and third-party compliance records.
- `external/`: Documentation and management of upstream dependencies.
- `manifests/`: Component, source, and target configuration manifests.
- `packaging/`: Packaging recipes and root filesystem material.
- `sdk/`: SDK-related material, if and to the extent implemented.
- `tests/`: Unit, integration, and boot-related tests.

The actual repository contents take precedence over assumptions based on directory names.

## 11. Long-Term Direction

ARK-OS aims to grow through deliberate, verifiable engineering rather than accumulating disconnected features.

Future improvements should follow documented architecture, explicit decisions, and demonstrated need.

Possible future capabilities are not commitments unless accepted through the project's decision process. No future platform, application ecosystem, compatibility layer, performance target, or release milestone should be presented as guaranteed.

## 12. Source of Truth

`AGENTS.md` defines the rules governing AI-assisted work.

`ABOUT.md` defines the project's intent and background while it is being used to establish the documentation baseline.

After the documentation baseline is completed and reviewed, the permanent documentation and accepted architectural decisions become the relevant sources of truth. This file is intended to be temporary and should be removed after that transition is complete.

When information is missing, contradictory, or unverified, document the uncertainty rather than inventing an answer.
