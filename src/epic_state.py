from typing import Dict, Any, List
from datetime import datetime


class EpicState:
    """Persistent state across turns (continuity field from Maintain phase)."""

    def __init__(self):
        self.turn_count: int = 0
        self.domain: str = "EED"

        self.prev_steering_band: str = "normal"
        self.current_lane: str = "direct_answer"

        self.cfi_prev_state: Dict[str, Any] = {}
        self.cfi_curr_state: Dict[str, Any] = {}

        self.forecast_history: List[Dict[str, float]] = []
        self.band_history: List[str] = []
        self.mismatch_history: List[float] = []

        self.oscillation_index: float = 0.0
        self.calibration_summary: Dict[str, Any] = {}

        self.telemetry_records: List[Dict[str, Any]] = []
        self.claim_records: Dict[str, Dict[str, Any]] = {}
        self.anchor_weights: Dict[str, float] = {}

    def update_from_maintain(self, maintain_output: Dict[str, Any]) -> None:
        """Update persistent EPIC continuity state from Maintain phase output."""
        self.turn_count += 1

        self.domain = maintain_output.get("domain", self.domain)
        self.prev_steering_band = maintain_output.get("steering_band", self.prev_steering_band)
        self.current_lane = maintain_output.get("resolved_lane", self.current_lane)

        self.cfi_prev_state = self.cfi_curr_state
        self.cfi_curr_state = maintain_output.get("cfi_state", self.cfi_curr_state)

        self.forecast_history.append(maintain_output.get("forecast_scores", {}))
        self.band_history.append(maintain_output.get("steering_band", "normal"))
        self.mismatch_history.append(maintain_output.get("calibration_mismatch", 0.0))

        self.oscillation_index = maintain_output.get("oscillation_index", self.oscillation_index)

        self.calibration_summary.update(
            maintain_output.get("calibration_update_summary", {})
        )

        self.telemetry_records.append(
            maintain_output.get("telemetry_record", {})
        )

        claim_revision = maintain_output.get("claim_record_revision", {})
        if isinstance(claim_revision, dict):
            self.claim_records.update(claim_revision)

        anchor_adjustment = maintain_output.get("anchor_weight_adjustment", {})
        if isinstance(anchor_adjustment, dict):
            self.anchor_weights.update(anchor_adjustment)

    def get_telemetry(self) -> Dict[str, Any]:
        """Create a telemetry scaffold for the current turn."""
        latest_forecast = self.forecast_history[-1] if self.forecast_history else {}

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "turn_count": self.turn_count,
            "domain": self.domain,
            "task_profile": "query_processing",
            "forecast_scores": latest_forecast,
            "steering_band": self.prev_steering_band,
            "claim_units": [],
            "claim_states": [],
            "route_assignments": [],
            "anchor_map_summary": self.anchor_weights.copy(),
            "contradiction_flags": [],
            "retrieval_actions": [],
            "clarification_actions": [],
            "disclosure_types": [],
            "final_lane_mix": [self.current_lane] if self.current_lane else [],
            "post_outcome_signal": 0.0,
            "calibration_update_summary": self.calibration_summary.copy(),
        }
