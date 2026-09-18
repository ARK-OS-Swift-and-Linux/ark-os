# Repository Verification Guide

This repository contains official signed releases and code for ARK-OS. To prevent supply chain attacks and verify that the repository has not been tampered with, you must verify the repository metadata using the provided signatures.

> [!CAUTION]
> **Do NOT implicitly trust scripts or keys inside the repository you are verifying!**
> A malicious actor who compromises a repository can easily alter any `.py` verification scripts or swap out the public keys (`keys/MAIN.pub`, `keys/BASE.pub`) to make a tampered repository look official.

## How to Verify the Repository

The official repository metadata is located in `REPO_INFO.json`. Its cryptographic signature is `REPO_INFO.json.sig`.

To securely verify the repository:

1. **Obtain the Official Public Key from a Trusted Source**
   Do NOT use the `keys/MAIN.pub` or `keys/BASE.pub` included in the clone you are verifying. Instead, download the official public key from a trusted, external source (e.g., the official ARK-OS website, developer's secure keybase, or hardware token).

2. **Verify the Signature using a Trusted Script**
   Do NOT execute `tools/generate_keys.py verify` from the untrusted repository! Use a version of the tool you have independently verified or use standard OpenSSL commands to verify the signature on `REPO_INFO.json` against the securely obtained public key.

   *Example OpenSSL verification command:*
   ```bash
   openssl dgst -sha256 -verify /path/to/trusted/BASE.pub -signature REPO_INFO.json.sig REPO_INFO.json
   ```

If the verification is successful (e.g., `Verified OK`), you can trust that `REPO_INFO.json` (and by extension, the repository it describes) is an official release.

---

## GPG Manifest & Tag Verification (Repo Tool)

Since ARK-OS has migrated to the Google `repo` tool for managing multiple repositories, our official releases are strictly locked down to exact revisions or tags within the `default.xml` manifest. 

To prevent "moving target" attacks and securely verify the entire project tree:

1. **Import the Official Public Key**
   Before cloning, import the official ARK-OS GPG public key (e.g., `arkos_public_key.asc`) into your local keyring:
   ```bash
   gpg --import arkos_public_key.asc
   ```

2. **Clone and Sync the Code**
   Initialize your repo client using the official manifest repository and sync the code:
   ```bash
   repo init -u https://github.com/ARK-OS-Swift-and-Linux
   repo sync
   ```

3. **Verify the Signed Release Tag**
   Navigate to the manifest repository (or the specific project directory) and verify the signed tag (e.g., `v1.0.0`):
   ```bash
   git tag -v v1.0.0
   ```

   **Expected Output:**
   Git will output a success message containing the text `gpg: Good signature from...`. 
   If any files on the server were modified without authorization, the cryptographic signature check will fail instantly.
