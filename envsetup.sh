#!/usr/bin/env bash
# ==============================================================================
# ARK-OS: Environment Setup and Toolchain Initialization
#
# Usage:
#   source envsetup.sh
#
# NOTE: This script must be SOURCED into an active shell session rather than
# executed directly. Executing a script runs it in an isolated child subshell;
# any exports, PATH modifications, or environment variables set in that subshell
# are discarded as soon as the child process exits. Sourcing executes commands
# directly within the parent shell, persisting the configured toolchain paths.
# ==============================================================================

# Ensure script is being sourced, not executed directly
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    echo "[!] Error: envsetup.sh must be sourced to persist environment changes." >&2
    echo "    Usage: source ${BASH_SOURCE[0]}" >&2
    exit 1
fi

# Locate repository root reliably regardless of current working directory
_ARKOS_ENVSETUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
export ARKOS_ROOT="${_ARKOS_ENVSETUP_DIR}"
export AAKE_DIR="${ARKOS_ROOT}/host-tools/aake"

echo "========================================"
echo "ARK-OS Environment Setup"
echo "========================================"
echo "Repository Root: ${ARKOS_ROOT}"

_AAKE_ENV_FAILURES=0
_AAKE_BOOT_WARNINGS=0

# 1. Host Operating System and Architecture
_HOST_OS="$(uname -s 2>/dev/null || echo "Unknown")"
_HOST_ARCH="$(uname -m 2>/dev/null || echo "Unknown")"

if [ "${_HOST_OS}" = "Linux" ] && [ "${_HOST_ARCH}" = "x86_64" ]; then
    echo "  [OK]   Host Platform            : ${_HOST_OS} ${_HOST_ARCH}"
else
    echo "  [FAIL] Host Platform            : ${_HOST_OS} ${_HOST_ARCH}"
    echo "         -> ARK-OS host tooling requires Linux x86_64."
    _AAKE_ENV_FAILURES=$((_AAKE_ENV_FAILURES + 1))
fi

# 2. Host C Compiler (gcc or clang)
_CC_PATH=""
if command -v gcc >/dev/null 2>&1; then
    _CC_PATH="$(command -v gcc)"
elif command -v clang >/dev/null 2>&1; then
    _CC_PATH="$(command -v clang)"
fi

if [ -n "${_CC_PATH}" ]; then
    echo "  [OK]   Host C Compiler          : ${_CC_PATH}"
else
    echo "  [FAIL] Host C Compiler          : Missing"
    echo "         -> Install gcc or clang (e.g., sudo pacman -S gcc or sudo apt install gcc)"
    _AAKE_ENV_FAILURES=$((_AAKE_ENV_FAILURES + 1))
fi

# 3. GNU Make (required for Aake bootstrap Makefile)
if command -v make >/dev/null 2>&1; then
    echo "  [OK]   GNU Make                 : $(command -v make)"
else
    echo "  [FAIL] GNU Make                 : Missing"
    echo "         -> Install make (e.g., sudo pacman -S make or sudo apt install make)"
    _AAKE_ENV_FAILURES=$((_AAKE_ENV_FAILURES + 1))
fi

# 4. Ninja Build System
if command -v ninja >/dev/null 2>&1; then
    echo "  [OK]   Ninja Build System       : $(command -v ninja)"
else
    echo "  [FAIL] Ninja Build System       : Missing"
    echo "         -> Install ninja (e.g., sudo pacman -S ninja or sudo apt install ninja-build)"
    _AAKE_ENV_FAILURES=$((_AAKE_ENV_FAILURES + 1))
fi

# 5. Swift Toolchain
if command -v swiftc >/dev/null 2>&1; then
    _SWIFT_VER="$(swiftc --version 2>/dev/null | head -n 1)"
    echo "  [OK]   Swift Toolchain          : $(command -v swiftc) (${_SWIFT_VER})"
else
    echo "  [FAIL] Swift Toolchain          : Missing"
    echo "         -> Install Swift 6.0+ toolchain and add swiftc to PATH"
    _AAKE_ENV_FAILURES=$((_AAKE_ENV_FAILURES + 1))
fi

# 6. Swift Static Linux SDK (musl)
_SWIFT_STATIC_SDK="${HOME}/.swiftpm/swift-sdks/swift-6.4.0-RELEASE_static-linux-0.1.0.artifactbundle/swift-6.4.0-RELEASE_static-linux-0.1.0/swift-linux-musl/musl-1.2.5.sdk/x86_64"
if [ -d "${_SWIFT_STATIC_SDK}" ]; then
    echo "  [OK]   Swift Static Linux SDK   : musl-1.2.5.sdk"
