# Crew Sock Price Predictor

A time-based predictive pricing model for crew socks using machine learning and temporal pattern analysis.

## Overview

This application demonstrates advanced data science techniques by forecasting sock prices based on day-of-week, hourly patterns, and seasonal demand cycles. Built as a portfolio project to showcase interactive data visualization and predictive modeling skills.

## Features

- Real-time price predictions with temporal feature engineering
- Interactive 24-hour and weekly price trend visualizations
- Heatmap analysis showing optimal purchase windows
- Special event modeling (holidays, promotional periods)
- Savings calculator with actionable recommendations

## Demo

[Live Demo](#) (Streamlit Cloud deployment coming soon)

## Installation
```bash
# Clone the repository
git clone https://github.com/maddierose717/SockPricePredictor.git
cd SockPricePredictor

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

## Usage
```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

## Technology Stack

- **Python 3.11**
- **Streamlit** - Web application framework
- **Plotly** - Interactive data visualizations
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **scikit-learn** - Machine learning utilities

## Model Architecture

The pricing model uses a feature-based approach with:

- **Temporal Features**: Day-of-week (0-6), hour (0-23), month (1-12)
- **Base Price**: $6.00 with dynamic adjustments
- **Pattern Recognition**: Peak hours, weekend shopping, seasonal trends
- **Event Multipliers**: Holiday sales, clearance periods, promotional events

Price adjustments range from -$3.50 (Black Friday) to +$2.50 (back-to-school rush).

## Project Structure
```
SockPricePredictor/
├── app.py              # Streamlit web application
├── model.py            # Price prediction logic
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## Contributing

This is a portfolio project, but suggestions and feedback are welcome! Please open an issue to discuss potential changes.

## License

MIT License - feel free to use this project for learning purposes.

## Contact

Created by [Maddie Rose](https://github.com/maddierose717)
