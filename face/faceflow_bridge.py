"""
Thin adapter around FaceFlow.
Keeps IoT Buddy decoupled from FaceFlow internals.
"""

from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FaceFlowBridge:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._engine = None
        self._workflow_name = "buddy_emotion"

        if enabled:
            self._init_faceflow()

    def _init_faceflow(self):
        try:
            # Import only when needed
            from faceflow.core.engine import FaceFlowEngine
            from faceflow.core.workflow import Workflow

            # These step names follow the FaceFlow design
            # Adjust imports if the actual class names differ slightly
            from faceflow.steps.detection import MediaPipeFaceDetector
            from faceflow.steps.emotion import DeepFaceEmotionAnalyzer

            self._engine = FaceFlowEngine()

            wf = (
                Workflow(self._workflow_name)
                .add_step(MediaPipeFaceDetector())
                .add_step(DeepFaceEmotionAnalyzer(detector_backend="mediapipe"))
            )
            self._engine.register_workflow(wf)
            logger.info("FaceFlow bridge initialized")
        except Exception as e:
            logger.warning(f"FaceFlow not available – running without face analysis: {e}")
            self.enabled = False
            self._engine = None

    def analyze_frame(self, frame) -> Optional[Dict[str, Any]]:
        """
        Analyze a single BGR frame (OpenCV style).
        Returns a normalized dict or None if disabled / no face.
        """
        if not self.enabled or self._engine is None or frame is None:
            return None

        try:
            result = self._engine.execute(self._workflow_name, {"image": frame})

            # FaceFlow typically returns a structure with detected faces.
            # We take the first face for simplicity (multi-face can be extended later).
            faces = result.get("faces") or result.get("results") or []
            if not faces:
                return None

            face = faces[0]
            dominant = face.get("dominant_emotion") or face.get("emotion") or "neutral"
            scores = face.get("emotion_scores") or face.get("emotions") or {}

            return {
                "dominant": str(dominant).lower(),
                "scores": {k.lower(): float(v) for k, v in scores.items()},
                "raw": face,
            }
        except Exception as e:
            logger.debug(f"Face analysis failed: {e}")
            return None

    def is_available(self) -> bool:
        return self.enabled and self._engine is not None
