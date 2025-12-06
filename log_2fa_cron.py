#!/usr/bin/env python3
import datetime
import os
from totp_utils import generate_totp

SEED_FILE = "/data/seed.txt"
OUTPUT_FILE = "/cron/last_code.txt"

if os.path.exists(SEED_FILE):
    with open(SEED_FILE) as f:
        seed = f.read().strip()
    code = generate_totp(seed)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"{timestamp} - 2FA Code: {code}\n")
