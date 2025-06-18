# scripts/load_and_plot.py

import mne

def load_and_plot(raw_path=None):
    """
    Load raw EEG/MEG data (default MNE sample) and plot the first 5 EEG channels.
    Returns the Raw object and the list of EEG channel indices.
    """
    # 1. Determine file path
    if raw_path is None:
        # download (if needed) and get sample data folder
        sample_folder = mne.datasets.sample.data_path()
        raw_path = f"{sample_folder}/MEG/sample/sample_audvis_raw.fif"

    # 2. Load the raw file
    raw = mne.io.read_raw_fif(raw_path, preload=True)

    # 3. Pick the first 5 EEG channels
    eeg_picks = mne.pick_types(raw.info, meg=False, eeg=True)[:5]

    # 4. Plot 10 seconds of data for those channels
    raw.plot(n_channels=5, picks=eeg_picks, duration=10, start=0.0)

    return raw, eeg_picks

if __name__ == "__main__":
    raw, picks = load_and_plot()
    print("Loaded raw data and plotted first 5 EEG channels.")
