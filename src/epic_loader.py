# src/epic_loader.py
import json
from pathlib import Path
from typing import Dict, Any

class EpicSpecLoader:
    """Loads and validates the EPIC operational spec JSON."""

    def __init__(self, spec_path: str = "docs/EPIC-v10-Operational-Spec.json"):
        self.spec_path = Path(spec_path)
        self.spec: Dict[str, Any] = self._load_and_validate()

    def _load_and_validate(self) -> Dict[str, Any]:
        if not self.spec_path.exists():
            raise FileNotFoundError(f"Spec file not found: {self.spec_path}")

        with self.spec_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Basic structural validation (expand as needed)
        required_top_keys = ["system", "domains", "platonic_5_plus_1", "cfi", "arc", "route_system"]
        missing = [k for k in required_top_keys if k not in data]
        if missing:
            raise ValueError(f"Missing required top-level keys: {missing}")

        return data

    @property
    def full_spec(self) -> Dict[str, Any]:
        return self.spec
