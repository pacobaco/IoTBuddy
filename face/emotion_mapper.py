from typing import Dict, Any

EMOTION_TO_VALENCE = {
    "happy": 0.85,
    "surprised": 0.35,
    "neutral": 0.0,
    "sad": -0.65,
    "angry": -0.75,
    "fear": -0.55,
    "disgust": -0.45,
}

def emotion_to_affect(dominant: str, scores: Dict[str, float] | None = None) -> Dict[str, Any]:
    """
    Convert FaceFlow emotion output into a simple affective signal.
    """
    scores = scores or {}
    valence = EMOTION_TO_VALENCE.get(dominant.lower(), 0.0)
    arousal = max(scores.values()) if scores else 0.5

    return {
        "dominant_emotion": dominant.lower(),
        "valence": float(valence),
        "arousal": float(arousal),
        "scores": scores,
    }
