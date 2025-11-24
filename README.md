# Crew Sock Price Predictor

Time-based predictive pricing model demonstrating machine learning and temporal pattern analysis.

## Features

- Real-time price predictions based on day-of-week, hour, and seasonal patterns
- Interactive visualizations with 24-hour trends and weekly heatmaps
- Optimal purchase timing recommendations with savings calculations

## Tech Stack

Python, Streamlit, Plotly, Pandas, scikit-learn

## Installation
```bash
git clone https://github.com/maddierose717/SockPricePredictor.git
cd SockPricePredictor
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

## Model

Base price of $6.00 with dynamic adjustments for:
- Time-of-day patterns (peak/off-peak)
- Day-of-week demand (Monday rush, Tuesday lull)
- Seasonal variations (winter, summer clearance)
- Special events (Black Friday, back-to-school)

## Demo

[Live Demo](#) - Coming soon
