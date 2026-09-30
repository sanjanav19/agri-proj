import os
import subprocess
from pathlib import Path

# ---------------------------------------------------------
# PROJECT ROOT
# project_audit.py is inside agri-proj/project_audit/
# so we go one level up to agri-proj
# ---------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

print("=" * 75)
print("              FLYER PROJECT AUDIT")
print("=" * 75)

print("\nPROJECT ROOT:")
print(ROOT)


# =========================================================
# 1. GIT INFORMATION
# =========================================================

print("\n\n[1] GIT INFORMATION")
print("-" * 75)


def run_git(command):
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return result.stderr.strip()

        return result.stdout.strip()

    except Exception as e:
        return str(e)


print("\nCurrent branch:")
print(run_git(["git", "branch", "--show-current"]))

print("\nAll branches:")
print(run_git(["git", "branch"]))

print("\nGit status:")
status = run_git(["git", "status", "--short"])

if status:
    print(status)
else:
    print("Working tree clean")


# =========================================================
# 2. PROJECT STRUCTURE
# =========================================================

print("\n\n[2] PROJECT FILE STRUCTURE")
print("-" * 75)

ignore_folders = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules"
}

for path in sorted(ROOT.rglob("*")):

    # Ignore unnecessary folders
    if any(part in ignore_folders for part in path.parts):
        continue

    if path.is_file():

        relative_path = path.relative_to(ROOT)

        print(relative_path)


# =========================================================
# 3. IMPORTANT FILE / FOLDER CHECK
# =========================================================

print("\n\n[3] IMPORTANT PROJECT COMPONENTS")
print("-" * 75)

important_items = [
    "smart-farming-iot-dataset.ipynb",

    "person2_lstm",

    "latency",

    "models",

    "results",

    "person6-baseline-security-integration",

    "centralized_baseline.py",

    "edge_cloud_baseline.py",

    "encryption.py",

    "test_encryption.py",

    "energy_measurement.py",

    "federated_learning.py",

    "server.py",

    "client.py"
]


for item in important_items:

    matches = list(ROOT.rglob(item))

    if matches:

        print(f"\n[FOUND] {item}")

        for match in matches:

            print(
                "       ",
                match.relative_to(ROOT)
            )

    else:

        print(f"\n[MISSING] {item}")


# =========================================================
# 4. CSV RESULT FILES
# =========================================================

print("\n\n[4] CSV RESULT FILES")
print("-" * 75)

csv_files = list(ROOT.rglob("*.csv"))

if not csv_files:

    print("No CSV files found.")

else:

    for csv_file in sorted(csv_files):

        try:

            relative_path = csv_file.relative_to(ROOT)

            print("\nFILE:")
            print(relative_path)

            print("SIZE:", csv_file.stat().st_size, "bytes")

            with open(
                csv_file,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                lines = f.readlines()

            if lines:

                print(
                    "ROWS:",
                    max(0, len(lines) - 1)
                )

                print("FIRST FEW ROWS:")

                for line in lines[:6]:

                    print(
                        "   ",
                        line.strip()
                    )

        except Exception as e:

            print(
                "Could not read:",
                csv_file,
                e
            )


# =========================================================
# 5. PYTHON FILE SUMMARY
# =========================================================

print("\n\n[5] PYTHON FILE SUMMARY")
print("-" * 75)

python_files = list(ROOT.rglob("*.py"))

for py_file in sorted(python_files):

    if any(
        part in ignore_folders
        for part in py_file.parts
    ):
        continue

    try:

        text = py_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        lines = text.splitlines()

        functions = []
        classes = []

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("def "):

                functions.append(stripped)

            if stripped.startswith("class "):

                classes.append(stripped)

        print(
            "\nFILE:",
            py_file.relative_to(ROOT)
        )

        print(
            "Lines:",
            len(lines)
        )

        if functions:

            print("Functions:")

            for function in functions:

                print(
                    "   ",
                    function
                )

        if classes:

            print("Classes:")

            for cls in classes:

                print(
                    "   ",
                    cls
                )

    except Exception as e:

        print(
            "Could not inspect:",
            py_file,
            e
        )


# =========================================================
# 6. SECURITY IMPLEMENTATION CHECK
# =========================================================

print("\n\n[6] SECURITY / ENCRYPTION CHECK")
print("-" * 75)

security_keywords = [
    "encrypt",
    "decrypt",
    "encryption",
    "decryption",
    "cipher",
    "AES",
    "Fernet",
    "encrypted",
    "payload"
]

security_found = False

for py_file in sorted(python_files):

    if any(
        part in ignore_folders
        for part in py_file.parts
    ):
        continue

    try:

        text = py_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        found = []

        for keyword in security_keywords:

            if keyword.lower() in text.lower():

                found.append(keyword)

        if found:

            security_found = True

            print(
                "\nFILE:",
                py_file.relative_to(ROOT)
            )

            print(
                "Found:",
                ", ".join(found)
            )

    except:
        pass


if not security_found:

    print(
        "No obvious encryption implementation found."
    )


# =========================================================
# 7. LATENCY / ENERGY CHECK
# =========================================================

print("\n\n[7] LATENCY / ENERGY / PERFORMANCE CHECK")
print("-" * 75)

performance_keywords = [
    "latency",
    "energy",
    "power",
    "cpu",
    "network",
    "payload",
    "overhead",
    "time"
]

performance_found = False

for py_file in sorted(python_files):

    if any(
        part in ignore_folders
        for part in py_file.parts
    ):
        continue

    try:

        text = py_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        found = []

        for keyword in performance_keywords:

            if keyword.lower() in text.lower():

                found.append(keyword)

        if found:

            performance_found = True

            print(
                "\nFILE:",
                py_file.relative_to(ROOT)
            )

            print(
                "Found:",
                ", ".join(found)
            )

    except:
        pass


if not performance_found:

    print(
        "No obvious performance measurement code found."
    )


# =========================================================
# 8. RESULT FOLDERS
# =========================================================

print("\n\n[8] RESULT / OUTPUT FOLDERS")
print("-" * 75)

result_names = [
    "results",
    "result",
    "output",
    "outputs"
]

for name in result_names:

    matches = [
        p for p in ROOT.rglob("*")
        if p.is_dir()
        and p.name.lower() == name.lower()
    ]

    for folder in matches:

        print(
            "\nRESULT FOLDER:",
            folder.relative_to(ROOT)
        )

        files_inside = list(folder.rglob("*"))

        if files_inside:

            for file in files_inside:

                if file.is_file():

                    print(
                        "   ",
                        file.relative_to(ROOT)
                    )

        else:

            print("    EMPTY")


# =========================================================
# 9. FINAL AUDIT MESSAGE
# =========================================================

print("\n")
print("=" * 75)
print("                    AUDIT COMPLETE")
print("=" * 75)

print("""
IMPORTANT:

This audit does NOT modify your project.

It only checks:
- Git branch/status
- project structure
- important files
- Python files
- CSV result files
- encryption-related code
- latency-related code
- energy-related code
- result/output folders

Copy the COMPLETE terminal output and send it to ChatGPT.

I will then identify:

1. COMPLETED tasks
2. PARTIALLY completed tasks
3. MISSING tasks
4. YOUR remaining work
5. TEAM MEMBERS' remaining work
6. WHAT OUTPUTS YOU CAN SHOW YOUR PROFESSOR TOMORROW
7. WHAT YOU SHOULD RUN BEFORE THE DEMO
""")

print("=" * 75)