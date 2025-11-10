# RSI + SMMA Trading Strategy

A comprehensive TradingView PineScript v6 **backtestable strategy** combining RSI (Relative Strength Index) with SMMA (Smoothed Moving Average) for advanced trend analysis and automated trading.

## 📋 Overview

This strategy provides a powerful combination of momentum (RSI) and trend (SMMA) indicators to identify and execute high-probability trades automatically. The strategy includes complete risk management with stop loss, take profit, and uses multiple confirmation layers including ADX strength measurement.

## 🎯 Key Features

### Strategy Features
- **Automated Trading**: Backtestable strategy with automatic entry and exit orders
- **Risk Management**: Configurable stop loss (SMMA-based, Percentage, or ATR) and take profit (Risk/Reward ratio, Percentage, or Fixed)
- **Position Control**: Separate long/short enabling, customizable entry/exit signal levels
- **Performance Metrics**: Real-time P&L tracking and win rate display

### Technical Indicators
- **Smoothed Moving Average (SMMA)**: Smoothed/modified moving average for trend identification
- **RSI Analysis**: Momentum measurement with overbought/oversold detection
- **Trend Scale (1-9)**: Comprehensive trend strength from very strong short (1) to very strong long (9)
- **ADX Integration**: Trend strength confirmation using Average Directional Index

### Visualization
- **SMMA Lines**: Fast and slow SMMA plotted on chart
- **Entry/Exit Markers**: Visual indicators for trades
- **Stop Loss/Take Profit Levels**: Real-time risk levels displayed
- **Info Table**: Shows current trend scale, RSI, ADX, position, P&L, and win rate

## 📁 Files

### Strategy Files
- **`rsi_smma_strategy.pine`** - **Main backtestable strategy** (use this for trading)
- `rsi_smma_lib.pine` - Core library with reusable RSI + SMMA functions
- `rsi_smma_indicator.pine` - Indicator version (for analysis without trading)

### Documentation
- `RSI_SMMA_README.md` - This file

## 🚀 Quick Start

### Using the Strategy (Recommended)

1. **Load Strategy**: Copy `rsi_smma_strategy.pine` to TradingView Pine Editor
2. **Add to Chart**: Click "Add to Chart" - strategy will appear as overlay
3. **Open Strategy Tester**: Click the "Strategy Tester" tab at bottom of screen to see performance metrics
4. **Configure Settings**:

#### Essential Settings
- **Entry Signal Level (Long)**: Default 7 (Scale 7-9 for long entries)
  - 7 = Long, 8 = Strong Long, 9 = Very Strong Long
- **Entry Signal Level (Short)**: Default 3 (Scale 1-3 for short entries)
  - 3 = Short, 2 = Strong Short, 1 = Very Strong Short
- **Exit Signal Level**: Default 5 (Neutral - exits both directions)

#### Risk Management
- **Stop Loss Type**: Choose SMMA (default), Percentage, or ATR
  - **SMMA**: Uses slow SMMA as dynamic support/resistance
  - **Percentage**: Fixed percentage from entry (e.g., 2%)
  - **ATR**: Multiple of Average True Range (e.g., 2x ATR)
- **Take Profit Type**: Choose Risk Ratio (default), Percentage, or Fixed
  - **Risk Ratio**: Multiple of stop distance (e.g., 2:1 risk/reward)

#### Trading Controls
- **Enable Long Trades**: Toggle long positions on/off
- **Enable Short Trades**: Toggle short positions on/off

### Backtesting the Strategy

1. **Time Period**: Use TradingView's date range selector to test specific periods
2. **Initial Capital**: Set in strategy settings (default $10,000)
3. **Performance Metrics**: View in Strategy Tester tab:
   - Net Profit, Profit Factor, Max Drawdown
   - Win Rate, Total Trades, Average Trade
   - Sharpe Ratio, etc.
4. **Optimize**: Adjust entry/exit levels and risk parameters based on results

## 📊 Strategy Logic

### How the Strategy Works

#### Entry Logic
**Long Entries:**
- Trigger: Trend scale crosses above the Entry Signal Level (default 7)
- Confirmation: RSI > 50, Fast SMMA > Slow SMMA, ADX confirms trend strength
- Execution: `strategy.entry("Long", strategy.long)`

**Short Entries:**
- Trigger: Trend scale crosses below the Short Entry Level (default 3)
- Confirmation: RSI < 50, Fast SMMA < Slow SMMA, ADX confirms trend strength
- Execution: `strategy.entry("Short", strategy.short)`

