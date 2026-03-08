from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict


REQUIRED_TOP_LEVEL_KEYS = {
    "system",
    "domains",
    "platonic_5_plus_1",
    "cfi",
    "arc",
    "route_system",
    "disclosure",
    "governance",
    "health_monitors",
    "learning_and_adaptation",
    "telemetry",
    "evaluation",
    "runtime",
}


def load_epic_spec(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))

    missing = REQUIRED_TOP_LEVEL_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"EPIC spec missing required keys: {sorted(missing)}")

    return data        # Version check
        version = data.get("system", {}).get("version")
        if version != self.EXPECTED_VERSION:
            raise ValueError(
                f"Spec version mismatch: expected {self.EXPECTED_VERSION}, "
                f"got {version or 'missing'}"
            )

        # Top-level keys
        missing_keys = [k for k in self.REQUIRED_TOP_KEYS if k not in data]
        if missing_keys:
            raise ValueError(f"Missing required top-level keys: {', '.join(missing_keys)}")

        # Optional: deeper spot-checks (add more as needed)
        if "cfi" in data and "forecast_dimensions" not in data["cfi"]:
            raise ValueError("cfi section missing 'forecast_dimensions'")

        if "arc" in data and "trust_lattice" not in data["arc"]:
            raise ValueError("arc section missing 'trust_lattice'")

        return data

    @property
    def full_spec(self) -> Dict[str, Any]:
        """Returns the full loaded and validated spec."""
        return self.spec
