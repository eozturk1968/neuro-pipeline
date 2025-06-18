import mne

def filter_raw(raw, l_freq=1.0, h_freq=40.0):
    """
    Return a band-pass filtered copy of raw.
    """
    return raw.copy().filter(l_freq=l_freq, h_freq=h_freq)

def reject_epochs(raw, events, event_id=None, tmin=-0.2, tmax=0.8, reject_thresh=100e-6):
    """
    Create epochs around events and reject by amplitude.

    Returns an mne.Epochs object.
    """
    epochs = mne.Epochs(
        raw,
        events,
        event_id=event_id,
        tmin=tmin,
        tmax=tmax,
        preload=True,
        reject=dict(eeg=reject_thresh)
    )
    return epochs

if __name__ == "__main__":
    # Quick smoke test
    sample_folder = mne.datasets.sample.data_path()
    raw = mne.io.read_raw_fif(f"{sample_folder}/MEG/sample/sample_audvis_raw.fif", preload=True)
    events = mne.find_events(raw, stim_channel='STI 014')
    raw_filt = filter_raw(raw)
    epochs = reject_epochs(raw_filt, events)
    print(f"Filtered raw and created {len(epochs)} epochs after rejection.")
