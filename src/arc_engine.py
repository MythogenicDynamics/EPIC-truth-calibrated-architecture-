from typing import Dict, Any, List

class ARCEngine:
    """Full ARC implementation — claim decomposition, lattice scoring, state assignment."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec['arc']

    def decompose_claims(self, prompt: str) -> List[str]:
        return prompt.split('. ')  # Simple sentence split - expand with real parser

    def score_anchors(self, anchors: Dict[str, float]) -> float:
        rules = self.spec['trust_lattice']['rules']
        classes = self.spec['trust_lattice']['anchor_classes']

        weighted_sum = sum(anchors.get(cls, 0.0) * classes[cls]['default_weight'] for cls in classes)
        distinct_classes = len([c for c in anchors if anchors[c] > 0.0])
        diversity_bonus = min(distinct_classes * rules['diversity_bonus']['bonus_per_distinct_anchor_class'], rules['diversity_bonus']['max_bonus'])
        single_source_penalty = rules['single_source_dampener']['decay_factor'] if distinct_classes == 1 else 0.0
        unsupported_penalty = rules['unsupported_specificity_penalty']['penalty'] if weighted_sum < 0.5 else 0.0
        staleness_penalty = 0.1

        score = weighted_sum + diversity_bonus - single_source_penalty - unsupported_penalty - staleness_penalty
        return max(0.0, min(1.0, score))

    def assign_states(self, claims: List[str], anchor_scores: List[float]) -> List[str]:
        states = []
        for score in anchor_scores:
            if score >= 0.9:
                states.append("verified")
            elif score >= 0.7:
                states.append("well_supported")
            elif score >= 0.5:
                states.append("reasoned_inference")
            elif score >= 0.3:
                states.append("weak_inference")
            elif score >= 0.1:
                states.append("speculative")
            else:
                states.append("unknown")
        return states
