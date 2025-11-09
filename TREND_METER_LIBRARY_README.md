# Trend Meter Library - Usage Guide

## Overview

The Trend Meter Library (`TrendMeterLib`) is a PineScript v6 library that provides multi-timeframe trend strength calculations on a 1-9 numeric scale. It combines configurable trend meters with ADX strength measurement and Heikin Ashi confirmation.

**Library File:** `trend_meter_lib.pine`
**Example Indicator:** `trend_meter_example.pine`

## Publishing the Library to TradingView

1. Open `trend_meter_lib.pine` in the TradingView Pine Editor
2. Click "Publish Script" (you must be logged in)
3. Choose "Library" as the publication type
4. Set visibility (Private, Invite-only, or Public)
5. Add description and release notes
6. Publish

**Note:** The library name in the code is `TrendMeterLib`. After publishing, it will be available as `YourUsername/TrendMeterLib/1` (version 1).

## Importing the Library

In your indicator or strategy, import the library:

```pinescript
//@version=6
indicator("My Indicator", overlay=false)

// Import the library with alias 'tm'
import YourUsername/TrendMeterLib/1 as tm
```

Replace `YourUsername` with your actual TradingView username.

## Available Functions

### Core Trend Meters

#### `calcMacd(int fastLen, int slowLen, int signalLen)`
Standard MACD crossover calculation.
- **Parameters:** Fast EMA length, Slow EMA length, Signal line length
- **Returns:** `true` if MACD > signal (bullish), `false` otherwise
- **Example:** `tm.calcMacd(12, 26, 9)`

#### `calcMomDad()`
Top Dog Trading Mom/Dad crossover.
- **Returns:** `true` if Mom > Dad (bullish), `false` otherwise
- **Example:** `tm.calcMomDad()`

#### `calcRsi(int length)`
RSI 50-level calculation.
- **Parameters:** RSI calculation length
- **Returns:** `true` if RSI > 50 (bullish), `false` otherwise
- **Example:** `tm.calcRsi(13)`

#### `calcRsiSigCross()`
RSI signal line cross using linear regression.
- **Returns:** `true` if RSI > signal line (bullish), `false` otherwise
- **Example:** `tm.calcRsiSigCross()`

#### `calcTrendCandles()`
Heikin Ashi based trend candles.
- **Returns:** `true` if trend candle is bullish, `false` otherwise
- **Example:** `tm.calcTrendCandles()`

### Utility Functions

#### `getMeterResult(string meterChoice)`
Get result from meter choice string.
- **Parameters:** Meter name string (see options below)
- **Returns:** `true` if meter is bullish, `false` otherwise
- **Example:** `tm.getMeterResult("MACD Crossover - Fast - 8, 21, 5")`

**Supported meter choices:**
- `"MACD Crossover - 12, 26, 9"`
- `"MACD Crossover - Fast - 8, 21, 5"`
- `"Mom Dad Cross (Top Dog Trading)"`
- `"RSI Signal Line Cross - RSI 13, Sig 21"`
- `"RSI 13: > or < 50"`
- `"RSI 5: > or < 50"`
- `"Trend Candles"`

#### `getLowerTimeframe(string parentTf, int divisor)`
Calculate lower timeframe string from parent timeframe.
- **Parameters:** Parent timeframe string, division factor
- **Returns:** Lower timeframe string in minutes
- **Example:** `tm.getLowerTimeframe("15", 3)` returns `"5"`

#### `calcHaTrendStrength(string haCloseTf, string haOpenTf)`
Calculate Heikin Ashi trend strength.
- **Parameters:** Timeframe for HA close, timeframe for HA open
- **Returns:** Strength value from -2 to +2
  - `+2` = Strong bullish (body > 70% of range)
  - `+1` = Weak bullish (body > 40% of range)
  - `0` = Neutral (body ≤ 40% of range)
  - `-1` = Weak bearish
  - `-2` = Strong bearish
- **Example:** `tm.calcHaTrendStrength("15", "15")`

### Main Calculation

#### `calculateTrendScale(...)`
Main function that calculates the 1-9 trend scale.

**Parameters:**
- `bool meter1Result` - Result from trend meter 1
- `bool meter2Result` - Result from trend meter 2
- `bool meter3Result` - Result from trend meter 3
- `float adxValue` - Current ADX value
- `float vsAdx` - Very Strong ADX threshold (typically 40)
- `float sAdx` - Strong ADX threshold (typically 30)
- `float wAdx` - Weak ADX threshold (typically 20)
- `int haStrength` - Heikin Ashi strength on parent timeframe (-2 to +2)
- `int haLowerStrength` - Heikin Ashi strength on lower timeframe (-2 to +2)
- `bool useHa` - Enable/disable HA confirmation
- `bool useLowerHa` - Enable/disable lower TF HA confirmation

