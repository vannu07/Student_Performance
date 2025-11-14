# Security and Credentials

Do NOT commit secrets (API keys, tokens, passwords) into the repository. This project now expects secrets to be provided via environment variables or a secrets manager.

Recommended workflow
- Add secrets locally to a `.env` file (see `.env.example`). Make sure `.env` is listed in `.gitignore` (already included).
- Use a secrets manager for production (GitHub/GitLab/CI secrets, AWS Secrets Manager, HashiCorp Vault, etc.).

If you accidentally committed a secret
1. Revoke and rotate the leaked secret immediately (eg. delete the token on the provider side).
2. Remove the secret from git history. Recommended tools:
   - `git filter-repo` (preferred):
     ```bash
     pip install git-filter-repo
     git filter-repo --path-glob 'path/to/file/with/secret' --invert-paths
     ```
   - `bfg-repo-cleaner`:
     ```bash
     java -jar bfg.jar --delete-files YOUR_FILE
     git reflog expire --expire=now --all && git gc --prune=now --aggressive
     ```

Notes for contributors
- Never paste tokens or passwords in issues, PRs, or public chat.
- For CI, set secrets in repository settings (GitHub Secrets) and reference them in workflows.
- Limit token scopes and rotate frequently.
