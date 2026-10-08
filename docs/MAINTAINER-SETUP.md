# Maintainer setup

One-time setup for the repo owner, done by hand **before the build agent starts**, plus a few later steps that the plan points back to. The agent never does these: they change account settings or involve keys.

Tick each box as you go. Total time: about 30 minutes.

**Status (2026-10-08):** done through the GitHub API with your approval: noreply email and history rewrite, commit signing on this Mac (verified), signing key on GitHub, public visibility, merge settings (4a), ruleset `protect-main` (4b, except the CI check), Actions limits incl. SHA pinning and fork-PR approval (4c), Dependabot, secret scanning, push protection and private vulnerability reporting (4d). Done by you: force push, signing scope, SSH passphrase, 2FA / passkey, email privacy, personal push protection. **Still open:** the required CI check and CodeQL (after B0.3.3), `git config core.hooksPath .githooks` (after B0.1.5), `brew install gitleaks`.

---

## 0. Repo visibility: public (done 2026-10-08)

`rtjw42/md3` is **public** (D21, MIT), so every GitHub protection below is free, and so are macOS CI minutes.

Before going public, the 3 existing commits were rewritten to your GitHub noreply address (`155293802+rtjw42@users.noreply.github.com`) and force-pushed once, so your Gmail address isn't in the public history. GitHub may keep the old commits for a while, reachable only by their exact commit ID; GitHub Support can purge them on request.

## 1. GitHub account security

1. Go to **github.com → your avatar → Settings → Password and authentication**.
2. Under **Two-factor authentication**, click **Enable**:
   - Choose **Authenticator app** (1Password, Apple Passwords, Authy, or Google Authenticator). Don't use SMS.
   - Scan the QR code and enter the 6-digit code.
   - **Download the recovery codes** and store them offline, e.g. printed or in your password manager. Without them, losing your phone locks you out.
3. Under **Passkeys**, click **Add a passkey** and use Touch ID. This becomes your fastest secure login.
4. Under **Sessions**, sign out of any device you don't recognise.

- [ ] 2FA on (authenticator app) · [ ] recovery codes saved offline · [ ] passkey added

---

## 2. SSH key passphrase

Your GitHub key is (probably) `~/.ssh/id_ed25519_personal`. A passphrase means a stolen copy of the file is useless on its own. macOS Keychain remembers the passphrase, so you won't have to type it every time.