#### Exit Logic
**Signal-Based Exits:**
- Long Exit: When trend scale drops to Exit Signal Level (default 5) or below
- Short Exit: When trend scale rises to (10 - Exit Signal Level) or above

**Risk-Based Exits (via strategy.exit):**
- Stop Loss: Triggered if price hits calculated stop level
- Take Profit: Triggered if price hits calculated profit target

#### Risk Management Calculation

**Stop Loss Options:**
1. **SMMA-Based** (Recommended):
   - Long: Stop at Slow SMMA (dynamic support)
   - Short: Stop at Slow SMMA (dynamic resistance)
   - Adapts to market volatility automatically

2. **Percentage-Based**:
   - Long: Entry price × (1 - Stop Loss %)
   - Short: Entry price × (1 + Stop Loss %)

3. **ATR-Based** (Volatility-adjusted):
   - Long: Entry price - (ATR × Multiplier)
   - Short: Entry price + (ATR × Multiplier)

**Take Profit Options:**
1. **Risk/Reward Ratio** (Recommended):
   - Profit Target = Entry + (Stop Distance × Risk/Reward Ratio)
   - Example: 2:1 ratio means profit target is 2× the stop distance

2. **Percentage-Based**:
   - Long: Entry price × (1 + Take Profit %)
   - Short: Entry price × (1 - Take Profit %)

### Indicator Calculations

### SMMA Calculation

The Smoothed Moving Average (SMMA) is calculated as:

```
SMMA(i) = (SMMA(i-1) * (Period - 1) + Close(i)) / Period
```

For the first value: `SMMA = SMA(close, period)`

**Characteristics**:
- Smoother than SMA, less lag than EMA
- Reduces noise while maintaining responsiveness
- Also known as Modified Moving Average (MMA) or Running Moving Average (RMA)

### RSI Analysis

**Standard RSI Calculation**:
- Period: 14 (configurable)
- Overbought: 70
- Oversold: 30
- Neutral: 50

**RSI Zones**:
- `>= 70`: Overbought (potential reversal)
- `50-70`: Bullish momentum
- `30-50`: Bearish momentum
- `<= 30`: Oversold (potential reversal)

### Combined RSI + SMMA Signals

The strategy uses multiple confirmation layers:

#### 1. Basic Alignment
- **Bullish**: RSI > 50 AND Fast SMMA > Slow SMMA
- **Bearish**: RSI < 50 AND Fast SMMA < Slow SMMA
- **Neutral**: Mixed signals

#### 2. Strength Levels (-3 to +3)

**Bullish Strength**:
- `+3`: RSI >= 70, Price > Fast SMMA > Slow SMMA (Very Strong)
- `+2`: RSI > 50, Price > Fast SMMA, Fast > Slow SMMA (Strong)
- `+1`: RSI > 50, Price > Fast SMMA (Moderate)

**Bearish Strength**:
- `-3`: RSI <= 30, Price < Fast SMMA < Slow SMMA (Very Strong)
- `-2`: RSI < 50, Price < Fast SMMA, Fast < Slow SMMA (Strong)
- `-1`: RSI < 50, Price < Fast SMMA (Moderate)

#### 3. ADX Integration (Trend Scale 1-9)

The strategy combines RSI + SMMA strength with ADX to create a 1-9 scale:

**Scale Interpretation**:
- **9**: Very Strong Long (Strength +3, ADX >= 30)
- **8**: Strong Long (Strength +3, ADX >= 20 OR Strength +2, ADX >= 30)
- **7**: Long (Strength +2/+3 with moderate ADX OR Strength +1, ADX >= 30)
- **6**: Weak Long (Strength +1, ADX < 30)
- **5**: Neutral (Strength 0)
- **4**: Weak Short (Strength -1, ADX < 30)
- **3**: Short (Strength -1/2 with moderate ADX OR Strength -1, ADX >= 30)
- **2**: Strong Short (Strength -3, ADX >= 20 OR Strength -2, ADX >= 30)
- **1**: Very Strong Short (Strength -3, ADX >= 30)

**ADX Thresholds**:
- `>= 30`: Strong trend
- `>= 20`: Weak trend
- `< 20`: No clear trend (ranging)

### Regime Detection

The strategy identifies 6 market regimes:

