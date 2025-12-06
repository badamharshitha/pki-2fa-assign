import json, requests

STUDENT_ID = "YOUR_STUDENT_ID"
GITHUB_REPO = "https://github.com/YOUR_USERNAME/pki-2fa"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO,
    "public_key": public_key
}

resp = requests.post(API_URL, json=payload)
data = resp.json()

with open("encrypted_seed.txt", "w") as f:
    f.write(data["encrypted_seed"])

print("Encrypted seed saved to encrypted_seed.txt")
