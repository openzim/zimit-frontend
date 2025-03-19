import json
import os
import re
from typing import Set, Dict, List, Tuple
from pathlib import Path

class LocaleKeyValidator:
    def __init__(self, locales_dir: str, project_dir: str, ignored_keys: Set[str] = None):
        self.locales_dir = Path(locales_dir)
        self.project_dir = Path(project_dir)
        self.all_json_keys = set()
        self.leaf_json_keys = set()
        self.used_keys = set()
        self.parent_keys = set()
        self.key_hierarchy = {}
        self.ignored_keys = ignored_keys or set()

    def flatten_json(self, json_obj: Dict, parent_key: str = '') -> Set[str]:
        keys = set()
        
        for key, value in json_obj.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            
            if current_key in self.ignored_keys or key in self.ignored_keys:
                continue
                
            keys.add(current_key)
            
            if isinstance(value, dict):
                self.parent_keys.add(current_key)
            else:
                self.leaf_json_keys.add(current_key)
            
            if parent_key:
                if parent_key not in self.key_hierarchy:
                    self.key_hierarchy[parent_key] = set()
                self.key_hierarchy[parent_key].add(key)
                self.parent_keys.add(parent_key)
            
            if isinstance(value, dict):
                nested_keys = self.flatten_json(value, current_key)
                keys.update(nested_keys)
        
        return keys

    def load_json_keys(self) -> None:
        json_files = ['en.json', 'qqq.json']
        
        for filename in json_files:
            file_path = self.locales_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        json_data = json.load(f)
                        self.all_json_keys.update(self.flatten_json(json_data))
                    except json.JSONDecodeError:
                        print(f"Warning: Couldn't parse {filename}")

    def extract_keys_from_python(self, content: str) -> Set[str]:
        patterns = [
            r'_\([\'"]([^\'"]+)[\'"]\)',
            r'gettext\([\'"]([^\'"]+)[\'"]\)',
            r'i18n\.get_string\([\'"]([^\'"]+)[\'"]\)',
        ]
        
        found_keys = set()
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            found_keys.update(match.group(1) for match in matches)
        
        return {k for k in found_keys if k not in self.ignored_keys}

    def scan_python_files(self) -> None:
        for py_file in self.project_dir.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    keys = self.extract_keys_from_python(content)
                    self.used_keys.update(keys)
            except (PermissionError, UnicodeDecodeError) as e:
                pass

    def mark_parent_keys_as_used(self) -> None:
        all_used = self.used_keys.copy()
        
        for key in all_used:
            parts = key.split('.')
            for i in range(1, len(parts)):
                parent = '.'.join(parts[:i])
                if parent and parent not in self.ignored_keys:
                    self.used_keys.add(parent)

    def get_unused_keys(self) -> Set[str]:
        unused = self.all_json_keys - self.used_keys
        return unused - self.parent_keys

    def get_missing_keys(self) -> Set[str]:
        return self.used_keys - self.all_json_keys

    def validate(self) -> Tuple[Set[str], Set[str]]:
        self.load_json_keys()
        self.scan_python_files()
        self.mark_parent_keys_as_used()
        
        unused = self.get_unused_keys()
        missing = self.get_missing_keys()
        
        return unused, missing

def main():
    validator = LocaleKeyValidator(
        locales_dir='./locales',
        project_dir='.',
        ignored_keys={"@metadata", "language"}
    )
    
    unused, missing = validator.validate()
    
    print("Unused keys:")
    for key in sorted(unused):
        print(f"  - {key}")
    
    print("\nMissing keys:")
    for key in sorted(missing):
        print(f"  - {key}")

if __name__ == '__main__':
    main()