# Contributing to ARK-OS

Thank you for your interest in contributing to ARK-OS.

ARK-OS is an independent operating-system development project focused on modular, understandable, and verifiable engineering. All contributions must adhere to the rules, safety invariants, and quality standards documented in [AGENTS.md](file:///home/aarav/repo/arkos/AGENTS.md).

---

## 1. Core Engineering Principles

Every contribution must respect the following standards:

1. **Understand Before Acting:** Inspect existing code, manifests, and documentation before making changes. Never guess when an incorrect assumption could affect system behavior, security, or architecture.
2. **No Bloat:** Every addition must have a clear purpose connected to an approved requirement. Do not add unrequested frameworks, speculative abstraction layers, unused configuration, or redundant helper classes.
3. **No Emojis:** The use of emojis is prohibited in source code, comments, documentation, commit messages, and tooling output.
4. **Professional Tone:** Avoid marketing hype, promotional phrasing, and unverified claims. Use precise, technically accurate descriptions.
5. **Preserve Working Implementations:** Do not perform broad refactorings during localized bug fixes. Always preserve existing functionality unless an explicit breaking change has been approved.

---

## 2. Contribution Workflow

### 2.1 Proposing Architectural Changes

Material architectural changes (such as adding a new component, modifying boot protocols, changing inter-process communication mechanisms, or adopting a major dependency) must be proposed through an Architecture Decision Record (ADR).

1. Review existing decisions and unresolved topics in [docs/decisions/](file:///home/aarav/repo/arkos/docs/decisions/).
2. Draft an ADR document specifying context, considered alternatives, decision rationale, and architectural trade-offs.
3. Submit the proposal for maintainer review before introducing implementation code.

### 2.2 Making Changes

1. **Keep Changes Focused:** Address one logical objective per change. Do not mix refactoring, formatting changes, and functional modifications in a single submission.
2. **Follow Directory Ownership:** Place files strictly in their owning directory as defined in [AGENTS.md](file:///home/aarav/repo/arkos/AGENTS.md) Section 3. Do not introduce unapproved root-level files or arbitrary directories.
3. **Write Meaningful Comments:** Explain invariants, ownership constraints, non-obvious algorithms, and hardware assumptions. Do not write comments that merely restate what the code does.

---

## 3. Code Standards by Language

### 3.1 Swift Code
- Follow the established Swift toolchain version (Swift 5.10+).
- Prefer value types unless identity or shared mutable state is required.
- Handle errors explicitly using typed throws or standard error constructs; never swallow errors in empty `catch` blocks.
- Respect actor isolation, Sendable contracts, and concurrency safety.
- Verify Linux runtime compatibility. Do not assume Darwin-specific frameworks (such as Apple-specific Foundation features or SwiftUI) are available.

### 3.2 C and C++ Code
- Adhere to the established style of the target component.
- Strictly document pointer lifetimes, buffer boundaries, error codes, and thread-safety assumptions.
- In freestanding or low-level environments, do not assume standard library facilities, dynamic allocations, or exception handling are available.
- Validate all buffer lengths and arithmetic conversions.

### 3.3 Manifests and Configuration
- Manifest files in `manifests/` must conform to established schemas.
- Do not invent fields without updating the corresponding parser and documentation.
- External sources must be recorded with exact pinned revisions in `manifests/sources.lock.toml`.

---

## 4. Documentation Standards

- Update documentation alongside any change to interfaces, workflows, or component responsibilities.
- Clearly distinguish between:
  - **Implemented:** Code is present and verified.
  - **Planned:** Architecture is specified but code does not exist.
  - **Unresolved:** Design questions requiring decision.
- Never present future goals as current capabilities.
- Keep documentation concise, accurate, and free of redundant boilerplate.

---

## 5. Validation and Testing Requirements

- Inspect modified files and the final diff before submission.
- Ensure all relative links and file references exist.
- Verify that no secrets, keys, temporary editor files, or build artifacts are introduced.
- **Build Restrictions:** Do not execute build or test commands without explicit authorization from repository maintainers, as outlined in [AGENTS.md](file:///home/aarav/repo/arkos/AGENTS.md) Section 6. Clearly document which checks were run and which remain unverified.
