# pinecode

RSI and MACD Crossover Trading Strategy

A Python-based technical analysis library that implements RSI (Relative Strength Index) and MACD (Moving Average Convergence Divergence) indicators with crossover detection for generating trading signals.

## Features

- **RSI Calculation**: Compute Relative Strength Index with customizable periods
- **MACD Calculation**: Calculate MACD line, signal line, and histogram
- **Crossover Detection**: Identify bullish and bearish crossovers for both indicators
- **Multiple Strategies**: Choose from different signal generation strategies
- **Backtesting**: Simple backtesting functionality to evaluate strategy performance
- **Clean API**: Easy-to-use functions and classes

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from strategy import RSIMACDStrategy
import pandas as pd

# Your price data
prices = pd.Series([100, 102, 101, 105, 107, 106, ...])

# Initialize strategy
strategy = RSIMACDStrategy()

# Get latest signal
signal = strategy.get_latest_signal(prices)
print(f"Signal: {signal['signal']}")  # BUY, SELL, or HOLD

# Run backtest
results = strategy.backtest(prices, initial_capital=10000)
print(f"Return: {results['return_pct']:.2f}%")
```

## Indicators

### RSI (Relative Strength Index)

The RSI is a momentum oscillator that measures the speed and magnitude of price changes. Values range from 0 to 100.

- **Oversold**: RSI < 30 (potential buy signal)
- **Overbought**: RSI > 70 (potential sell signal)

### MACD (Moving Average Convergence Divergence)

MACD shows the relationship between two moving averages of prices.

- **MACD Line**: Fast EMA - Slow EMA
- **Signal Line**: EMA of MACD line
- **Histogram**: MACD line - Signal line

**Crossover Signals**:
- **Bullish**: MACD crosses above signal line (buy)
- **Bearish**: MACD crosses below signal line (sell)

## Usage

### Basic Indicator Calculation

```python
from indicators import calculate_rsi, calculate_macd

# Calculate RSI
rsi = calculate_rsi(prices, period=14)

# Calculate MACD
macd_data = calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9)
```

### Crossover Detection

```python
from indicators import detect_rsi_crossover, detect_macd_crossover

# Detect RSI crossovers
rsi_signals = detect_rsi_crossover(rsi, oversold=30, overbought=70)

# Detect MACD crossovers
macd_signals = detect_macd_crossover(macd_data)
```

### Strategy Implementation

```python
from strategy import RSIMACDStrategy

# Initialize with custom parameters
strategy = RSIMACDStrategy(
    rsi_period=14,
    rsi_oversold=30,
    rsi_overbought=70,
    macd_fast=12,
    macd_slow=26,
    macd_signal=9
)

# Analyze price data
analysis = strategy.analyze(prices)

# Generate signals with different strategies
signals = strategy.generate_signals(prices, strategy='combined')
```

## Strategy Types

1. **rsi_only**: Signals based only on RSI crossovers
2. **macd_only**: Signals based only on MACD crossovers
3. **combined**: Signal when either RSI or MACD triggers (more signals)
4. **confirmation**: Signal only when both indicators agree (fewer, higher confidence signals)

## Example

Run the example script to see the strategy in action:

```bash
python example.py
```

This will:
- Generate sample price data
- Calculate RSI and MACD indicators
- Display signals from different strategies
- Show the latest trading signal
- Run a backtest and display results

## API Reference

### RSIMACDStrategy Class

#### `__init__(rsi_period=14, rsi_oversold=30, rsi_overbought=70, macd_fast=12, macd_slow=26, macd_signal=9)`

Initialize the strategy with custom parameters.

#### `analyze(prices)`

Analyze price data and return DataFrame with all indicators and signals.

**Returns**: pandas DataFrame with columns:
- `price`: Original prices
- `rsi`: RSI values
- `macd`, `macd_signal`, `macd_histogram`: MACD components
- `rsi_buy`, `rsi_sell`: RSI signals
- `macd_bullish`, `macd_bearish`: MACD crossover signals
- `macd_zero_bullish`, `macd_zero_bearish`: MACD zero-line crossovers

#### `generate_signals(prices, strategy='combined')`

Generate buy/sell signals based on selected strategy.

**Parameters**:
- `prices`: Price data (pandas Series or list)
- `strategy`: One of 'rsi_only', 'macd_only', 'combined', 'confirmation'

**Returns**: DataFrame with `buy` and `sell` signal columns

#### `get_latest_signal(prices, strategy='combined')`

Get the most recent trading signal.

**Returns**: dict with:
- `signal`: 'BUY', 'SELL', or 'HOLD'
- `price`: Current price
- `rsi`: Current RSI value
- `macd`, `macd_signal`, `macd_histogram`: Current MACD values

#### `backtest(prices, initial_capital=10000, strategy='combined')`

Run a simple backtest of the strategy.

**Returns**: dict with:
- `initial_capital`: Starting capital
- `final_capital`: Ending capital
- `return_pct`: Return percentage
- `num_trades`: Number of trades executed
- `trades`: List of trade details

## Technical Details

### RSI Calculation

1. Calculate price changes (delta)
2. Separate gains and losses
3. Calculate average gains and losses over period
4. Compute RS (Relative Strength) = Average Gain / Average Loss
5. Calculate RSI = 100 - (100 / (1 + RS))

### MACD Calculation

1. Calculate fast EMA (default: 12 periods)
2. Calculate slow EMA (default: 26 periods)
3. MACD Line = Fast EMA - Slow EMA
4. Signal Line = EMA of MACD Line (default: 9 periods)
5. Histogram = MACD Line - Signal Line

## Limitations

- This is a simple implementation for educational and research purposes
- Backtest results do not account for transaction costs, slippage, or market impact
- Past performance does not guarantee future results
- Always validate strategies with real historical data and paper trading before live trading

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
