import numpy as np
from scipy.signal import butter, filtfilt, welch

BANDS = {
    "delta": (0.5, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 12.0),
    "beta":  (12.0, 30.0),
    "gamma": (30.0, 45.0),   # practical upper limit for consumer EEG
}

def bandpower(data: np.ndarray, fs: float, band: tuple) -> float:
    low, high = band
    nyq = 0.5 * fs
    b, a = butter(4, [low/nyq, high/nyq], btype="band")
    filtered = filtfilt(b, a, data)
    freqs, psd = welch(filtered, fs, nperseg=min(256, len(filtered)))
    idx = np.logical_and(freqs >= low, freqs <= high)
    return np.trapz(psd[idx], freqs[idx])

def extract_powers(eeg_window: np.ndarray, fs: float = 250.0) -> dict:
    return {name: float(bandpower(eeg_window, fs, limits))
            for name, limits in BANDS.items()}
