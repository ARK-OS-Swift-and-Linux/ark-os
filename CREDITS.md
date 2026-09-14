# ArkOS Credits and Licensing

ArkOS incorporates open-source projects and libraries to build its rich ecosystem. We are grateful to the authors and contributors of these projects.

 - **The Linux Kernel (7.0 & 6.1)** - Used for x86_64 and Raspberry Pi 4 (AArch64) respectively.
 - **The GNU C Library (Glibc 2.43)** - Compiled for both x86_64 and AArch64.
 - **Swift 6.3.2 (Apple)** - Powering the core UI and IPC layers, acting as the primary language for `arkrt`.
 - **mimalloc (Microsoft)** - For providing the ultra-fast memory allocator.
 - **LLVM / Clang 22** - For the prebuilt cross-compilation toolchain.
 - **QEMU** - The vital emulation platform used for testing x86_64 and AArch64 builds.
 - **Raspberry Pi Firmware** - Including `start4.elf` and `bootcode.bin` provided by Broadcom and the Raspberry Pi Foundation.
 - **Widevine DRM (Google)** - For providing the Content Decryption Module in the vendor partition.
 - **Wayland (freedesktop.org)** - The core display server protocol powering ArkUI.
 - **Wayland Protocols (freedesktop.org)** - Extensions to the Wayland protocol.
 - **libdrm (freedesktop.org)** - For Direct Rendering Manager interactions in the display compositor.
 - **libinput (freedesktop.org)** - Handling mouse, keyboard, and touch inputs seamlessly.
 - **libxkbcommon (xkbcommon.org)** - For keyboard layout translation and keymap compilation.
 - **Ninja Build System** - For extremely fast parallel compilation orchestrated by `aake`.
 - **NASM (Netwide Assembler)** - Used for compiling the x86_64 assembly bootloader stages.
 - **Python 3** - Used for boot image packing, signing, and Verified Boot scripting.
 - **GCC & Make** - Foundational open-source utilities used for building `aake`.
 - **swift-argument-parser (Apple)** - For building powerful command-line tools in Swift.
 - **swift-metrics (Apple)** - For comprehensive metrics and performance tracking.
 - **swift-system (Apple)** - For low-level system calls and file path operations.
 - **swift-log (Apple)** - For a standard logging API.
 - **SwiftTerm (Miguel de Icaza)** - For Terminal emulation.
 - **swift-nio-ssh (Apple)** - For SSH protocol implementation.
 - **swift-nio-extras (Apple)** - For extra NIO features.
 - **swift-nio-http2 (Apple)** - For HTTP/2 support.
 - **swift-nio-ssl (Apple)** - For SSL/TLS support.
 - **grpc-swift (gRPC)** - For building robust gRPC services.
 - **swift-nio (Apple)** - For high-performance networking.

A massive round of APPLAUSE and heartfelt thanks to the creators and maintainers of these incredible projects! Without your foundational tools, languages, and open-source contributions, this operating system would simply not be possible. Thank you!

Official Rights over this project "ARK-OS" belongs to Aarav Ravindra Kharade.

Contributors: <NONE>

Note: If you think your work has been used without your permission, please let me know at arkosgogs@gmail.com