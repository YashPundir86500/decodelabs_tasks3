# 🔐 Enterprise Random Password Generator

> **Cryptographically secure** password generation powered by Python's `secrets` module — no weak randomness, no compromises.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Password Strength Scoring](#password-strength-scoring)
- [Output & File Saving](#output--file-saving)
- [Project Structure](#project-structure)
- [Security Notes](#security-notes)
- [License](#license)

---

## Overview

**Enterprise Random Password Generator** is a CLI tool that generates high-entropy, cryptographically secure passwords using Python's built-in `secrets` module — the same module recommended for security-sensitive applications by the Python Software Foundation.

Whether you need a single strong password or a batch of 50, this tool gives you full control over length, character composition, and output format.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔒 **Cryptographically Secure** | Uses `secrets.choice()` and `secrets.SystemRandom()` — not `random` |
| 🔡 **Flexible Character Sets** | Uppercase, lowercase, digits, and optional special characters |
| 📏 **Custom Length** | Any length from 4 to 512 characters |
| 🔁 **Batch Generation** | Generate 1 to 50 passwords in a single run |
| 💪 **Strength Evaluator** | Rates each password: 🔴 Weak / 🟡 Medium / 🟢 Strong |
| 💾 **File Export** | Optionally save all passwords to `saved_passwords.txt` with timestamps |
| 🛡️ **Guaranteed Complexity** | Every password always contains at least one uppercase, one lowercase, and one digit |

---

## ⚙️ Requirements

- **Python 3.10+** (uses built-in `tuple[str, str]` type hints)
- No third-party packages required — 100% standard library

---

## 🚀 Installation

```bash
# Clone or download the repository
git clone https://github.com/your-username/enterprise-password-generator.git
cd enterprise-password-generator
```

That's it. No `pip install` needed.

---

## 🖥️ Usage

```bash
python Password_Generator.py
```

You'll be guided through an interactive menu:

```
============================================================
   🔐  Enterprise Random Password Generator  🔐
============================================================

  Main Menu
  ─────────
  [1]  Generate password(s)
  [2]  Exit
```

### Step-by-step flow

1. **Choose option `[1]`** to begin generation
2. **Enter desired length** — between 4 and 512 characters
3. **Include special characters?** — `y` for symbols like `@#$%!`, `n` for alphanumeric only
4. **How many passwords?** — 1 to 50 at a time
5. **Save to file?** — Optionally export results to `saved_passwords.txt`

### Example Output

```
------------------------------------------------------------
  #     Password                                      Strength
------------------------------------------------------------
  1     kR9!mXqL@2vTzN#pW8cJ                         🟢 Strong
  2     Yt7$bVnQ3sMuEwK!                              🟢 Strong
  3     Lp4@jHrX2oGcNd9                               🟡 Medium
------------------------------------------------------------
```

---

## 💪 Password Strength Scoring

Each password is evaluated on a 7-point scoring rubric:

| Criterion | Points |
|---|---|
| Length ≥ 8 | +1 |
| Length ≥ 12 | +1 |
| Length ≥ 16 | +1 |
| Contains uppercase letter | +1 |
| Contains lowercase letter | +1 |
| Contains digit | +1 |
| Contains special character | +1 |

**Score → Rating:**

| Score | Rating |
|---|---|
| 0 – 3 | 🔴 Weak |
| 4 – 5 | 🟡 Medium |
| 6 – 7 | 🟢 Strong |

---

## 💾 Output & File Saving

When you choose to save, passwords are **appended** to `saved_passwords.txt` in your working directory. Each batch is clearly separated with metadata:

```
──────────────────────────────────────────────────
Generated : 2025-01-15 14:32:07
Length    : 20
Count     : 3
──────────────────────────────────────────────────
  [  1]  kR9!mXqL@2vTzN#pW8cJ  (Strong)
  [  2]  Yt7$bVnQ3sMuEwK!9pRj  (Strong)
  [  3]  Lp4@jHrX2oGcNd9mQbTs  (Strong)
```

> ⚠️ **Important:** Store `saved_passwords.txt` securely. Never commit it to version control. Consider adding it to `.gitignore`.

---

## 📁 Project Structure

```
enterprise-password-generator/
│
├── Password_Generator.py    # Main application file
├── README.md                # This file
└── saved_passwords.txt      # Auto-created when you save passwords (gitignore this!)
```

---

## 🔐 Security Notes

- **`secrets` vs `random`** — This tool uses Python's `secrets` module which draws from the OS-level CSPRNG (`/dev/urandom` on Linux/macOS, `CryptGenRandom` on Windows). The standard `random` module is **not** suitable for security purposes.
- **Guaranteed entropy** — The generator always injects at least one character from each required category before filling the rest randomly, ensuring no policy bypass by pure chance.
- **Shuffle is secure** — Final character ordering uses `secrets.SystemRandom().shuffle()`, not `random.shuffle()`.
- **Never reuse passwords** — Use a password manager (e.g., Bitwarden, 1Password) to store generated passwords safely.

---

## 📄 License

This project is released for internal and personal use. For commercial distribution, please review your organization's security tool licensing requirements.

---

