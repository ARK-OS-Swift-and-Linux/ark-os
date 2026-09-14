import sys
import json
import os
import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def main():
    if len(sys.argv) < 3:
        print("Usage: sign_binaries.py <output_vault.json> <host_path:target_path> ...")
        sys.exit(1)

    output_path = sys.argv[1]
    binaries = sys.argv[2:]

    # Generate or load key
    key_path = "keys/ed25519_priv.pem"
    os.makedirs("keys", exist_ok=True)

    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
    else:
        private_key = ed25519.Ed25519PrivateKey.generate()
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

    public_key = private_key.public_key()
    pub_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    master_pub_b64 = base64.b64encode(pub_raw).decode('utf-8')

    registry = {}

    for bin_arg in binaries:
        if ":" not in bin_arg:
            continue
        host_path, target_path = bin_arg.split(":", 1)
        
        if not os.path.exists(host_path):
            print(f"Warning: {host_path} does not exist, skipping.")
            continue

        with open(host_path, "rb") as f:
            data = f.read()
        
        # Compute SHA256 of the file
        digest = hashlib.sha256(data).digest()

        # Sign the digest
        signature = private_key.sign(digest)
        
        registry[target_path] = base64.b64encode(signature).decode('utf-8')

    vault = {
        "masterPublicKeyBase64": master_pub_b64,
        "signatureRegistry": registry
    }

    with open(output_path, "w") as f:
        json.dump(vault, f, indent=4)
        print(f"Wrote SignatureVault with {len(registry)} signatures to {output_path}")

if __name__ == "__main__":
    main()
