"""
╔══════════════════════════════════════════════════════════════════╗
║          Enterprise Random Password Generator                    ║
║          Secure | Professional | Feature-Rich                    ║
╚══════════════════════════════════════════════════════════════════╝

Author  : Enterprise Security Tools
Version : 1.0.0
Module  : secrets (cryptographically secure random generation)
"""

import secrets
import string
import os
from datetime import datetime


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def print_banner():
    """Display the application banner."""
    print("\n" + "=" * 60)
    print("   🔐  Enterprise Random Password Generator  🔐")
    print("=" * 60)


def print_separator():
    """Print a visual separator line."""
    print("-" * 60)


# ─────────────────────────────────────────────
#  INPUT VALIDATION
# ─────────────────────────────────────────────

def get_positive_integer(prompt: str, min_val: int = 1, max_val: int = 512) -> int:
    """
    Prompt the user for a positive integer within [min_val, max_val].
    Loops until valid input is received.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if value < min_val:
                print(f"  ⚠  Please enter a value of at least {min_val}.")
            elif value > max_val:
                print(f"  ⚠  Please enter a value no greater than {max_val}.")
            else:
                return value
        except ValueError:
            print("  ✖  Invalid input. Please enter a whole number.")


def get_yes_no(prompt: str) -> bool:
    """Ask a yes/no question and return True for 'y', False for 'n'."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  ⚠  Please enter 'y' or 'n'.")


# ─────────────────────────────────────────────
#  CHARACTER POOL BUILDER
# ─────────────────────────────────────────────

def build_character_pool(include_special: bool) -> str:
    """
    Build the character pool used for password generation.

    Args:
        include_special: Whether to include punctuation characters.

    Returns:
        A string containing all allowed characters.
    """
    pool = string.ascii_letters + string.digits  # upper + lower + digits
    if include_special:
        pool += string.punctuation
    return pool


# ─────────────────────────────────────────────
#  PASSWORD STRENGTH EVALUATOR
# ─────────────────────────────────────────────

def evaluate_strength(password: str) -> tuple[str, str]:
    """
    Evaluate the strength of a password based on length and character variety.

    Scoring rubric
    ──────────────
    +1  length ≥ 8
    +1  length ≥ 12
    +1  length ≥ 16
    +1  contains uppercase letter
    +1  contains lowercase letter
    +1  contains digit
    +1  contains special character

    Score → Label
    0-3  → Weak   🔴
    4-5  → Medium 🟡
    6-7  → Strong 🟢

    Returns:
        (label, coloured emoji label)
    """
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 3:
        return "Weak", "🔴 Weak"
    if score <= 5:
        return "Medium", "🟡 Medium"
    return "Strong", "🟢 Strong"


# ─────────────────────────────────────────────
#  CORE GENERATOR
# ─────────────────────────────────────────────

def generate_password(length: int, include_special: bool) -> str:
    """
    Generate a cryptographically secure password.

    Guarantees at least one character from each required category,
    then fills the remainder from the full pool, and finally shuffles
    everything so the mandatory characters aren't always at the start.

    Args:
        length         : Desired password length (≥ 4).
        include_special: Whether to include punctuation.

    Returns:
        The generated password as a plain string.
    """
    pool = build_character_pool(include_special)

    # ── Mandatory characters (one per required category) ──
    mandatory = [
        secrets.choice(string.ascii_uppercase),   # at least 1 uppercase
        secrets.choice(string.ascii_lowercase),   # at least 1 lowercase
        secrets.choice(string.digits),            # at least 1 digit
    ]
    if include_special:
        mandatory.append(secrets.choice(string.punctuation))  # at least 1 special

    # ── Fill the rest from the full pool ──
    remaining_length = length - len(mandatory)
    remaining_chars  = [secrets.choice(pool) for _ in range(remaining_length)]

    # ── Combine and shuffle using secrets for secure ordering ──
    password_chars = mandatory + remaining_chars
    # secrets.SystemRandom is CSPRNG-backed; use it for shuffle
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def generate_multiple_passwords(
    length: int,
    count: int,
    include_special: bool,
) -> list[str]:
    """
    Generate 'count' passwords of the given length.

    Args:
        length         : Desired password length.
        count          : Number of passwords to generate.
        include_special: Whether to include punctuation.

    Returns:
        List of generated password strings.
    """
    return [generate_password(length, include_special) for _ in range(count)]


