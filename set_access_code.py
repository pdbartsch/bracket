"""Set the 6-character access code for the bracket entry page.

Usage:
    uv run set_access_code.py MYCODE
"""

import hashlib
import sys


def main():
    if len(sys.argv) != 2 or len(sys.argv[1]) != 6:
        print("Usage: uv run set_access_code.py <6-char-code>")
        sys.exit(1)

    code = sys.argv[1]
    hash_hex = hashlib.sha256(code.encode()).hexdigest()

    entry_path = "docs/entry.html"
    with open(entry_path) as f:
        content = f.read()

    # Replace the placeholder or existing hash
    import re
    content = re.sub(
        r"const ACCESS_HASH = '[^']*';",
        f"const ACCESS_HASH = '{hash_hex}';",
        content,
    )

    with open(entry_path, "w") as f:
        f.write(content)

    print(f"Access code set: {code}")
    print(f"SHA-256 hash:    {hash_hex}")
    print(f"Updated:         {entry_path}")


if __name__ == "__main__":
    main()
