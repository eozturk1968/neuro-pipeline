import numpy as np
from mne.time_frequency import tfr_morlet

def compute_tfr(epochs, picks, freqs=None, n_cycles=None):
    """
    Compute Morlet-wavelet time–frequency representation and average.

    Parameters
    ----------
    epochs : mne.Epochs
    picks : list of int or channel names
    freqs : array-like | None
        Frequencies of interest in Hz.
    n_cycles : array-like | None
        Number of cycles per frequency.

    Returns
    -------
    power_avg : mne.time_frequency.EpochsTFR
    """
    if freqs is None:
        freqs = np.arange(4, 31, 2)  # 4–30 Hz
    if n_cycles is None:
        n_cycles = freqs / 2.        # cycles per frequency

    power = tfr_morlet(
        epochs,
        picks=picks,
        freqs=freqs,
        n_cycles=n_cycles,
        return_itc=False,
        average=False
    )
    return power.average()

def plot_tfr(power_avg, tmin=-0.2, tmax=0.8, fmin=4, fmax=30):
    """
    Plot averaged time–frequency power with baseline correction.

    Parameters
    ----------
    power_avg : mne.time_frequency.EpochsTFR
    tmin, tmax : float
        Time window to display.
    fmin, fmax : float
        Frequency range to display.
    """
    power_avg.plot(
        baseline=(None, 0),
        mode='logratio',
        tmin=tmin, tmax=tmax,
        fmin=fmin, fmax=fmax
    )
