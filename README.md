# Neuro-Pipeline

An end-to-end EEG data processing toolkit built with Python and MNE, designed for single-trial event‐related potential (ERP) and time–frequency analyses, with automated exports for downstream analysis.

## Highlights

* **Raw Data Visualization**
  Quickly plot continuous EEG recordings to inspect data quality.
* **Signal Preprocessing**
  Apply band‑pass filtering and automatic epoch rejection to clean raw signals.
* **ERP Extraction**
  Segment data around events, compute averaged responses, detect peak amplitudes, and export results.
* **Time–Frequency Decomposition**
  Perform wavelet‐based analyses to quantify power in user‑defined frequency bands and export per‑channel metrics.
* **Modular Scripts**
  Run each stage as a standalone command‐line script for reproducibility and easy integration into larger workflows.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/eozturk1968/neuro-pipeline.git
cd neuro-pipeline
```

### 2. Set Up a Virtual Environment

> **Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

> **macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage Guide

All scripts assume an activated virtual environment and a terminal launched from the project root.

### A. Plot Raw EEG

```bash
python -m scripts.load_and_plot \
  --raw-file path/to/sample_raw.fif \
  --output plots/raw_overview.png
```

### B. Preprocess Data

```bash
python -m scripts.preprocess \
  --raw-file path/to/sample_raw.fif \
  --l-freq 1.0 --h-freq 40.0 \
  --reject-thresh 100e-6 \
  --output preprocessed/sample_filtered.fif
```

### C. ERP Analysis

```bash
python -m scripts.erp \
  --raw-file preprocessed/sample_filtered.fif \
  --event-id 1 --tmin -0.2 --tmax 0.8 \
  --reject-thresh 100e-6
```

*Generates `erp_peaks.csv` containing peak amplitudes and latencies.*

### D. Time–Frequency Analysis

```bash
python -m scripts.tfr \
  --raw-file preprocessed/sample_filtered.fif \
  --freq-min 8 --freq-max 12 --n-cycles 7 \
  --tmin -0.2 --tmax 0.8
```

*Exports `tfr_band_power.csv` with band‑specific power for each channel.*

## Results Notebook

1. Launch JupyterLab:

   ```bash
   jupyter lab
   ```
2. Open `01_results.ipynb` to view bar charts, summary statistics, and visual reports.

## License

This project is released under the MIT License — see [LICENSE](LICENSE) for details.
