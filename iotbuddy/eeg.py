import numpy as np
from scipy.signal import butter, filtfilt, welch

BANDS = {
    "delta": (0.5, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 12.0),
    "beta": (12.0, 30.0),
    "gamma": (30.0, 45.0),
}


def _bandpower(data: np.ndarray, fs: float, band: tuple) -> float:
    low, high = band
    nyq = fs * 0.5
    if high >= nyq:
        high = nyq - 0.5
    if low >= high:
        return 0.0
    b, a = butter(4, [low / nyq, high / nyq], btype="band")
    filtered = filtfilt(b, a, data)
    freqs, psd = welch(filtered, fs, nperseg=min(256, len(filtered)))
    idx = np.logical_and(freqs >= low, freqs <= high)
    return float(np.trapz(psd[idx], freqs[idx])) if np.any(idx) else 0.0


def extract_powers(eeg_window: np.ndarray, fs: float = 250.0) -> dict:
    if eeg_window.ndim > 1:
        eeg_window = np.mean(eeg_window, axis=0)
    return {name: _bandpower(eeg_window, fs, limits) for name, limits in BANDS.items()}
