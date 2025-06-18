import mne
import csv

def compute_evoked(epochs, condition):
    """
    Compute the evoked response for one condition.

    Parameters
    ----------
    epochs : mne.Epochs
    condition : str
        Key in epochs.event_id, e.g. 'standard' or 'deviant'.

    Returns
    -------
    evoked : mne.Evoked
    """
    return epochs[condition].average()

def export_peak_to_csv(evoked, channel_name, tmin=0.25, tmax=0.5, csv_path='erp_peaks.csv'):
    """
    Extract peak amplitude & latency for a channel and save to CSV.

    Parameters
    ----------
    evoked : mne.Evoked
    channel_name : str
    tmin, tmax : float
    csv_path : str
    """
    # Isolate that channel
    ev_chan = evoked.copy().pick_channels([channel_name])

    # Find peak (may return scalar or array)
    amp, lat = ev_chan.get_peak(tmin=tmin, tmax=tmax, mode='pos')
    # Ensure scalars
    amp = amp if not hasattr(amp, '__len__') else amp[0]
    lat = lat if not hasattr(lat, '__len__') else lat[0]

    # Write to CSV (amplitude in µV)
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['channel', 'amplitude_uV', 'latency_s'])
        writer.writerow([channel_name, amp * 1e6, lat])
    print(f"Saved peak data to {csv_path}")