1. **STRONG UPTREND**: ADX >= 25, Fast SMMA > Slow SMMA, RSI > 50
2. **UPTREND**: ADX >= 25, Fast SMMA > Slow SMMA
3. **RANGING BULLISH**: ADX < 25, Fast SMMA > Slow SMMA, RSI > 50
4. **RANGING BEARISH**: ADX < 25, Fast SMMA < Slow SMMA, RSI < 50
5. **DOWNTREND**: ADX >= 25, Fast SMMA < Slow SMMA
6. **STRONG DOWNTREND**: ADX >= 25, Fast SMMA < Slow SMMA, RSI < 50

## 🎨 Visual Elements

### Trend Scale Display
- **Circles**: Size and color-coded from red (bearish) to green (bullish)
- **Scale 9**: Bright green, largest circles
- **Scale 5**: Yellow, medium circles (neutral)
- **Scale 1**: Bright red, largest circles

### Signal Line
- **Simplified view**: +1 (bullish), 0 (neutral), -1 (bearish)
- **Line plot**: Easy to spot trend changes

### Regime Table
- **Top-right corner**: Real-time regime information
- **Displays**: Current regime, scale, RSI value, ADX value
- **Color-coded**: Green (bullish), Red (bearish), Yellow (neutral)

### Background Colors
- **Light green**: Strong uptrend regime
- **Light red**: Strong downtrend regime

## ⚙️ Strategy Configuration

### Strategy Settings (Most Important)
- **Entry Signal Level (Long)**: Default 7 (range 6-9)
  - Conservative (8-9): Fewer but stronger signals
  - Moderate (7): Balanced approach
  - Aggressive (6): More signals, earlier entries

- **Entry Signal Level (Short)**: Default 3 (range 1-4)
  - Conservative (1-2): Fewer but stronger signals
  - Moderate (3): Balanced approach
  - Aggressive (4): More signals, earlier entries

- **Exit Signal Level**: Default 5 (range 1-5)
  - Lower values (3-4): Hold positions longer
  - Neutral (5): Exit at trend reversal
  - Higher values (6+): Quick exits

- **Enable Long Trades**: Default true
- **Enable Short Trades**: Default true (disable for long-only strategies)

### Risk Management Settings
**Stop Loss:**
- **Type**: SMMA (recommended), Percentage, or ATR
- **Stop Loss %**: 2% (if using Percentage type)
- **ATR Multiplier**: 2.0 (if using ATR type)
- **ATR Length**: 14

**Take Profit:**
- **Type**: Risk Ratio (recommended), Percentage, or Fixed
- **Risk/Reward Ratio**: 2.0 (2:1 reward/risk)
- **Take Profit %**: 4% (if using Percentage type)

### Indicator Settings
**RSI:**
- **Length**: 14 (standard)
  - Lower (5-9): More responsive, more signals
  - Higher (14-21): Smoother, fewer false signals

**SMMA:**
- **Fast Length**: 10 (responsive)
  - Range: 5-15
- **Slow Length**: 20 (trend confirmation)
  - Range: 20-50

**ADX:**
- **Length**: 14 (standard)
- **Strong Threshold**: 30
- **Weak Threshold**: 20

### Display Settings
- **Show SMMA Lines on Chart**: Shows Fast/Slow SMMA
- **Show Entry/Exit Markers**: Triangle markers for trades
- **Show Info Table**: Real-time stats (Scale, RSI, ADX, Position, P&L, Win Rate)

## 📈 Strategy Usage Guide

### Recommended Configurations by Trading Style

#### Conservative (Lower Frequency, Higher Accuracy)
```
Entry Signal Level (Long): 8
Entry Signal Level (Short): 2
Exit Signal Level: 5
Stop Loss Type: SMMA
Take Profit Type: Risk Ratio (2.0)
```
- Fewer trades, stronger confirmations
- Best for: Swing trading, larger timeframes (4H, Daily)

#### Balanced (Default Settings)
```
Entry Signal Level (Long): 7
Entry Signal Level (Short): 3
Exit Signal Level: 5
Stop Loss Type: SMMA
Take Profit Type: Risk Ratio (2.0)
```
- Moderate trade frequency with good accuracy
- Best for: Most traders, 1H-4H timeframes

#### Aggressive (Higher Frequency, More Trades)
```
Entry Signal Level (Long): 6
Entry Signal Level (Short): 4
Exit Signal Level: 4
Stop Loss Type: ATR (Multiplier: 1.5)
Take Profit Type: Risk Ratio (1.5)
```
- More trading opportunities, accept some false signals
- Best for: Day trading, smaller timeframes (15m-1H)

