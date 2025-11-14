"""
Helper to load `.env` into the environment for local development.
Usage:
  python scripts/load_env.py        # loads .env from repo root and prints loaded keys
  python scripts/load_env.py --run "python app.py"  # load env and run a command

Note: For production, use a real secrets manager or CI secrets.
"""
import os
import argparse
from dotenv import load_dotenv


def mask(v: str) -> str:
    if not v:
        return ""
    if len(v) <= 8:
        return "*" * len(v)
    return v[:4] + "..." + v[-4:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env", help="Path to .env file")
    parser.add_argument("--run", help="Optional command to run after loading env")
    args = parser.parse_args()

    env_path = os.path.join(os.getcwd(), args.env_file)
    if not os.path.exists(env_path):
        print(f"No {args.env_file} found at {env_path}. Nothing loaded.")
        return

    load_dotenv(dotenv_path=env_path)
    print(f"Loaded environment variables from {env_path}")

    # Show a few common vars (masked)
    for key in ["SECRET_KEY", "MLFLOW_TRACKING_URI", "MLFLOW_TRACKING_USERNAME", "MLFLOW_TRACKING_PASSWORD"]:
        val = os.getenv(key)
        if val is not None:
            print(f"{key} = {mask(val)}")

    if args.run:
        print(f"Running: {args.run}")
        os.system(args.run)


if __name__ == "__main__":
    main()
