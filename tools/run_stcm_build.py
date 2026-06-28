#!/usr/bin/env python3
import subprocess


def main():
    result = subprocess.run(["python", "tools/verify_ae_intake.py"], check=False)
    if result.returncode == 0:
        print("PASS STCM build")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
