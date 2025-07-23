# Portfolio Analysis Assignment

This project processes dummy stock trade data to compute portfolio returns and values, with currency and split adjustments. It demonstrates data engineering, financial calculations, and basic UI integration.

## Features
- Load and combine multiple stock trade CSV files
- Create a master list of holdings
- Detect and adjust for stock splits
- Adjust trading cashflows for splits
- Integrate historical daily currency rates (USD, INR, SGD) by using frankfurter api
- Compute transaction prices in multiple currencies
- Fetch split-adjusted historical prices/NAVs from Yahoo Finance/AMFI
- Calculate daily portfolio value across currencies
- Compute XIRR for each holding
- Simple UI for portfolio visualization
- (Bonus) Fetch latest news for holdings via APIs

## File Structure
- `main.py`: Main script for data processing and analysis
- `final_dataset.csv`: Output dataset
- `Preprocessing.ipynb`: Notebook for data exploration and preprocessing
- `requirements.txt`: Python dependencies
- `currency_dataset/`: Contains currency rates data
- `stock_dataset/`: Contains stock trade data for 2023, 2024, 2025

## Getting Started
1. Create and activate a virtual environment:
   - On Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
4. (Optional) Explore data in `Preprocessing.ipynb`

## Future Extensions
- Add more data sources
- Enhance UI features
- Integrate real-time APIs for prices and news
