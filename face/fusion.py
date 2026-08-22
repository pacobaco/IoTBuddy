from typing import Dict

def fuse_states(eeg_powers: Dict[str, float], affect: Dict) -> Dict[str, float]:
    """
    Lightly bias EEG band powers using facial affect.
    Returns a new dict – original is not modified.
    """
    adjusted = dict(eeg_powers)
    valence = affect.get("valence", 0.0)
    arousal = affect.get("arousal", 0.5)

    # Positive valence gently supports relaxed / creative bands
    if valence > 0.25:
        adjusted["alpha"] = adjusted.get("alpha", 0.0) * (1.0 + 0.18 * valence)
        adjusted["theta"] = adjusted.get("theta", 0.0) * (1.0 + 0.12 * valence)

    # High arousal + negative valence increases beta (alert / tense)
    if arousal > 0.55 and valence < -0.2:
        adjusted["beta"] = adjusted.get("beta", 0.0) * (1.0 + 0.25 * arousal)

    # Very high positive arousal can give a small gamma bump
    if valence > 0.5 and arousal > 0.7:
        adjusted["gamma"] = adjusted.get("gamma", 0.0) * 1.15

    return adjusted
