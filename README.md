# Interest Rate Risk Dashboard

## 📊 Project Overview

An interactive quantitative finance application built to construct yield curves, model fixed-income term structures, and evaluate interest rate risk profiles. The platform dynamically ingests live U.S. Treasury data from Federal Reserve Economic Data (FRED), implements a local file-based caching layer to optimize API rate limits, and provides interactive analytics for stress-testing assets and portfolios against shifting yield curves.

---

## 📸 Screenshots & Scenario Analysis

### 📈 Premium Bond Scenario Analysis
Evaluating pricing variations and portfolio sensitivity under a baseline state versus an expansionary monetary policy environment (rate cut).

| Base Case (Premium Bond) | 50 bps Rate Cut (Premium Bond) |
| :---: | :---: |
| ![Base Case Premium Bond](screenshots/base_case(premiumbond).png) | ![50bps Cut Premium Bond](screenshots/cut_scenario_50bps(premiumbond).png) |

### 📉 Discount Bond Scenario Analysis
Evaluating risk metrics and terminal valuations under a baseline state versus a contractionary monetary policy environment (rate hike).

| Base Case (Discount Bond) | 50 bps Rate Hike (Discount Bond) |
| :---: | :---: |
| ![Base Case Discount Bond](screenshots/base_case(discountbond).png) | ![50bps Hike Discount Bond](screenshots/hike_scenario_50bps(discountbond).png) |

---

## 📁 Repository Structure

```text
├── screenshots/             # Visual outputs of dashboard scenario stress-testing
├── src/
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── curve.py             # Yield curve construction and bootstrapping logic
│   ├── dashboard.py         # Main Streamlit user interface and layout execution
│   ├── data.py              # FRED API ingestion and local cache management
│   ├── main.py              # Application entry point and orchestrator
│   ├── pricing.py           # Fixed-income asset valuation models
│   ├── risk.py              # Risk sensitivity engine (DV01, Convexity calculations)
│   └── test.py              # Unit tests and quantitative validation scripts
│
├── venv/                    # Isolated local virtual environment
├── .gitignore               # Explicit rules for excluding untracked files and venv
├── README.md                # Project documentation and file directory map
├── requirements.txt         # Core production-pinned external dependencies
└── treasury_cache.csv       # Local daily historical market rate database
💻 Installation & Quickstart
Follow these quick terminal steps to spin up the dashboard locally:

1. Set Up and Activate Environment
Make sure you are running inside an isolated virtual environment:

On Mac / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows
```powershell
python -m venv venv
.\venv\Scripts\activate
```
Install Verified Dependencies
Install all required third-party libraries pinned in your environment config:

```bash
pip install -r requirements.txt
```
Launch the Application
Execute the Streamlit application layer directly from the root directory:

```bash
streamlit run src/dashboard.py
```