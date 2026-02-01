# 📊 CSX Portfolio Optimization

> **Markowitz Mean-Variance Portfolio Optimization for Cambodia Securities Exchange (CSX) Equities**

[![Website](https://img.shields.io/badge/Website-Live-brightgreen?style=for-the-badge)](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://csxmarkowitzportfoliooptimzation-efpq4vg6kvbfwf6svdikkp.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

---

## 🎯 Project Overview

This project implements the **Markowitz Mean-Variance Portfolio Optimization** model applied to equities listed on the **Cambodia Securities Exchange (CSX)**. We demonstrate a complete quantitative finance workflow from data acquisition to backtesting, providing both analytical and numerical solutions for optimal portfolio construction.

### Key Objectives
- 📈 Construct **Global Minimum Variance (GMV)** portfolios
- 📉 Generate the **Efficient Frontier** for risk-return tradeoff analysis
- 🔬 Validate performance through **out-of-sample backtesting**
- 🧪 Conduct **sensitivity analysis** for robustness testing
- 🌐 Deploy interactive web application for real-time optimization

---

## 🚀 Live Demos

| Resource | Description | Link |
|----------|-------------|------|
| 🌐 **Website** | Complete project documentation with Jupyter notebook, PDFs, and navigation | [View Website →](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/) |
| 🎮 **Interactive App** | Live Streamlit application for real-time portfolio optimization | [Launch App →](https://csxmarkowitzportfoliooptimzation-efpq4vg6kvbfwf6svdikkp.streamlit.app) |
| 📓 **Source Code** | Jupyter notebook with complete implementation | [View Notebook →](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Source_Code/CSX_Portfolio_Optimization.html) |
| 📊 **Presentation** | Professional slides covering methodology and results | [View Slides →](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Presentation_Slide/) |
| 📄 **Report** | Comprehensive written documentation | [View Report →](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Project_Report/) |

---

## 📁 Project Structure

```
CSX_Markowitz_Portfolio_Optimzation/
│
├── 📓 Source_Code/
│   ├── CSX_Portfolio_Optimization.ipynb    # Main Jupyter notebook
│   └── *.xlsx                               # CSX equity price data
│
├── 🎮 Streamlit_app/
│   ├── app.py                               # Streamlit application
│   ├── utils.py                             # Helper functions
│   ├── requirements.txt                     # Python dependencies
│   └── data/                                # CSX equity data
│
├── 📊 Presenation_Slide/
│   └── CSX_Presentaion_Slide.pdf           # Project presentation
│
├── 📄 Project_Report/
│   └── CSX_Project_Report.pdf              # Comprehensive report
│
├── 🌐 Website Files/
│   ├── _quarto.yml                         # Quarto configuration
│   ├── index.qmd                           # Homepage
│   ├── styles.css                          # Custom styling
│   └── docs/                               # Generated website (GitHub Pages)
│
└── README.md                                # This file
```

---

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.8+** - Primary programming language
- **Jupyter Notebook** - Interactive development environment
- **Pandas & NumPy** - Data manipulation and numerical computing
- **SciPy** - Optimization algorithms
- **Plotly** - Interactive visualizations

### Web Technologies
- **Streamlit** - Interactive web application framework
- **Quarto** - Website generation and Jupyter notebook rendering
- **GitHub Pages** - Free static website hosting

### Deployment
- **Streamlit Community Cloud** - Free Streamlit app hosting
- **GitHub Actions** - Automated deployment pipeline

---

## 📊 Methodology

### 1. Data Acquisition & Preprocessing
- Historical price data for **9 CSX equities**
- Return calculation and outlier treatment
- Missing data handling
- Statistical validation

### 2. Portfolio Optimization

#### Global Minimum Variance (GMV)
Minimize portfolio variance subject to budget constraint:

```
min w'Σw
s.t. w'1 = 1
```

Where:
- `w` = portfolio weights
- `Σ` = covariance matrix
- `1` = vector of ones

#### Efficient Frontier
Construct the risk-return tradeoff curve by solving:

```
min w'Σw
s.t. w'μ = μ_target
     w'1 = 1
```

Where `μ` = expected returns vector

### 3. Backtesting & Validation
- **Out-of-sample testing** on unseen data
- **Benchmark comparison** with equal-weighted portfolio
- **Performance metrics**: Returns, volatility, Sharpe ratio

### 4. Sensitivity Analysis
- Impact of correlation assumptions
- Effect of volatility shocks
- Robustness to parameter changes

---

## 📈 Key Results

### GMV Portfolio Performance (Out-of-Sample)

| Strategy | Annualized Return | Volatility | 
|----------|-------------------|------------|
| **GMV (Long/Short)** | -5.48% | 4.45% |
| **GMV (Long Only)** | -5.47% | 4.45% |
| **Equal-Weighted** | Benchmark | Benchmark |

> **Note**: Results based on historical CSX data. Past performance does not guarantee future results.

---

## 🎮 Interactive Streamlit App

The Streamlit application provides **5 interactive pages**:

### 1. 📊 Dashboard
- Executive overview with key statistics
- Asset universe profile
- Risk-return scatter plot

### 2. 📈 Data Analysis
- Historical price charts
- Return distributions
- Correlation heatmap

### 3. ⚙️ Optimization
- Real-time GMV portfolio calculation
- Interactive efficient frontier
- Toggle short-selling constraints
- Adjustable risk-free rate

### 4. 🔬 Backtest
- Out-of-sample performance comparison
- Cumulative return charts
- Performance metrics table

### 5. 🧪 Sensitivities
- Correlation stress testing
- Volatility impact analysis
- Return sensitivity

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip
git
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/LENGDEVID/CSX_Markowitz_Portfolio_Optimzation.git
cd CSX_Markowitz_Portfolio_Optimzation
```

2. **Install dependencies**
```bash
pip install -r Streamlit_app/requirements.txt
```

3. **Run Jupyter Notebook**
```bash
jupyter notebook Source_Code/CSX_Portfolio_Optimization.ipynb
```

4. **Run Streamlit App (Local)**
```bash
streamlit run Streamlit_app/app.py
```

---

## 📦 Dependencies

```text
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
openpyxl>=3.1.0
scipy>=1.11.0
matplotlib>=3.7.0
jinja2>=3.1.0
```

---

## 🌐 Deployment

### Website (GitHub Pages)
The website is automatically deployed via GitHub Pages from the `/docs` folder.

**Update workflow**:
```bash
quarto render              # Regenerate website
git add docs/
git commit -m "Update website"
git push origin main       # Auto-deploys to GitHub Pages
```

### Streamlit App (Streamlit Cloud)
The app is automatically deployed via Streamlit Community Cloud.

**Update workflow**:
```bash
# Edit Streamlit_app/app.py
git add Streamlit_app/
git commit -m "Update app"
git push origin main       # Auto-deploys to Streamlit Cloud
```

---

## 📚 Documentation

- **[Jupyter Notebook](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Source_Code/CSX_Portfolio_Optimization.html)** - Complete implementation with code, visualizations, and analysis
- **[Presentation Slides](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Presentation_Slide/)** - Professional overview of methodology and results
- **[Project Report](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Project_Report/)** - Comprehensive written documentation

---

## 👨‍💻 Author

**Leng Devid**

### Supervisor
**Professor: Mr. Toem Touch**

### Academic Context
This project was developed as part of advanced coursework in **Portfolio Management and Quantitative Finance**, demonstrating the application of Modern Portfolio Theory to emerging market equities (Cambodia Securities Exchange).

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🙏 Acknowledgments

- **Modern Portfolio Theory** - Harry Markowitz (1952)
- **Cambodia Securities Exchange (CSX)** - Data source
- **Streamlit Community** - Interactive app framework
- **Quarto** - Website generation tool

---

## 📧 Contact

For questions or collaboration opportunities, please reach out via GitHub issues.

---

## 🔗 Quick Links

- 🌐 [Live Website](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/)
- 🎮 [Interactive App](https://csxmarkowitzportfoliooptimzation-efpq4vg6kvbfwf6svdikkp.streamlit.app)
- 📓 [Source Code](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Source_Code/CSX_Portfolio_Optimization.html)
- 📊 [Presentation](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Presentation_Slide/)
- 📄 [Report](https://lengdevid.github.io/CSX_Markowitz_Portfolio_Optimzation/Project_Report/)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for quantitative finance education

</div>
