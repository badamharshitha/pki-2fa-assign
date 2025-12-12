# scripts/sign_commit.py
import base64, subprocess, sys
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# ensure keys exist
for fn in ("student_private.pem","instructor_public.pem"):
    try:
        open(fn,"rb").read()
    except FileNotFoundError:
        print(f"ERROR: missing {fn}", file=sys.stderr); sys.exit(2)

# load student private key
with open("student_private.pem","rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# get latest commit hash
commit_hash = subprocess.check_output(["git","log","-1","--format=%H"]).decode().strip()

# sign commit hash (ASCII) using RSA-PSS (SHA256, max salt)
signature = private_key.sign(
    commit_hash.encode("utf-8"),
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# load instructor public key and encrypt signature with RSA-OAEP (SHA256)
with open("instructor_public.pem","rb") as f:
    instr_pub = load_pem_public_key(f.read())

encrypted_sig = instr_pub.encrypt(
    signature,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# print single-line base64
print(base64.b64encode(encrypted_sig).decode())