### Timeframe Recommendations

**Scalping (5m-15m):**
- Fast SMMA: 5-8
- Slow SMMA: 10-15
- RSI: 5-9
- Entry Level (Long): 6-7
- Higher frequency, tighter stops

**Day Trading (15m-1H):**
- Fast SMMA: 8-10
- Slow SMMA: 15-20
- RSI: 9-14
- Entry Level (Long): 7
- Balanced settings (use defaults)

**Swing Trading (4H-Daily):**
- Fast SMMA: 10-15
- Slow SMMA: 20-30
- RSI: 14-21
- Entry Level (Long): 7-8
- Lower frequency, higher conviction trades

**Position Trading (Daily-Weekly):**
- Fast SMMA: 15-20
- Slow SMMA: 30-50
- RSI: 14-21
- Entry Level (Long): 8-9
- Very selective, strong trends only

### Market-Specific Settings

**Crypto (High Volatility):**
- Use ATR-based stops (Multiplier: 2.5-3.0)
- Shorter SMMA periods (Fast: 8, Slow: 16)
- Entry Level: 7 (need confirmation but can't wait too long)

**Forex:**
- SMMA-based stops work well (respects technical levels)
- Standard periods (Fast: 10, Slow: 20)
- Consider session times in backtest

**Stocks:**
- Percentage-based stops common (2-3%)
- Standard settings work well
- Adjust for gap risk (don't trade on open)

### What to Monitor

The strategy automatically displays:
1. **Current Trend Scale**: Shows market strength (1-9)
2. **Position**: LONG, SHORT, or NONE
3. **P&L**: Net profit/loss from all trades
4. **Win Rate**: Percentage of winning trades

**In Strategy Tester Tab:**
- **Net Profit**: Total profit minus total loss
- **Profit Factor**: Gross profit / Gross loss (>1.5 is good)
- **Max Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns (>1.0 is good)
- **Win Rate**: Target 45-55% (with good risk/reward)

## 🔧 Library Functions Reference

### SMMA Functions

#### `calcSmma(float src, int length)`
Calculates Smoothed Moving Average.
- **Parameters**: src (source price), length (period)
- **Returns**: SMMA value

#### `calcSmmaCross(float src, int fastLength, int slowLength)`
Dual SMMA crossover signal.
- **Returns**: true if fast > slow (bullish)

### RSI Functions

#### `calcRsi(int length, float threshold = 50.0)`
RSI threshold signal.
- **Returns**: true if RSI > threshold

#### `getRsiValue(int length)`
Raw RSI value.
- **Returns**: RSI value (0-100)

#### `calcRsiZones(int length, float overbought = 70.0, float oversold = 30.0)`
RSI zone detection.
- **Returns**: 1 (overbought), -1 (oversold), 0 (neutral)

### Combined Functions

#### `getRsiSmmaSignal(int rsiLength, int fastSmmaLength, int slowSmmaLength)`
Basic alignment signal.
- **Returns**: 1 (bullish), -1 (bearish), 0 (neutral)

#### `getRsiSmmaConfirmation(int rsiLength, int smmaLength, float rsiThreshold = 50.0)`
Price above SMMA + RSI confirmation.
- **Returns**: true for confirmed bullish

#### `getRsiSmmaStrength(int rsiLength, int fastSmmaLength, int slowSmmaLength)`
Momentum strength measurement.
- **Returns**: -3 to +3 (strength level)

#### `calculateRsiSmmaTrendScale(int rsiLength, int fastSmmaLength, int slowSmmaLength, int adxLength, float adxStrongThreshold = 30.0, float adxWeakThreshold = 20.0)`
Comprehensive trend scale with ADX.
- **Returns**: 1-9 scale

#### `detectRsiSmmaRegime(int rsiLength, int fastSmmaLength, int slowSmmaLength, int adxLength, float adxThreshold = 25.0)`
Market regime detection.
- **Returns**: String (regime name)

### Utility Functions

#### `getPriceSmmaDistance(int smmaLength)`
Distance between price and SMMA.
- **Returns**: Percentage distance

#### `detectRsiSmmaCross(int rsiLength, int fastSmmaLength, int slowSmmaLength)`
Entry signal detection.
- **Returns**: 1 (bullish cross), -1 (bearish cross), 0 (no cross)

## 💡 Best Practices

### Strategy Optimization Process

1. **Start with Defaults**: Run backtest with default settings first
2. **Analyze Results**: Look at Strategy Tester metrics
3. **Identify Issues**:
   - Low win rate? → Increase entry levels (7→8, 3→2)
   - Too few trades? → Decrease entry levels (7→6, 3→4)
   - Large drawdowns? → Tighten stops or reduce position size
   - Small winners? → Increase take profit ratio
4. **Optimize One Parameter at a Time**: Don't change everything at once
5. **Test on Different Periods**: Ensure strategy works in different market conditions

### Risk Management Rules

1. **Never Risk More Than 2% Per Trade**:
   - Strategy uses 100% equity by default
   - In live trading, adjust position size based on stop distance
   - Position Size = (Account × 2%) / Stop Distance

2. **Use Appropriate Stop Loss Type**:
   - **Trending markets**: SMMA-based (adapts to trend)
   - **Range-bound**: Percentage or ATR (fixed risk)
   - **High volatility**: ATR with larger multiplier (2.5-3.0)

3. **Set Realistic Take Profit Targets**:
   - Risk/Reward Ratio of 2:1 is standard
   - Aggressive: 1.5:1 (higher win rate needed)
   - Conservative: 3:1 (lower win rate acceptable)

4. **Monitor Drawdowns**:
   - If drawdown > 20%: Stop trading and review settings
   - If drawdown > 10%: Reduce position size

### Common Pitfalls to Avoid

1. **Over-optimization (Curve Fitting)**:
   - Don't optimize every parameter perfectly for past data
   - Test on out-of-sample period (different time range)
   - If performance drops significantly, you over-fit

2. **Ignoring Market Conditions**:
   - Strategy works best in trending markets
   - Reduce position size in ranging markets (low ADX)
   - Consider disabling during major news events

3. **Wrong Timeframe**:
   - Don't scalp on daily charts
   - Don't swing trade on 1-minute charts
   - Match strategy settings to your timeframe (see Timeframe Recommendations)

4. **Ignoring Commission and Slippage**:
   - Strategy includes 0.1% commission and 2 ticks slippage
   - Adjust these in strategy settings for your broker
   - High-frequency trading needs lower entry/exit levels to overcome costs

5. **Revenge Trading After Losses**:
   - Strategy may have losing streaks (normal)
   - Don't manually override with more aggressive settings
   - Trust the system if backtest shows profitability

### Forward Testing Before Live Trading

1. **Paper Trading**: Use TradingView's paper trading feature
2. **Small Size**: Start with minimal position size
3. **Track Real Performance**: Compare to backtest results
4. **Adjust for Reality**: Account for emotions, execution delays
5. **Only Go Live**: When paper trading matches backtest expectations

## 📊 Performance Considerations

### Advantages
- Combines momentum (RSI) with trend (SMMA) for robust signals
- Multiple confirmation layers reduce false signals
- Adapts to trend strength via ADX integration
- Clear visual representation of market state
- Works across all timeframes and instruments

### Limitations
- Lagging indicator (like all moving averages)
- May give late signals in fast-moving markets
- Requires optimization for different instruments
- Less effective in choppy, ranging markets
- Multiple indicators = more complex interpretation

### Optimization Tips
1. Backtest on your specific instrument and timeframe
2. Adjust SMMA lengths based on instrument volatility
3. Fine-tune ADX thresholds for market conditions
4. Consider adding volume confirmation
5. Use higher timeframe for trend filter

## 🔄 Version History

### v1.0 (Current)
- Initial release
- SMMA implementation
- RSI + SMMA combination functions
- Trend scale (1-9) with ADX integration
- Regime detection
- Multi-timeframe support
- Full visualization and alerts

## 📝 License

This library is provided as-is for educational and trading purposes. Use at your own risk.

## 🤝 Contributing

To improve this library:
1. Test on various instruments and timeframes
2. Suggest parameter optimizations
3. Report bugs or edge cases
4. Share successful configurations

## 📧 Support

For questions or issues:
- Check TradingView documentation for PineScript v6
- Review example indicator for implementation patterns
- Test in simulator before live trading

## ⚠️ Disclaimer

This indicator is for educational purposes only. Past performance does not guarantee future results. Always test strategies thoroughly before using with real money. Consider your risk tolerance and consult with a financial advisor.

---

**Happy Trading! 📈**
