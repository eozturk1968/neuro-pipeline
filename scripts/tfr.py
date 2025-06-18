# scripts/tfr.py

import numpy as np
from mne.time_frequency import tfr_morlet
import csv


def compute_tfr(epochs, picks, freqs=None, n_cycles=None):
    """
    Compute Morlet-wavelet time–frequency representation and average across trials.

    Parameters
    ----------
    epochs : mne.Epochs
    picks : list of channel indices or names
    freqs : array-like | None
        Frequencies of interest in Hz. Default: 4–30 Hz in steps of 2.
    n_cycles : array-like | None
        Number of cycles per frequency. Default: freqs / 2.

    Returns
    -------
    power_avg : mne.time_frequency.EpochsTFR
    """
    if freqs is None:
        freqs = np.arange(4, 31, 2)  # 4, 6, …, 30 Hz
    if n_cycles is None:
        n_cycles = freqs / 2.        # e.g. 2 cycles at 4 Hz, 15 cycles at 30 Hz

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
        Time window (s) to display.
    fmin, fmax : float
        Frequency range (Hz) to display.
    """
    power_avg.plot(
        baseline=(None, 0),
        mode='logratio',
        tmin=tmin, tmax=tmax,
        fmin=fmin, fmax=fmax,
    )


def export_band_power(power_avg, band, tmin, tmax, csv_path='tfr_band_power.csv'):
    """
    Compute mean power in a given freq band & time window, then write to CSV.

    Parameters
    ----------
    power_avg : mne.time_frequency.EpochsTFR
    band : tuple of (low_freq, high_freq)
    tmin, tmax : float
        Time window (s) of interest.
    csv_path : str
        Output CSV file path.
    """
    data = power_avg.data        # shape (n_channels, n_freqs, n_times)
    freqs = power_avg.freqs
    times = power_avg.times

    # Create masks for frequency and time
    freq_mask = (freqs >= band[0]) & (freqs <= band[1])
    time_mask = (times >= tmin) & (times <= tmax)

    # Average across freq and time dimensions
    band_power = data[:, freq_mask][:, :, time_mask].mean(axis=(1, 2))

    # Write results to CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['channel', f'{band[0]}-{band[1]}Hz_power'])
        for ch_name, val in zip(power_avg.ch_names, band_power):
            writer.writerow([ch_name, val])
    print(f"Saved band power to {csv_path}")


if __name__ == "__main__":
    # Smoke test: load & preprocess data, compute TFR, plot, and export band power
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
    print("TFR script ran successfully.")

    # 4. Export alpha-band (8–12 Hz) power between 0.3–0.6 s
    export_band_power(power_avg, band=(8, 12), tmin=0.3, tmax=0.6)
