# Install the animated GitHub profile

1. Download and extract this ZIP.
2. Your public profile repository must be named exactly `Tejass555`: https://github.com/Tejass555/Tejass555
3. Copy the *contents* of the extracted folder into the repository root. Keep `.github/workflows/refresh-profile.yml` at that exact path. Back up your current README before replacing it.
4. Edit `profile.json` to update the three metric cards. Starter metrics are editable text, not verified statistics.
5. Optional local test: install Python 3.10+ and run `python scripts/render_readme_cards.py` from the repository root. No pip packages are needed.
6. Create a GitHub Personal Access Token that can read your account's contribution calendar. If a fine-grained token cannot access the GraphQL query, use a classic token with `read:user` scope.
7. In repository Settings → Secrets and variables → Actions → New repository secret, create `GH_TOKEN` and paste the token. Never commit the token.
8. In Settings → Actions → General → Workflow permissions, enable **Read and write permissions** and save.
9. Open Actions → **Refresh animated profile cards** → **Run workflow**. Check that it succeeds and updates `cards/` and `data/contributions.json`.
10. Open https://github.com/Tejass555 to verify the profile. Scheduled refresh is daily at 02:15 UTC (07:45 India time); GitHub may delay scheduled runs.

For a local data refresh, set `GH_TOKEN` and `GITHUB_USERNAME=Tejass555`, then run:
- Windows PowerShell: `$env:GH_TOKEN="YOUR_TOKEN"; $env:GITHUB_USERNAME="Tejass555"; python scripts/collect_contributions.py`
- macOS/Linux: `export GH_TOKEN="YOUR_TOKEN"; export GITHUB_USERNAME="Tejass555"; python scripts/collect_contributions.py`

SVG animation support differs between clients; this build focuses on the reference's paper/ink/blue-red-yellow look and readable static cards. Contribution charts use GitHub's returned contribution calendar. Metric-card copy is manually configured in `profile.json`.
