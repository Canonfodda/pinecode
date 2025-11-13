# Adaptive Fibonacci Pullback Monitor

## Overview
A Pine Script v6 indicator that monitors pullbacks from swing highs and signals when price retraces to specific percentage levels. Designed for scaling out of long positions.

## Purpose
Detect when price pulls back from a recent swing high by specific percentages (e.g., 33%, 50%, 61.8%) to help with position exit/scaling decisions.

## How It Works

### Swing High Detection
- Uses configurable lookback period (default: 20 bars)
- Optional ATR-adaptive lookback for volatility adjustment
- Tracks the highest high within the lookback period

### Pullback Calculation
- Measures current price distance from swing high
- Converts to percentage: `(SwingHigh - CurrentPrice) / SwingHigh * 100`

### Signal Levels
- **Level 1**: 25% pullback (default)
- **Level 2**: 33% pullback (default) - Primary exit signal
- **Level 3**: 50% pullback (default)
- **Level 4**: 61.8% pullback (default)

All levels are configurable via inputs.

## Visual Elements

### Chart Overlays
- **Blue Line**: Current swing high
- **Cross Markers**: Retracement level prices (green → yellow → orange → red)
- **Background Color**: Flashes when price hits a level

### Info Table (Top Right)
- Swing High price
- Current price
- Pullback percentage (color-coded)
- Active lookback period
- Current status (which level hit, if any)

## Configuration Options

### Swing Detection
- `Swing High Lookback`: Base period for finding swing high (5-200 bars)
- `Use ATR Adaptive Lookback`: Enable volatility-based adjustment
- `ATR Period`: Period for ATR calculation (default: 14)
- `ATR Lookback Multiplier`: How much ATR affects lookback (0.1-5.0)

### Retracement Levels
- `Level 1-4 (%)`: Customize each pullback level percentage

### Display Options
- `Show Swing High Line`: Toggle swing high plot
- `Show Retracement Levels`: Toggle level markers
- `Show Info Table`: Toggle statistics table

## Alerts
Four alert conditions available:
- Level 1 Hit
- Level 2 Hit
- Level 3 Hit
- Level 4 Hit

Set up in TradingView's alert menu after adding indicator to chart.

## Usage Strategy

### Position Scaling Example
- Price hits 33% pullback (Level 2) → Sell 25% of position
- Price hits 50% pullback (Level 3) → Sell another 25%
- Price hits 61.8% pullback (Level 4) → Sell another 25%

Adjust percentages and levels based on your risk management.

## Code Stats
- **Lines**: ~120
- **Version**: Pine Script v6
- **Type**: Indicator (overlay=true)
- **Style**: Minimal, no line continuations, pure Pine Script

## Next Development Steps
1. Test on various timeframes and instruments
2. Add swing low detection for short positions
3. Create reusable functions for library export
4. Add multi-timeframe swing detection
5. Implement position size calculator

## Notes
- Currently tracks long positions only (pullback from swing high)
- Works on any timeframe
- More volatile markets may benefit from ATR-adaptive lookback
- Keep lookback period reasonable for your trading timeframe
