# RSI + SMMA Strategy Library

A comprehensive TradingView PineScript v6 library combining RSI (Relative Strength Index) with SMMA (Smoothed Moving Average) for advanced trend analysis and trading signals.

## 📋 Overview

This library provides a powerful combination of momentum (RSI) and trend (SMMA) indicators to identify high-probability trading opportunities. The strategy uses multiple confirmation layers including ADX strength measurement and regime detection.

## 🎯 Key Features

- **Smoothed Moving Average (SMMA)**: Implementation of the smoothed/modified moving average calculation
- **RSI Analysis**: Multiple RSI functions including threshold, zones, and value extraction
- **Combined Signals**: Integrated RSI + SMMA signals with various confirmation methods
- **Trend Scale (1-9)**: Comprehensive trend strength measurement from very strong short (1) to very strong long (9)
- **Regime Detection**: Identifies market states (strong uptrend, uptrend, ranging, downtrend, strong downtrend)
- **ADX Integration**: Trend strength confirmation using Average Directional Index
- **Multi-timeframe Support**: Analyze trends across different timeframes
- **Modular Design**: Reusable library functions for custom implementations

## 📁 Files

### Library Files
- `rsi_smma_lib.pine` - Core library with all RSI + SMMA functions

### Example Indicators
- `rsi_smma_indicator.pine` - Full-featured indicator demonstrating the strategy

### Documentation
- `RSI_SMMA_README.md` - This file

## 🚀 Quick Start

### Using the Indicator

1. Copy `rsi_smma_indicator.pine` to TradingView Pine Editor
2. Click "Add to Chart"
3. Configure settings:
   - **RSI Length**: Default 14 (standard RSI period)
   - **Fast SMMA**: Default 10 (responsive to recent price action)
   - **Slow SMMA**: Default 20 (confirms longer-term trend)
   - **ADX Length**: Default 14 (trend strength measurement)

### Using the Library

1. Publish `rsi_smma_lib.pine` as a library on TradingView
2. Import in your indicator:
```pinescript
import YourUsername/RSISMMALib/1 as rs
```
3. Use library functions:
```pinescript
// Calculate trend scale
trendScale = rs.calculateRsiSmmaTrendScale(14, 10, 20, 14, 30.0, 20.0)

// Detect regime
regime = rs.detectRsiSmmaRegime(14, 10, 20, 14, 25.0)

// Get signal strength
strength = rs.getRsiSmmaStrength(14, 10, 20)
```

## 📊 Strategy Logic

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

## ⚙️ Configuration

### RSI Settings
- **RSI Length**: Period for RSI calculation (default: 14)
  - Lower values (5-9): More responsive, more signals
  - Higher values (14-21): Smoother, fewer false signals
- **Overbought Level**: Default 70
- **Oversold Level**: Default 30

### SMMA Settings
- **Fast SMMA Length**: Default 10
  - Shorter periods: More responsive to price changes
  - Recommended range: 5-15
- **Slow SMMA Length**: Default 20
  - Longer periods: Confirms overall trend direction
  - Recommended range: 20-50

### ADX Settings
- **ADX Length**: Default 14 (standard)
- **Strong Trend Threshold**: Default 30
- **Weak Trend Threshold**: Default 20

### Display Options
- **Show Trend Scale (1-9)**: Display full 9-level scale
- **Show Regime Detection**: Display regime table
- **Show Signal Line**: Simplified -1/0/+1 signal

### Alert Settings
- **Enable Alerts**: Turn on/off all alert conditions
- Alerts trigger on:
  - Trend scale changes (1, 2, 3, 7, 8, 9)
  - Signal line crosses (buy/sell)
  - Regime changes (strong uptrend/downtrend)

## 📈 Trading Applications

### Entry Signals

**Long Entry**:
1. **Conservative**: Scale 8-9 (very strong long)
2. **Moderate**: Scale 7 (long) with confirmation
3. **Aggressive**: Scale 6 (weak long) on pullbacks

**Short Entry**:
1. **Conservative**: Scale 1-2 (very strong short)
2. **Moderate**: Scale 3 (short) with confirmation
3. **Aggressive**: Scale 4 (weak short) on bounces

### Exit Signals

**Long Exit**:
- Scale drops to 5 (neutral) or below
- Regime changes to DOWNTREND or RANGING BEARISH
- RSI reaches extreme overbought (>80)

**Short Exit**:
- Scale rises to 5 (neutral) or above
- Regime changes to UPTREND or RANGING BULLISH
- RSI reaches extreme oversold (<20)

### Filter Conditions

**Avoid Trading When**:
- Scale = 5 (neutral, no clear trend)
- ADX < 20 (weak trend, ranging market)
- Regime = "RANGING" (choppy conditions)
- Conflicting signals (RSI bullish but SMMA bearish)

### Multi-Timeframe Strategy

**Example Setup**:
1. **Higher TF** (4H/Daily): Identify overall trend
2. **Lower TF** (15m/1H): Find precise entries
3. **Rule**: Only trade in direction of higher timeframe

**Implementation**:
```pinescript
// Higher timeframe trend
htfScale = request.security(syminfo.tickerid, "240", calculateRsiSmmaTrendScale(...))

// Lower timeframe entry
ltfScale = calculateRsiSmmaTrendScale(...)

// Only long when HTF is bullish
longCondition = htfScale >= 6 and ltfScale >= 7
```

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

### Parameter Optimization

1. **RSI Length**:
   - Trending markets: 14-21 (standard to slow)
   - Ranging markets: 5-9 (fast, responsive)

2. **SMMA Lengths**:
   - Fast/Slow ratio: 1:2 is standard (e.g., 10/20, 15/30)
   - Wider spreads: Stronger confirmation but slower signals
   - Narrower spreads: Faster signals but more whipsaws

3. **ADX Thresholds**:
   - Volatile markets: Lower thresholds (20/25)
   - Calm markets: Higher thresholds (30/35)

### Risk Management

1. **Position Sizing**: Scale positions based on trend scale
   - Scale 8-9: Full position
   - Scale 6-7: Half position
   - Scale 4-5: No position

2. **Stop Loss**: Place stops based on SMMA levels
   - Long: Below slow SMMA
   - Short: Above slow SMMA

3. **Take Profit**: Use scale levels
   - Exit 50% at opposite weak signal (scale 4 for longs)
   - Exit remaining at neutral (scale 5)

### Common Pitfalls

1. **Overtrading**: Wait for scale 7+ (long) or 3- (short)
2. **Ignoring ADX**: Don't trade when ADX < 20 (ranging)
3. **Fighting the Trend**: Only trade in direction of higher timeframe
4. **FOMO**: Wait for pullbacks to strong SMMA support/resistance

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
