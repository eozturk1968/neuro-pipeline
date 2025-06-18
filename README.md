# Neuroengineering Data Pipeline

This repository implements a modular EEG/fNIRS pipeline:
- **scripts/load_and_plot.py** — Load raw data & plot first 5 EEG channels  
- **scripts/preprocess.py** — Band-pass filter + epoch rejection  
- **scripts/erp.py** — Compute ERPs & export peak amplitudes to CSV  
- **scripts/tfr.py** — Compute Morlet-wavelet TFR & plot spectrogram  

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/neuro-pipeline.git
   cd neuro-pipeline
