# scripts/tfr.py

import numpy as np
from mne.time_frequency import tfr_morlet

def compute_tfr(epochs, picks, freqs=None, n_cycles=None):
    """
    Compute Morlet-wavelet time–frequency representation and average across trials.
    """
    if freqs is None:
        freqs = np.arange(4, 31, 2)
    if n_cycles is None:
        n_cycles = freqs / 2.

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
    """
    power_avg.plot(
        baseline=(None, 0),
        mode='logratio',
        tmin=tmin, tmax=tmax,
        fmin=fmin, fmax=fmax,
    )

if __name__ == "__main__":
    import mne
    from scripts.load_and_plot import load_and_plot
    from scripts.preprocess import filter_raw, reject_epochs

    # 1. Load raw data and picks
    raw, picks = load_and_plot()

    # 2. Find events and preprocess
    events = mne.find_events(raw, stim_channel='STI 014')
    raw_filt = filter_raw(raw)
    epochs = reject_epochs(raw_filt, events)

    # 3. Compute & plot TFR on the first EEG pick
    power_avg = compute_tfr(epochs, picks[:1])
    plot_tfr(power_avg)

    # 4. Confirmation message
    print("TFR script ran successfully.")

