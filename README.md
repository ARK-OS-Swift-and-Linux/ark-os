# ArkOS

A Linux-based operating system built from scratch — designed to be easy to use, easy to compile, and open for customization.


You can sync the repo via:
```bash
curl -fsSL https://raw.githubusercontent.com/ARK-OS-Swift-and-Linux/main/refs/heads/main/sync.sh | bash
```

> [!DISCLAMER]
>
> Building now requires a Stable Internet Connection!
> Only on the first build since after that downloads are cached
> If you rerun a Fresh build you will need a Internet Connection!
> This is to reduce the size of the project on servers!

```
[ 2/5 ] Add Display Support
    
    [ Finished ]   Fix Build, Git, and Management
    [ 1 day ]      Add Display Support
    [ Pending ]    Complete arkrt 
    [ 1h 2m ]      Add arm64 compile support to aake
    [ Pending ]    Update Documentation
```
## Building

### Prerequisites

| Tool | Purpose |
|------|---------|
| `clang` (prebuilt, included) | C/C++ compilation (all architectures) |
| `swiftc` | Swift compilation |
| `nasm` | x86 assembly |
| `python3` | Boot image packing & signing |
| `qemu-system-x86_64` / `qemu-system-aarch64` | Testing & Emulation |
| `mkfs.ext4`, `mkfs.vfat`, `mtools`, `parted` | Disk image generation |
| `cpio`, `gzip` | Initramfs packing |
| `ninja` | Build system |

### How to use compiler

```bash

Usage: aake [options] [commands]

Commands:

build       Build ArkOS for the host architecture (default if options passed)
test        Run ArkOS in QEMU (automatically builds if needed)
clean       Clean the build directory
sign        Sign binaries
font-gen    Generate TTF fonts to Swift/C arrays
cursor-gen  Generate mouse cursor arrays

Options:

--x86_64    Build/test for x86_64 architecture
--arm64     Build/test for ARM64 architecture
--uefi      Test in UEFI mode (for x86_64)
--bios      Test in BIOS mode (for x86_64)
-v          Verbose output
-j          Number of parallel jobs
--no-ninja  Generate build files but don't compile
```

#### Cross-Architecture Testing

```bash
aake test --x86_64 --uefi
aake test --x86_64 --bios
aake test --arm64 --uefi
aake test --arm64 --bios
```

Test targets auto-detect the host CPU and use hardware acceleration (KVM) when possible, falling back to software emulation (TCG) for cross-architecture testing.

### Raspberry Pi 4 Flashing

To write the compiled ARM64 image to an SD card for real hardware:

```bash
sudo dd if=finished/rpi4/rpi4.img of=/dev/sdX bs=4M status=progress
sync
```

All compilation uses the prebuilt Clang/LLVM toolchain with target triples:
- x86_64: `clang --target=x86_64-linux-gnu`
- ARM64: `clang --target=aarch64-linux-gnu`

### Output Images

All images are generated in `finished/` (or `finished/rpi4/` for ARM64):

| Image | Description |
|-------|-------------|
| `boot.img` | Bootloader + animation + kernel + initramfs |
| `sys.img` | System partition (frameworks, libraries) |
| `vend.img` | Vendor partition (DRM, keys, mirror info) |
| `vbk.img` | Verified Boot Key — bootloader verifies sys.img/vend.img signatures |
| `vbmeta.img` | Boot metadata — mount configuration (vbmeta.ark) |
| `dtbo.img` | *(ARM64 only)* Device tree blobs and overlays for the kernel |
| `rpi4.img` | *(ARM64 only)* Flashable SD card image combining all partitions |

## 📁 Project Structure

```
arkos/
├── boot/                    # Bootloader source & configs
│   ├── source/              # Assembly source (bootloader.asm, stage2.asm) and C source (bootloader.c)
│   │   └── animationframes/ # Pre-generated boot animation frames
│   ├── rpi4/                # RPi4 boot firmware and config
│   ├── initramfs.img        # Base initramfs image
│   └── *.ark                # Boot configuration files
├── build/envset.sh          # Android-style build environment setup
├── frameworks/              # OS frameworks (DRM, SwiftUI)
├── hardware/                # Hardware-specific configurations
│   └── rpi4/                # Raspberry Pi 4 config (.ark)
├── kernel/                  # Linux kernel source + prebuilt bzImage
├── prebuilts/               # Prebuilt toolchains and SDKs
│   ├── clang/               # LLVM/Clang 22 toolchain
│   ├── Swift/               # Precompiled Swift 6.3.2 runtime & stdlib
│   └── mimalloc.o           # Microsoft mimalloc memory allocator
├── system/                  # Core system components
│   ├── apps/                # System apps (setup_app)
│   ├── display/             # Display compositor (ui_daemon) and boot animation
│   ├── services/            # Service configuration definitions (.serve)
│   ├── sysroot/             # x86_64 system root
│   └── sysrootaarch64/      # ARM64 system root
├── vendor/                  # Vendor-specific files
│   ├── verify/              # Verified Boot keys & signing tools
│   ├── mirror/              # Mirror configuration
│   └── Widewine/            # DRM (Widevine) integration
├── arkrt/                   # ArkOS runtime monolithic daemon (PID1) and libraries
├── Makefile                 # Top-level build entry point
└── finished/                # Build output (generated)
```

## 📄 License

See [LICENSE](LICENSE) for details.