# ─────────────────────────────────────────────
#  FILE SAVER
# ─────────────────────────────────────────────

def save_passwords_to_file(passwords: list[str], length: int) -> str:
    """
    Append generated passwords to 'saved_passwords.txt' in the
    current working directory.

    Each batch is headed with a timestamp and password length so the
    file remains readable after many sessions.

    Args:
        passwords: List of password strings to save.
        length   : The length used to generate this batch.

    Returns:
        The absolute path of the file that was written.
    """
    filename  = "saved_passwords.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{'─' * 50}\n")
        f.write(f"Generated : {timestamp}\n")
        f.write(f"Length    : {length}\n")
        f.write(f"Count     : {len(passwords)}\n")
        f.write(f"{'─' * 50}\n")
        for idx, pwd in enumerate(passwords, start=1):
            label, _ = evaluate_strength(pwd)
            f.write(f"  [{idx:>3}]  {pwd}  ({label})\n")

    return os.path.abspath(filename)


# ─────────────────────────────────────────────
#  DISPLAY RESULTS
# ─────────────────────────────────────────────

def display_passwords(passwords: list[str]) -> None:
    """
    Print a formatted table of passwords with their strength ratings.

    Args:
        passwords: List of password strings to display.
    """
    print_separator()
    print(f"  {'#':<5} {'Password':<45} {'Strength'}")
    print_separator()
    for idx, pwd in enumerate(passwords, start=1):
        _, emoji_label = evaluate_strength(pwd)
        print(f"  {idx:<5} {pwd:<45} {emoji_label}")
    print_separator()


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def show_menu() -> None:
    """Display the main interactive menu."""
    print("\n  Main Menu")
    print("  ─────────")
    print("  [1]  Generate password(s)")
    print("  [2]  Exit")


def run() -> None:
    """
    Application entry-point.

    Drives the menu loop: collects user preferences, generates
    passwords, displays results, optionally saves to file, then
    asks whether to continue or quit.
    """
    print_banner()
    print("  Welcome! This tool generates cryptographically secure")
    print("  passwords using Python's 'secrets' module.\n")

    while True:
        show_menu()
        choice = input("\n  Enter your choice: ").strip()

        # ── Exit ──────────────────────────────────────────────────────
        if choice == "2":
            print("\n  👋  Thank you for using Enterprise Password Generator.")
            print("      Stay secure!\n")
            break

        # ── Generate ──────────────────────────────────────────────────
        elif choice == "1":
            print_separator()

            # 1. Password length
            length = get_positive_integer(
                "  Enter desired password length (4–512): ",
                min_val=4,
                max_val=512,
            )

            # 2. Special characters toggle
            include_special = get_yes_no("  Include special characters?")

            # 3. Number of passwords
            count = get_positive_integer(
                "  How many passwords to generate? (1–50): ",
                min_val=1,
                max_val=50,
            )

            # 4. Generate
            passwords = generate_multiple_passwords(length, count, include_special)

            # 5. Display
            print(f"\n  ✅  Generated {count} password(s) of length {length}:\n")
            display_passwords(passwords)

            # 6. Save to file (optional)
            if get_yes_no("\n  Save password(s) to file?"):
                filepath = save_passwords_to_file(passwords, length)
                print(f"  💾  Saved to: {filepath}")

        # ── Invalid option ─────────────────────────────────────────────
        else:
            print("  ⚠  Invalid choice. Please enter 1 or 2.")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    run()