1. Add a passphrase (the old one is blank if there isn't one; just press Return):
   ```bash
   ssh-keygen -p -f ~/.ssh/id_ed25519_personal
   ```
2. Make sure `~/.ssh/config` has this block (open it with `open -e ~/.ssh/config`; if `Host github.com` already exists, add the three missing lines to it):
   ```
   Host github.com
     IdentityFile ~/.ssh/id_ed25519_personal
     AddKeysToAgent yes
     UseKeychain yes
   ```
3. Store the passphrase in Keychain once:
   ```bash
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519_personal
   ```
4. Test:
   ```bash
   ssh -T git@github.com
   ```
   You should see "Hi rtjw42! You've successfully authenticated…".

- [ ] Passphrase set · [ ] Keychain stores it · [ ] `ssh -T` works

---

## 3. Signed commits (SSH signing)

Every commit gets a "Verified" badge on GitHub, so nobody can pass off commits as yours. Commits the agent makes on your Mac are signed with your key too, through the SSH agent. The agent never reads the key file.

1. Tell git to sign with your SSH key, for this repo only:
   ```bash
   cd ~/Documents/md3
   git config gpg.format ssh
   git config user.signingkey ~/.ssh/id_ed25519_personal.pub
   git config commit.gpgsign true
   git config tag.gpgsign true
   ```
   (To sign in every repo, use `git config --global …` instead.)
2. Let git verify signatures locally:
   ```bash
   mkdir -p ~/.config/git
   echo "rtjw42@gmail.com $(cat ~/.ssh/id_ed25519_personal.pub)" >> ~/.config/git/allowed_signers
   git config gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
   ```
3. Add the same key to GitHub **as a signing key** (a separate entry from the authentication key):
   **Settings → SSH and GPG keys → New SSH key → Key type: Signing Key**, then paste the output of:
   ```bash
   cat ~/.ssh/id_ed25519_personal.pub
   ```
4. Make sure your commit email is verified on GitHub: **Settings → Emails**. It must match `git config user.email`.
5. Test: make any small commit, then check it:
   ```bash
   git log --show-signature -1
   ```
   You should see `Good "git" signature for rtjw42@gmail.com`. On GitHub, the commit shows **Verified**.
6. Optional: **Settings → SSH and GPG keys → Vigilant mode**. Unsigned commits that claim to be you then show as "Unverified".

- [ ] Signing configured · [ ] signing key on GitHub · [ ] test commit shows Verified

---

## 4. Repository settings on GitHub

All of these are under **github.com/rtjw42/md3 → Settings**.

### 4a. General → Pull Requests
- [ ] ✅ Allow merge commits · ☐ untick **Allow squash merging** · ☐ untick **Allow rebase merging**. Squash and rebase would delete the task commits the timeline is built from.
- [ ] ✅ **Automatically delete head branches** (tidies up stage branches after merge)
- [ ] ✅ **Always suggest updating pull request branches**

### 4b. Rules → Rulesets → New ruleset → New branch ruleset
**Done 2026-10-08** (ruleset `protect-main`). Only the required CI check is left; see "Later steps". For reference, the settings:
- **Name:** `protect-main` · **Enforcement status:** Active
- **Bypass list:** leave empty. You can still temporarily disable the ruleset in an emergency.
- **Target branches:** Add target → **Include default branch**
- Rules:
  - [ ] ✅ Restrict deletions
  - [ ] ✅ Block force pushes
  - [ ] ✅ Require signed commits
  - [ ] ✅ Require a pull request before merging → Required approvals: **0** (you can't approve your own PR; the stage-end review agent is the reviewer). ✅ Require conversation resolution before merging.
  - [ ] ✅ Require status checks to pass → **add the CI check after B0.3.3 exists** (see the later steps below). ✅ Require branches to be up to date before merging.
- **Create**.

### 4c. Actions → General
- [ ] **Actions permissions:** Allow `rtjw42`, and select non-`rtjw42`, actions and reusable workflows → ✅ Allow actions created by GitHub. Add others only when the plan needs them.
- [ ] **Fork pull request workflows:** Require approval for **all external contributors**
- [ ] **Workflow permissions:** **Read repository contents and packages permissions** · ☐ untick "Allow GitHub Actions to create and approve pull requests"

### 4d. Advanced Security (called "Code security" on some accounts)
- [ ] ✅ Dependency graph
- [ ] ✅ Dependabot alerts · ✅ Dependabot security updates
- [ ] ✅ Grouped security updates
- [x] ✅ Secret scanning · ✅ Push protection · ✅ Private vulnerability reporting (done 2026-10-08)
- [ ] CodeQL → **Set up → Default**. It supports Swift and C/C++; do this once B0.3 has code to scan.

### 4e. Your personal setting
- [ ] **Your avatar → Settings → Code security → Push protection for yourself: Enable.** It blocks you pushing secrets to any public repo.

---

## 5. Local protections on this Mac

1. **Agent permission limits**: already created at `.claude/settings.json`. They block the agent from:
   - reading `~/.ssh`, `~/.gnupg`, keychains, gh credentials and signing-key files
   - force-pushing, pushing straight to `main` or deleting branches
   - skipping hooks (`--no-verify`), changing global git config or the hooks path
   - the `security` keychain tool, `sudo`, and GitHub secrets, repo-edit, delete and admin-merge commands

   Merging PRs, creating tags and creating releases always ask you first. Review the file once; the agent commits it in B0.1.2.

   *Limits:* these rules block the agent's tools, but they aren't a sandbox. The real protection for `main` is the ruleset in 4b, and the real protection for keys is that they never live in the repo or in the agent's reach.
2. **Git hooks path** (after the agent creates `.githooks/` in B0.1.5; the agent is blocked from doing this itself, so it can't switch hooks off either):
   ```bash
   git config core.hooksPath .githooks
   ```
3. **gitleaks** (local secret scanner; the pre-commit hook runs it from B0.5 onwards):
   ```bash
   brew install gitleaks
   ```

- [ ] Reviewed `.claude/settings.json` · [ ] hooks path set (after B0.1.5) · [ ] gitleaks installed

---

## Later steps (the plan points you back here)

| When | Step | How |
|---|---|---|
| After **B0.3.3** (CI exists) | Make CI a required check | Settings → Rules → `protect-main` → add **Require status checks to pass** with the CI job name (it appears after one CI run) and ✅ Require branches to be up to date. Also set up CodeQL (4d). |
| **B10.3** (before the first preview) | Create the Sparkle update-signing key | Run Sparkle's `generate_keys` tool on your Mac. The private key goes into your Keychain. **Export a backup** (`generate_keys -x sparkle_private_key`) to an encrypted USB drive or your password manager, then delete the exported file. Losing it means existing users can never be updated. |
| **B10.3** | Release environment for secrets | Settings → Environments → New environment `release` → ✅ Required reviewers: you → Deployment branches: tags matching `v*` only. Add the Sparkle key (and later the Apple keys) as **environment secrets** here, never as repo secrets. |
| **B10.4.4** (before 1.0) | Apple Developer account | Buy at developer.apple.com ($99/yr, #172). Create a **Developer ID Application** certificate and an **App Store Connect API key** for notarization. Store both only as `release` environment secrets, plus an offline backup. |
| Every 6 months | Security review | Check Settings → Sessions, SSH keys, deploy keys and authorized OAuth apps; remove anything unused. |
