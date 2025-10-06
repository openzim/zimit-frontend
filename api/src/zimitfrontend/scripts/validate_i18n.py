#!/usr/bin/env python3
"""Validate i18n translation files and usage in code."""

import json
import re
import sys
from pathlib import Path
from typing import Any

# ruff: noqa: T201


def load_json(path: Path) -> dict[str, Any]:
    """Load and parse a JSON file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)  # type: ignore


def get_all_keys(data: dict[str, Any], prefix: str = "") -> set[str]:
    """Recursively extract all keys from nested dictionary."""
    keys: set[str] = set()
    for key, value in data.items():
        # Skip metadata
        if key == "@metadata":
            continue
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(
                get_all_keys(
                    value, full_key  # pyright: ignore[reportUnknownArgumentType]
                )
            )
        else:
            keys.add(full_key)
    return keys


def extract_keys_from_python(file_path: Path) -> set[str]:
    """Extract i18n keys from Python files."""
    content = file_path.read_text(encoding="utf-8")
    # Match: i18n.t("key" or i18n.t('key'
    pattern = r'i18n\.t\s*\(\s*["\']([^"\']+)["\']'
    return set(re.findall(pattern, content))


def extract_keys_from_jinja(file_path: Path) -> set[str]:
    """Extract i18n keys from Jinja templates."""
    content = file_path.read_text(encoding="utf-8")
    # Match: translate('key') or translate("key")
    pattern = r'translate\s*\(\s*["\']([^"\']+)["\']'
    return set(re.findall(pattern, content))


def extract_keys_from_vue_ts(file_path: Path) -> set[str]:
    """Extract i18n keys from Vue/TypeScript files."""
    content = file_path.read_text(encoding="utf-8")
    keys: set[str] = set()
    # Match: $t('key') or $t("key") - used in templates
    pattern1 = r'\$t\s*\(\s*["\']([^"\']+)["\']'
    keys.update(re.findall(pattern1, content))
    # Match: t('key') or t("key") - used in script setup sections
    # Use word boundary to avoid matching $t, translate, etc.
    pattern2 = r'\bt\s*\(\s*["\']([^"\']+)["\']'
    keys.update(re.findall(pattern2, content))
    # Match: keypath="key" or keypath='key' (for i18n-t component)
    pattern3 = r'keypath\s*=\s*["\']([^"\']+)["\']'
    keys.update(re.findall(pattern3, content))
    return keys


def main() -> int:
    """Main validation function."""
    # Find repository root (go up from this script location)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent.parent
    locales_dir = repo_root / "locales"
    api_dir = repo_root / "api"
    ui_dir = repo_root / "ui"

    print("🔍 Validating i18n translations...")
    print()

    errors: list[str] = []

    # 1. Load and validate locale files
    print("📁 Checking locale files...")
    en_path = locales_dir / "en.json"
    qqq_path = locales_dir / "qqq.json"

    if not en_path.exists():
        errors.append(f"❌ Missing en.json at {en_path}")
        return 1

    if not qqq_path.exists():
        errors.append(f"❌ Missing qqq.json at {qqq_path}")
        return 1

    en_data = load_json(en_path)
    qqq_data = load_json(qqq_path)

    en_keys = get_all_keys(en_data)
    qqq_keys = get_all_keys(qqq_data)

    print(f"   Found {len(en_keys)} keys in en.json")
    print(f"   Found {len(qqq_keys)} keys in qqq.json")

    # Check en.json and qqq.json have matching keys
    if en_keys != qqq_keys:
        errors.append("❌ Keys in en.json and qqq.json do not match!")
        missing_in_qqq = en_keys - qqq_keys
        missing_in_en = qqq_keys - en_keys
        if missing_in_qqq:
            errors.append(f"   Missing in qqq.json: {sorted(missing_in_qqq)}")
        if missing_in_en:
            errors.append(f"   Extra in qqq.json: {sorted(missing_in_en)}")
    else:
        print("   ✅ en.json and qqq.json keys match")

    # Check other locale files
    for locale_file in sorted(locales_dir.glob("*.json")):
        if locale_file.name in ["en.json", "qqq.json"]:
            continue
        locale_data = load_json(locale_file)
        locale_keys = get_all_keys(locale_data)
        extra_keys = locale_keys - en_keys
        if extra_keys:
            errors.append(
                f"❌ {locale_file.name} has keys not in en.json: {sorted(extra_keys)}"
            )
        else:
            print(f"   ✅ {locale_file.name} keys are valid subset")

    print()

    # 2. Extract keys from code
    print("🔎 Extracting keys from code...")
    code_keys: set[str] = set()
    # Track which files use which keys
    key_locations: dict[str, list[str]] = {}

    # Python files
    if api_dir.exists():
        for py_file in api_dir.rglob("*.py"):
            # Skip node_modules and this validation script itself
            if "node_modules" in str(py_file) or py_file.samefile(Path(__file__)):
                continue
            keys = extract_keys_from_python(py_file)
            if keys:
                print(f"   Found {len(keys)} keys in {py_file.relative_to(repo_root)}")
                code_keys.update(keys)
                for key in keys:
                    key_locations.setdefault(key, []).append(
                        str(py_file.relative_to(repo_root))
                    )

    # Jinja templates (HTML and TXT files)
    if api_dir.exists():
        for template_file in list(api_dir.rglob("*.html")) + list(
            api_dir.rglob("*.txt")
        ):
            if "node_modules" in str(template_file):
                continue
            keys = extract_keys_from_jinja(template_file)
            if keys:
                rel_path = template_file.relative_to(repo_root)
                print(f"   Found {len(keys)} keys in {rel_path}")
                code_keys.update(keys)
                for key in keys:
                    key_locations.setdefault(key, []).append(
                        str(template_file.relative_to(repo_root))
                    )

    # Vue/TS files
    if ui_dir.exists():
        for vue_file in ui_dir.rglob("*.vue"):
            if "node_modules" in str(vue_file):
                continue
            keys = extract_keys_from_vue_ts(vue_file)
            if keys:
                print(f"   Found {len(keys)} keys in {vue_file.relative_to(repo_root)}")
                code_keys.update(keys)
                for key in keys:
                    key_locations.setdefault(key, []).append(
                        str(vue_file.relative_to(repo_root))
                    )

        for ts_file in ui_dir.rglob("*.ts"):
            if "node_modules" in str(ts_file):
                continue
            keys = extract_keys_from_vue_ts(ts_file)
            if keys:
                print(f"   Found {len(keys)} keys in {ts_file.relative_to(repo_root)}")
                code_keys.update(keys)
                for key in keys:
                    key_locations.setdefault(key, []).append(
                        str(ts_file.relative_to(repo_root))
                    )

    print(f"   Total unique keys used in code: {len(code_keys)}")
    print()

    # 3. Cross-validate
    print("🔗 Cross-validating code vs. locale files...")

    # Keys used in code but not in en.json
    missing_in_locales = code_keys - en_keys
    if missing_in_locales:
        errors.append(
            f"❌ Keys used in code but missing in en.json ({len(missing_in_locales)}):"
        )
        for key in sorted(missing_in_locales):
            files = ", ".join(key_locations[key])
            errors.append(f"   - {key} (used in: {files})")
    else:
        print("   ✅ All code keys exist in en.json")

    # Keys in en.json but not used in code
    # Ignore special keys that are used differently
    # (e.g., "language" is used by the i18n system itself)
    ignored_keys = {"language"}
    unused_keys = en_keys - code_keys - ignored_keys
    if unused_keys:
        errors.append(f"❌ Keys in en.json but not used in code ({len(unused_keys)}):")
        for key in sorted(unused_keys):
            errors.append(f"   - {key}")
    else:
        print("   ✅ All en.json keys are used in code")

    print()

    # 4. Check that all locale files are referenced in ui/src/i18n.ts
    print("📋 Checking locale files are registered in ui/src/i18n.ts...")
    i18n_ts_path = ui_dir / "src" / "i18n.ts"
    if i18n_ts_path.exists():
        i18n_ts_content = i18n_ts_path.read_text(encoding="utf-8")
        # Extract language codes from supportedLanguages array (active and commented)
        # Match both: { code: 'en', ... } and //  { code: 'en', ... }
        pattern = r"(?://\s*)?{\s*code:\s*['\"]([^'\"]+)['\"]"
        referenced_codes = set(re.findall(pattern, i18n_ts_content))

        # Get all locale files except qqq.json (which is for documentation)
        locale_codes = set()
        for locale_file in locales_dir.glob("*.json"):
            if locale_file.name != "qqq.json":
                locale_code = locale_file.stem
                locale_codes.add(locale_code)

        # Check for missing references
        missing_refs = locale_codes - referenced_codes
        if missing_refs:
            errors.append(
                f"❌ Locale files not referenced in ui/src/i18n.ts "
                f"({len(missing_refs)}):"
            )
            for code in sorted(missing_refs):
                errors.append(
                    f"   - {code}.json (add to supportedLanguages array, "
                    f"can be commented out)"
                )
        else:
            print("   ✅ All locale files are registered in ui/src/i18n.ts")

        # Check for references to non-existent files
        extra_refs = referenced_codes - locale_codes
        if extra_refs:
            errors.append(
                f"❌ Languages in ui/src/i18n.ts without locale files "
                f"({len(extra_refs)}):"
            )
            for code in sorted(extra_refs):
                errors.append(f"   - {code} (missing locales/{code}.json)")
    else:
        print("   ⚠️  ui/src/i18n.ts not found, skipping check")

    print()

    # 5. Report results
    if errors:
        print("❌ Validation failed!\n")
        for error in errors:
            print(error)
        return 1
    else:
        print("✅ All i18n validation checks passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
