#!/usr/bin/env python3

"""
ARK-OS Cryptographic Trust / Verified Boot Generator

Trust hierarchy:

    MAIN
      |
      | signs
      v
    BASE
      |
      | signs
      v
    ARK-OS artifacts

MAIN is the global ARK-OS trust anchor.
BASE is the normal artifact-signing key.

IMPORTANT:
- MAIN.key must NEVER be shipped with ARK-OS.
- BASE.key should also remain private.
- Only public keys and signatures belong in the OS image.
- Ed25519 is used for actual cryptographic signatures.
- SHA3-512 is used for deterministic identifiers/fingerprints,
  NOT as a replacement for a signature algorithm.

Dependency:

    python3 -m pip install cryptography
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import stat
import struct
import sys
import tempfile
from pathlib import Path
from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
KEYS_DIR = REPO_ROOT / "keys"

MAIN_KEY = KEYS_DIR / "MAIN.key"
MAIN_PUB = KEYS_DIR / "MAIN.pub"

BASE_KEY = KEYS_DIR / "BASE.key"
BASE_PUB = KEYS_DIR / "BASE.pub"

BASE_CERT = KEYS_DIR / "BASE.cert"

# Kept as WIDE.key to preserve your existing naming scheme.
# It is intentionally a PUBLIC trust manifest, not a private secret.
WIDE_KEY = KEYS_DIR / "WIDE.key"

VB_IMAGE = REPO_ROOT / "vb.img"
VB_SIGNATURE = REPO_ROOT / "vb.img.sig"

MAGIC = b"ARK-VB-1\x00"
FORMAT_VERSION = 1

ALGORITHM = "Ed25519"
HASH_ALGORITHM = "SHA3-512"


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def secure_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

    # Best effort. On Unix this makes the directory owner-only.
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass


def atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
    """
    Atomically write a file.

    This prevents a partially-written private key from being left behind
    if the process is interrupted.
    """
    secure_mkdir(path.parent)

    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=str(path.parent),
    )

    try:
        os.fchmod(fd, mode)

        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(tmp_name, path)

    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


# ---------------------------------------------------------------------------
# Ed25519 key handling
# ---------------------------------------------------------------------------

def generate_private_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


def save_private_key(path: Path, key: Ed25519PrivateKey) -> None:
    """
    Store the raw 32-byte Ed25519 private seed.

    This file is sensitive.
    """
    raw = key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    if len(raw) != 32:
        raise RuntimeError("Unexpected Ed25519 private key size")

    atomic_write(path, raw, 0o600)


def load_private_key(path: Path) -> Ed25519PrivateKey:
    raw = read_bytes(path)

    if len(raw) != 32:
        raise ValueError(
            f"{path}: invalid Ed25519 private key; expected 32 bytes"
        )

    return Ed25519PrivateKey.from_private_bytes(raw)


def save_public_key(path: Path, key: Ed25519PublicKey) -> None:
    raw = key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    if len(raw) != 32:
        raise RuntimeError("Unexpected Ed25519 public key size")

    atomic_write(path, raw, 0o644)


def load_public_key(path: Path) -> Ed25519PublicKey:
    raw = read_bytes(path)

    if len(raw) != 32:
        raise ValueError(
            f"{path}: invalid Ed25519 public key; expected 32 bytes"
        )

    return Ed25519PublicKey.from_public_bytes(raw)


# ---------------------------------------------------------------------------
# Fingerprints
# ---------------------------------------------------------------------------

def fingerprint(public_key: Ed25519PublicKey) -> str:
    raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    return hashlib.sha3_512(raw).hexdigest()


# ---------------------------------------------------------------------------
# MAIN / BASE trust hierarchy
# ---------------------------------------------------------------------------

def generate_main() -> Ed25519PrivateKey:
    """
    Generate the permanent ARK-OS MAIN trust anchor.

    MAIN should normally be generated ONCE and then kept offline.
    """
    if MAIN_KEY.exists():
        raise RuntimeError(
            "MAIN.key already exists. Refusing to overwrite the ARK-OS root key."
        )

    main = generate_private_key()

    save_private_key(MAIN_KEY, main)
    save_public_key(MAIN_PUB, main.public_key())

    return main


def generate_base(main: Ed25519PrivateKey) -> Ed25519PrivateKey:
    """
    Generate BASE and create a MAIN-signed certificate binding BASE
    to the ARK-OS trust root.
    """

    if BASE_KEY.exists():
        raise RuntimeError(
            "BASE.key already exists. Refusing to overwrite it."
        )

    base = generate_private_key()

    save_private_key(BASE_KEY, base)
    save_public_key(BASE_PUB, base.public_key())

    base_public = base.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    certificate = {
        "format": "ARK-OS-KEY-CERT-1",
        "algorithm": ALGORITHM,
        "role": "BASE",
        "root": "MAIN",
        "public_key": base64.b64encode(base_public).decode("ascii"),
        "fingerprint": fingerprint(base.public_key()),
    }

    unsigned = json.dumps(
        certificate,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    signature = main.sign(unsigned)

    certificate["signature"] = base64.b64encode(signature).decode("ascii")

    final = json.dumps(
        certificate,
        indent=2,
        sort_keys=True,
    ).encode("utf-8")

    atomic_write(BASE_CERT, final, 0o644)

    return base


def create_wide_manifest(main: Ed25519PrivateKey) -> None:
    """
    WIDE is deliberately a trust manifest rather than a fake derived
    private key.

    It contains public trust information and is signed by MAIN.
    """

    main_public = main.public_key()

    if not BASE_PUB.exists():
        raise RuntimeError("BASE.pub does not exist")

    base_public = load_public_key(BASE_PUB)

    manifest = {
        "format": "ARK-OS-WIDE-TRUST-1",
        "algorithm": ALGORITHM,
        "root": {
            "role": "MAIN",
            "fingerprint": fingerprint(main_public),
        },
        "signing": {
            "role": "BASE",
            "fingerprint": fingerprint(base_public),
        },
        "policy": {
            "artifacts_must_be_signed": True,
            "base_must_be_authorized_by_main": True,
        },
    }

    unsigned = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    signature = main.sign(unsigned)

    manifest["main_signature"] = base64.b64encode(signature).decode("ascii")

    atomic_write(
        WIDE_KEY,
        json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8"),
        0o644,
    )


# ---------------------------------------------------------------------------
# Verified Boot image
# ---------------------------------------------------------------------------

def create_verified_boot_image(main: Ed25519PrivateKey) -> None:
    """
    Create a deterministic ARK-OS verified-boot container.

    Layout:

        MAGIC
        VERSION
        ALGORITHM
        PAYLOAD_LENGTH
        PAYLOAD
        SHA3-512(PAYLOAD)
        ED25519_SIGNATURE

    The signature covers the complete authenticated header + payload hash.
    """

    # This is a demo boot payload.
    # Replace this with your actual kernel/initramfs/boot payload later.
    payload = (
        b"ARK-OS VERIFIED BOOT PAYLOAD\n"
        b"This payload is authenticated by the ARK-OS MAIN root key.\n"
    )

    payload_hash = hashlib.sha3_512(payload).digest()

    algorithm_bytes = ALGORITHM.encode("ascii")

    header = (
        MAGIC
        + struct.pack("<I", FORMAT_VERSION)
        + struct.pack("<I", len(algorithm_bytes))
        + algorithm_bytes
        + struct.pack("<Q", len(payload))
    )

    authenticated_data = header + payload_hash

    signature = main.sign(authenticated_data)

    image = (
        header
        + payload
        + payload_hash
        + struct.pack("<I", len(signature))
        + signature
    )

    atomic_write(VB_IMAGE, image, 0o644)

    # Separate detached signature for tooling.
    atomic_write(VB_SIGNATURE, signature, 0o644)


# ---------------------------------------------------------------------------
# Artifact signing
# ---------------------------------------------------------------------------

def sign_file(path: Path) -> Path:
    """
    Sign an arbitrary ARK-OS artifact using BASE.
    """

    base = load_private_key(BASE_KEY)

    data = path.read_bytes()
    digest = hashlib.sha3_512(data).digest()

    signature = base.sign(digest)

    signature_path = Path(str(path) + ".sig")

    atomic_write(signature_path, signature, 0o644)

    return signature_path


def verify_file(path: Path, signature_path: Path) -> bool:
    """
    Verify an artifact against the ARK-OS BASE public key.
    """

    base_public = load_public_key(BASE_PUB)

    data = path.read_bytes()
    digest = hashlib.sha3_512(data).digest()

    signature = signature_path.read_bytes()

    try:
        base_public.verify(signature, digest)
        return True
    except InvalidSignature:
        return False


# ---------------------------------------------------------------------------
# Verify BASE certificate using MAIN
# ---------------------------------------------------------------------------

def verify_base_certificate() -> bool:
    main_public = load_public_key(MAIN_PUB)

    certificate = json.loads(BASE_CERT.read_text())

    signature_b64 = certificate.pop("signature")
    signature = base64.b64decode(signature_b64)

    unsigned = json.dumps(
        certificate,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    try:
        main_public.verify(signature, unsigned)
    except InvalidSignature:
        return False

    base_public_raw = base64.b64decode(certificate["public_key"])
    base_public = Ed25519PublicKey.from_public_bytes(base_public_raw)

    expected_fp = fingerprint(base_public)

    return expected_fp == certificate["fingerprint"]


# ---------------------------------------------------------------------------
# Verify verified boot image
# ---------------------------------------------------------------------------

def verify_verified_boot_image() -> bool:
    main_public = load_public_key(MAIN_PUB)

    data = VB_IMAGE.read_bytes()

    offset = 0

    if data[offset:offset + len(MAGIC)] != MAGIC:
        return False

    offset += len(MAGIC)

    version = struct.unpack_from("<I", data, offset)[0]
    offset += 4

    if version != FORMAT_VERSION:
        return False

    algorithm_length = struct.unpack_from("<I", data, offset)[0]
    offset += 4

    algorithm = data[offset:offset + algorithm_length].decode("ascii")
    offset += algorithm_length

    if algorithm != ALGORITHM:
        return False

    payload_length = struct.unpack_from("<Q", data, offset)[0]
    offset += 8

    payload = data[offset:offset + payload_length]
    offset += payload_length

    stored_hash = data[offset:offset + 64]
    offset += 64

    calculated_hash = hashlib.sha3_512(payload).digest()

    if not secrets.compare_digest(stored_hash, calculated_hash):
        return False

    signature_length = struct.unpack_from("<I", data, offset)[0]
    offset += 4

    signature = data[offset:offset + signature_length]

    header = (
        MAGIC
        + struct.pack("<I", version)
        + struct.pack("<I", algorithm_length)
        + algorithm.encode("ascii")
        + struct.pack("<Q", payload_length)
    )

    authenticated_data = header + calculated_hash

    try:
        main_public.verify(signature, authenticated_data)
        return True
    except InvalidSignature:
        return False


# ---------------------------------------------------------------------------
# Full generation
# ---------------------------------------------------------------------------

def generate_all() -> None:
    secure_mkdir(KEYS_DIR)

    print()
    print("=" * 72)
    print("          ARK-OS CRYPTOGRAPHIC TRUST INITIALIZATION")
    print("=" * 72)
    print()

    print("[1/5] Generating MAIN root key...")

    main = generate_main()

    print("[+] MAIN.key generated")
    print("[+] MAIN.pub generated")
    print(f"[+] MAIN fingerprint:")
    print(f"    {fingerprint(main.public_key())}")
    print()

    print("[2/5] Generating BASE signing key...")

    base = generate_base(main)

    print("[+] BASE.key generated")
    print("[+] BASE.pub generated")
    print("[+] BASE.cert generated")
    print()

    print("[3/5] Generating WIDE trust manifest...")

    create_wide_manifest(main)

    print("[+] WIDE.key generated")
    print()

    print("[4/5] Generating verified boot image...")

    create_verified_boot_image(main)

    print("[+] vb.img generated")
    print("[+] vb.img.sig generated")
    print()

    print("[5/5] Verifying trust chain...")

    if not verify_base_certificate():
        raise RuntimeError("BASE certificate verification FAILED")

    if not verify_verified_boot_image():
        raise RuntimeError("Verified boot image verification FAILED")

    print("[+] MAIN → BASE trust chain valid")
    print("[+] vb.img signature valid")
    print()

    print("=" * 72)
    print("                 ARK-OS TRUST INITIALIZED")
    print("=" * 72)
    print()
    print("MAIN = permanent ARK-OS root of trust")
    print("BASE = artifact signing key")
    print("WIDE = signed public trust manifest")
    print()
    print("IMPORTANT:")
    print("  MAIN.key MUST NOT be shipped inside ARK-OS.")
    print("  Keep MAIN.key offline / hardware protected.")
    print("  BASE.key must also remain private.")
    print()
    print(f"Keys: {KEYS_DIR}")
    print(f"Boot image: {VB_IMAGE}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="ARK-OS cryptographic trust and verified boot tool"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser(
        "generate",
        help="Generate MAIN, BASE, WIDE and verified boot image",
    )

    sign_parser = sub.add_parser(
        "sign",
        help="Sign an ARK-OS artifact using BASE",
    )
    sign_parser.add_argument("file", type=Path)

    verify_parser = sub.add_parser(
        "verify",
        help="Verify an ARK-OS artifact using BASE",
    )
    verify_parser.add_argument("file", type=Path)
    verify_parser.add_argument(
        "--signature",
        type=Path,
        default=None,
    )

    sub.add_parser(
        "verify-boot",
        help="Verify vb.img using MAIN",
    )

    sub.add_parser(
        "verify-base",
        help="Verify BASE certificate using MAIN",
    )

    args = parser.parse_args()

    try:
        if args.command == "generate":
            generate_all()

        elif args.command == "sign":
            signature = sign_file(args.file)
            print(f"[+] Signed: {args.file}")
            print(f"[+] Signature: {signature}")

        elif args.command == "verify":
            signature = args.signature or Path(str(args.file) + ".sig")

            if verify_file(args.file, signature):
                print("[+] SIGNATURE VALID")
                return 0

            print("[!] SIGNATURE INVALID", file=sys.stderr)
            return 1

        elif args.command == "verify-boot":
            if verify_verified_boot_image():
                print("[+] VERIFIED BOOT SIGNATURE VALID")
                return 0

            print("[!] VERIFIED BOOT SIGNATURE INVALID", file=sys.stderr)
            return 1

        elif args.command == "verify-base":
            if verify_base_certificate():
                print("[+] MAIN → BASE CERTIFICATE VALID")
                return 0

            print("[!] BASE CERTIFICATE INVALID", file=sys.stderr)
            return 1

        else:
            parser.print_help()

    except Exception as exc:
        print(f"[FATAL] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