else
    echo "  [WARN] Swift Static Linux SDK   : Not found in ~/.swiftpm/swift-sdks"
    echo "         -> Target builds requiring static-musl will need the Swift SDK."
    echo "            Install via: swift sdk install <swift-static-sdk-url>"
fi

# 7. QEMU Emulator (Optional for building, required for `aake test --uefi`)
if command -v qemu-system-x86_64 >/dev/null 2>&1; then
    echo "  [OK]   QEMU Emulator            : $(command -v qemu-system-x86_64)"
else
    echo "  [WARN] QEMU Emulator            : Missing"
    echo "         -> Boot testing via 'aake test --uefi' requires qemu-system-x86_64."
    _AAKE_BOOT_WARNINGS=$((_AAKE_BOOT_WARNINGS + 1))
fi

# 8. UEFI Firmware (OVMF)
_OVMF_FOUND=""
for _p in "/usr/share/edk2/x64/OVMF.4m.fd" "/usr/share/OVMF/OVMF_CODE.fd" "/usr/share/ovmf/OVMF.fd"; do
    if [ -f "${_p}" ]; then
        _OVMF_FOUND="${_p}"
        break
    fi
done

if [ -n "${_OVMF_FOUND}" ]; then
    echo "  [OK]   UEFI Firmware (OVMF)     : ${_OVMF_FOUND}"
else
    echo "  [WARN] UEFI Firmware (OVMF)     : Missing in standard paths"
    echo "         -> Boot testing via 'aake test --uefi' requires edk2-ovmf."
    _AAKE_BOOT_WARNINGS=$((_AAKE_BOOT_WARNINGS + 1))
fi

echo "----------------------------------------"

# 9. Bootstrap Aake if missing or out of date
_AAKE_BIN="${AAKE_DIR}/bin/aake"
_NEED_BOOTSTRAP=0

if [ ! -x "${_AAKE_BIN}" ]; then
    _NEED_BOOTSTRAP=1
else
    # Check if any source or header is newer than the binary
    for _src in "${AAKE_DIR}"/src/*.c "${AAKE_DIR}"/include/*.h "${AAKE_DIR}"/Makefile; do
        if [ -f "${_src}" ] && [ "${_src}" -nt "${_AAKE_BIN}" ]; then
            _NEED_BOOTSTRAP=1
            break
        fi
    done
fi

if [ ${_NEED_BOOTSTRAP} -eq 1 ] && [ ${_AAKE_ENV_FAILURES} -eq 0 ]; then
    echo "[aake-bootstrap] Building Aake native orchestrator via bootstrap Makefile..."
    if make -C "${AAKE_DIR}" >/dev/null 2>&1; then
        echo "[aake-bootstrap] Aake built successfully at ${_AAKE_BIN}"
    else
        echo "[aake-bootstrap] Error: Failed to compile Aake. Run 'make -C ${AAKE_DIR}' to inspect diagnostics." >&2
        _AAKE_ENV_FAILURES=$((_AAKE_ENV_FAILURES + 1))
    fi
fi

# 10. Update PATH to include Aake binary directory (avoiding duplicates)
case ":${PATH}:" in
    *":${AAKE_DIR}/bin:"*)
        ;;
    *)
        export PATH="${AAKE_DIR}/bin:${PATH}"
        ;;
esac

# 11. Final Summary
echo "========================================"
if [ ${_AAKE_ENV_FAILURES} -eq 0 ]; then
    echo "ARK-OS Build Environment Configured"
    echo "ARKOS_ROOT : ${ARKOS_ROOT}"
    echo "AAKE_DIR   : ${AAKE_DIR}"
    echo "Aake CLI   : $(command -v aake 2>/dev/null || echo "${_AAKE_BIN}")"
    echo ""
    echo "Ready for building ARK-OS"
    echo "========================================"
    return 0 2>/dev/null || exit 0
else
    echo "ARK-OS Environment Configuration Incomplete"
    echo "Errors: ${_AAKE_ENV_FAILURES} required dependency check(s) failed."
    echo "Please install the missing tools and re-run: source envsetup.sh"
    echo "========================================"
    return 1 2>/dev/null || exit 1
fi
