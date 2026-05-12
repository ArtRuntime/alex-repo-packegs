# Custom Arch Linux Repository (Monorepo)

This repository serves as the master source for a custom, automated Arch Linux package repository. It utilizes a **Monorepo architecture** and GitHub Actions to continuously build, sign, and publish packages.

## Structure

Each package lives in its own subdirectory. To add a new package, simply create a new directory containing:
- `PKGBUILD.template` (A standard PKGBUILD, using `{VERSION}`, `{SHA256}`, and `{URL}` as placeholders).
- `main.py` (A web scraper that prints a JSON object with the latest `version`, `sha256`, and `url`).
- `requirements.txt` *(Optional)* (Python dependencies for `main.py`).

## How it Works

1. **Check Updates:** A GitHub Action runs periodically to execute `main.py` in every folder and compares the version against the existing state (`versions.json`).
2. **Matrix Build:** For any package needing an update, the pipeline spawns a parallel, isolated Arch Linux sandbox container to build the package.
3. **Publish:** Once all packages build successfully, they are merged into the master `alex-repo.db`, signed with GPG, and published to the `latest` rolling release tag.
4. **Sync:** Finally, a webhook triggers your Vercel Next.js dashboard to update its database and reflect the new packages.

## Secrets Required (GitHub Actions)
- `GPG_PRIVATE_KEY`: Your ASCII-armored private GPG key for signing packages.
- `GPG_PASSPHRASE`: The passphrase for your GPG key.
- `SYNC_URL`: The webhook URL for your dashboard (e.g., `https://your-domain.vercel.app/api/webhook/sync`).
- `SYNC_API_KEY`: The API key generated from your dashboard settings.
