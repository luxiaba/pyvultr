import json
import os
from typing import Dict


class TestFixture:
    def __init__(self):
        """Load all test fixtures."""
        self._fixtures: Dict = {}
        self.fixtures_dir = "./tests/fixtures"
        self.reload()

    def get(self, path: str) -> Dict:
        """Return the test fixture data loaded at the given Path."""
        suffix = "" if path.endswith(".json") else ".json"
        return self._fixtures.get(f"{path}{suffix}")

    def reload(self):
        """Load all JSON files in the fixtures directory."""
        self._fixtures = {}
        for path, _, files in os.walk(self.fixtures_dir):
            for name in files:
                abs_path = os.path.join(path, name)
                rel_path = os.path.relpath(abs_path, self.fixtures_dir)
                with open(abs_path, "r") as f:
                    content = json.loads(f.read())
                self._fixtures[rel_path] = content
