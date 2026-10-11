# World Population Growth Analysis Dashboard

An interactive Streamlit dashboard that explores world population by country, continent, and year.

## Features
- Sidebar filters for continent, population year, 2022 population range, and country search
- A top-countries slider
- KPI cards and five interactive charts
- All charts and KPI values update together when sidebar filters change
- View and download the filtered dataset

## Run locally
1. Install Python 3.9 or newer.
2. Open a terminal in this folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

Keep `app.py`, `requirements.txt`, and `world pop.csv` in the same folder.

## Deploy on Streamlit Community Cloud
1. Upload these project files to a GitHub repository.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
4. Click **Deploy**.