**Returns:** Integer from 1 to 9
- **9** = Very Strong Long (all 3 meters bullish, ADX ≥ 40, HA confirms)
- **8** = Strong Long (all 3 meters bullish, ADX ≥ 30)
- **7** = Weak Long (all 3 meters bullish, ADX ≥ 20, OR 2 meters bullish with HA)
- **6** = Very Weak Long (all 3 meters bullish, ADX < 20, OR 2 meters bullish)
- **5** = No Trend (meters mixed)
- **4** = Very Weak Short (all 3 meters bearish, ADX < 20, OR 2 meters bearish)
- **3** = Weak Short (all 3 meters bearish, ADX ≥ 20, OR 2 meters bearish with HA)
- **2** = Strong Short (all 3 meters bearish, ADX ≥ 30)
- **1** = Very Strong Short (all 3 meters bearish, ADX ≥ 40, HA confirms)

## Example Usage

### Simple Example - Direct Function Calls

```pinescript
//@version=6
indicator("Simple Trend Check", overlay=true)

import YourUsername/TrendMeterLib/1 as tm

// Check individual meters
macdBullish = tm.calcMacd(8, 21, 5)
rsiBullish = tm.calcRsi(13)
momDadBullish = tm.calcMomDad()

// Display results
bgcolor(macdBullish ? color.new(color.green, 90) : color.new(color.red, 90))
```

### Complete Example - Full Trend Scale

See `trend_meter_example.pine` for a complete implementation that includes:
- Input parameters for all settings
- Multi-timeframe analysis
- Full trend scale calculation
- Dot visualization
- Alert conditions

### Multi-Timeframe Example

```pinescript
//@version=6
indicator("MTF Trend Scale", overlay=false)

import YourUsername/TrendMeterLib/1 as tm

// Settings
parentTf = input.timeframe("15", "Timeframe")
adxLen = input.int(14, "ADX Length")

// Calculate meters on selected timeframe
meter1 = request.security(syminfo.tickerid, parentTf, tm.calcMacd(8, 21, 5))
meter2 = request.security(syminfo.tickerid, parentTf, tm.calcRsi(13))
meter3 = request.security(syminfo.tickerid, parentTf, tm.calcRsi(5))

// Get ADX
[diPlus, diMinus, adx] = request.security(syminfo.tickerid, parentTf, ta.dmi(adxLen, adxLen))

// Calculate HA strength
haStrength = tm.calcHaTrendStrength(parentTf, parentTf)

// Get trend scale
trendScale = tm.calculateTrendScale(meter1, meter2, meter3, adx, 40, 30, 20, haStrength, 0, true, false)

// Plot
plot(trendScale, "Trend Scale", color=trendScale >= 6 ? color.green : trendScale <= 4 ? color.red : color.gray, linewidth=2)
hline(5, "Neutral", color=color.gray, linestyle=hline.style_dashed)
```

## Important Notes - PineScript v6 Compliance

1. **No Line Continuations:** PineScript v6 does not support line continuations. All expressions must be on a single line or properly structured with operators.

2. **Const Strings in Alerts:** The `alertcondition()` function requires `const string` for the message parameter, not `series string`. Do not use string concatenation or variables.

3. **Library Limitations:**
   - Libraries cannot have `input.*()` declarations
   - Libraries cannot have `plot()` statements
   - Libraries cannot have `alertcondition()` statements
   - Libraries cannot have script-level calculations
   - All functionality must be in exported functions

4. **Function Parameters:** All data needed by library functions must be passed as parameters. Libraries cannot access script-level variables.

5. **Multi-Timeframe Security:** When using `request.security()` with library functions, ensure the function is called within the security context, not the result passed to it.

## Workflow for Using the Library

1. **Publish the library** (one time)
   - Open `trend_meter_lib.pine` in TradingView
   - Publish as a library (private or public)
   - Note your username and library name

2. **Create your indicator**
   - Import the library: `import YourUsername/TrendMeterLib/1 as tm`
   - Define your input parameters
   - Call library functions with appropriate parameters
   - Handle plotting and alerts in your indicator

3. **Update the library** (when needed)
   - Make changes to `trend_meter_lib.pine`
   - Publish a new version
   - Update import statement in your indicators: `import YourUsername/TrendMeterLib/2 as tm`

## Support

For issues or questions:
- Review the example indicator: `trend_meter_example.pine`
- Check PineScript v6 documentation: https://www.tradingview.com/pine-script-docs/
- Verify import statement matches your published library name

## Version History

- **1.0.0** (2025-11-09) - Initial library release
  - 9 exported functions for trend calculation
  - Multi-timeframe support
  - Heikin Ashi confirmation
  - Full PineScript v6 compliance
