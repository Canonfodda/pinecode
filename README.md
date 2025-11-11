# PineCode - RSI-SMA & MACD Crossover Strategy

A TradingView PineScript v6 strategy that combines RSI with SMA overlay and MACD crossover confirmation for generating precise trading signals.

## Strategy Overview

This is a **two-step confirmation strategy** that reduces false signals by requiring both RSI and MACD agreement before entering trades.

### Entry Logic

#### LONG Entry (2 Steps)
1. **Flag Step**: RSI (in 0-50 zone) crosses **above** its SMA → Flag potential long
2. **Confirmation Step**: MACD crosses **above** Signal line → Enter long

#### SHORT Entry (2 Steps)
1. **Flag Step**: RSI (in 50-100 zone) crosses **below** its SMA → Flag potential short
2. **Confirmation Step**: MACD crosses **below** Signal line → Enter short

### Exit Logic

**Exit for both Long and Short**: When RSI crosses back over its SMA (in either direction)

## Visual Explanation

```
LONG SETUP:
─────────────────────────────────────────────────────
RSI Panel (0-100):
    50 ├─────────────────────────────  [Upper Zone]
       │         RSI crosses
       │         above SMA ↑
    30 ├─────────────────────────────  [Lower Zone Flag]
       │    ●  ← Flag set here
     0 └─────────────────────────────

MACD Panel:
       │
     0 ├──────X──────────────────────  [Zero Line]
       │       ↑ MACD crosses above
       │         Signal → ENTER LONG ✓

Exit when: RSI crosses SMA again (either direction)

SHORT SETUP:
─────────────────────────────────────────────────────
RSI Panel (0-100):
   100 ├─────────────────────────────
       │         RSI crosses
       │         below SMA ↓
    50 ├─────────────────────────────  [Upper Zone Flag]
       │    ●  ← Flag set here
     0 └─────────────────────────────

MACD Panel:
       │       ↓ MACD crosses below
     0 ├──────X──────────────────────  [Zero Line]
       │         Signal → ENTER SHORT ✓

Exit when: RSI crosses SMA again (either direction)
```

## Files

### 1. `RSI_MACD_Cross_Strategy.pine`
Main strategy file with:
- Complete entry/exit logic
- Visual signals and flags
- Real-time dashboard
- Configurable parameters
- Built-in alerts

### 2. `MACD_Indicator.pine` (Optional)
Companion MACD indicator for separate panel visualization:
- MACD line and Signal line
- Histogram display
- Crossover highlights
- Sync with strategy alerts

## Installation & Usage

### TradingView Setup

1. **Open TradingView** and go to the Pine Editor
2. **Copy the strategy code** from `RSI_MACD_Cross_Strategy.pine`
3. **Paste into Pine Editor** and click "Add to Chart"
4. **Optional**: Add `MACD_Indicator.pine` in a separate panel below

### Recommended Layout

```
┌─────────────────────────────────────┐
│     Main Chart (Price)              │
│     (Strategy plots here)           │
├─────────────────────────────────────┤
│     RSI Panel                       │
│     - RSI line (blue)               │
│     - RSI SMA (orange)              │
│     - Zones highlighted             │
│     - Entry signals shown           │
├─────────────────────────────────────┤
│     MACD Panel (optional)           │
│     - MACD vs Signal                │
│     - Histogram                     │
│     - Crossover markers             │
└─────────────────────────────────────┘
```

## Configuration Parameters

### RSI Settings
| Parameter | Default | Description |
|-----------|---------|-------------|
| RSI Length | 14 | Period for RSI calculation |
| RSI SMA Length | 14 | SMA period applied to RSI |
| Lower Zone | 50 | Upper boundary of long zone (0 to this value) |
| Upper Zone | 50 | Lower boundary of short zone (this to 100) |

### MACD Settings
| Parameter | Default | Description |
|-----------|---------|-------------|
| Fast Length | 12 | Fast EMA period |
| Slow Length | 26 | Slow EMA period |
| Signal Length | 9 | Signal line period |

### Strategy Settings
| Parameter | Default | Description |
|-----------|---------|-------------|
| Initial Capital | 10,000 | Starting capital for backtest |
| Order Size | 100% | Percentage of equity per trade |
| Commission | 0.1% | Commission per trade |

## Visual Indicators

### On RSI Panel

- **Blue Line**: RSI value
- **Orange Line**: SMA of RSI
- **Green Background**: Long zone (RSI 0-50)
- **Red Background**: Short zone (RSI 50-100)
- **Green Circle ("L Flag")**: Long trade flagged
- **Red Circle ("S Flag")**: Short trade flagged
- **Green Triangle Up ("LONG")**: Long entry executed
- **Red Triangle Down ("SHORT")**: Short entry executed

### Dashboard (Top Right)

Real-time display showing:
- Current RSI value
- Current RSI SMA value
- Current MACD value
- Current Signal line value
- Current flag status (LONG FLAG / SHORT FLAG / NO FLAG)

## Alerts

The strategy includes 6 alert conditions:

1. **Long Flag**: RSI crossed above SMA in lower zone
2. **Short Flag**: RSI crossed below SMA in upper zone
3. **Long Entry**: MACD confirmed - long trade entered
4. **Short Entry**: MACD confirmed - short trade entered
5. **Exit Long**: RSI/SMA crossover - long position closed
6. **Exit Short**: RSI/SMA crossover - short position closed

### Setting Up Alerts

1. Right-click the strategy on your chart
2. Select "Add Alert"
3. Choose the desired alert condition
4. Configure notification method (popup, email, webhook, etc.)

## Strategy Logic Flow

```
┌─────────────────────────────────────────────────┐
│  Start                                          │
└────────────┬────────────────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │  Check RSI & SMA   │
    └────────┬───────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
   RSI 0-50      RSI 50-100
   RSI > SMA     RSI < SMA
      │             │
   Set LONG      Set SHORT
   FLAG          FLAG
      │             │
      └──────┬──────┘
             │
             ▼
    ┌────────────────────┐
    │  Wait for MACD     │
    │  Confirmation      │
    └────────┬───────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
   MACD >        MACD <
   Signal        Signal
      │             │
   ENTER         ENTER
   LONG          SHORT
      │             │
      └──────┬──────┘
             │
             ▼
    ┌────────────────────┐
    │  Monitor Position  │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  RSI crosses SMA?  │
    │  (either direction)│
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  EXIT POSITION     │
    │  Clear Flags       │
    └────────────────────┘
```

## Example Scenarios

### Scenario 1: Successful Long Trade

```
1. RSI = 40 (in 0-50 zone)
2. RSI crosses above RSI SMA → LONG FLAG SET ⚑
3. Wait for MACD...
4. MACD crosses above Signal → ENTER LONG ✓
5. Position held...
6. RSI crosses back below RSI SMA → EXIT LONG ✓
```

### Scenario 2: Failed Setup (No Entry)

```
1. RSI = 35 (in 0-50 zone)
2. RSI crosses above RSI SMA → LONG FLAG SET ⚑
3. Wait for MACD...
4. MACD does NOT cross Signal
5. RSI crosses back below SMA → Flag cleared, no trade taken
```

### Scenario 3: Successful Short Trade

```
1. RSI = 65 (in 50-100 zone)
2. RSI crosses below RSI SMA → SHORT FLAG SET ⚑
3. Wait for MACD...
4. MACD crosses below Signal → ENTER SHORT ✓
5. Position held...
6. RSI crosses back above RSI SMA → EXIT SHORT ✓
```

## Backtesting

The strategy includes built-in backtesting capabilities:

1. **Apply strategy to chart**
2. **Open Strategy Tester** (bottom panel)
3. **View performance metrics**:
   - Net Profit
   - Total Trades
   - Win Rate
   - Profit Factor
   - Max Drawdown
   - And more...

### Optimization Tips

- Test different RSI SMA lengths (10, 14, 20, 30)
- Adjust zone boundaries (try 40/60 instead of 50/50)
- Test on multiple timeframes
- Compare different MACD settings
- Use on different assets (stocks, crypto, forex)

## Best Practices

1. **Use on trending markets**: This strategy works best in trending conditions
2. **Combine with trend filters**: Consider adding a longer-term MA filter
3. **Respect timeframes**: Higher timeframes (4H, Daily) typically more reliable
4. **Risk management**: Use stop losses even though not built into this strategy
5. **Test thoroughly**: Backtest extensively before live trading
6. **Paper trade first**: Verify performance in real-time before risking capital

## Limitations

- **Whipsaws in ranging markets**: May generate false signals in choppy conditions
- **No built-in stop loss**: Consider adding risk management
- **No position sizing**: Currently uses fixed percentage
- **Lag from confirmations**: Two-step process may miss fast moves
- **Not suitable for scalping**: Better for swing trading

## Customization Ideas

### Add Stop Loss & Take Profit
```pinescript
// Add after entry
if strategy.position_size > 0
    strategy.exit("Exit Long", "Long", stop=stop_price, limit=take_profit_price)
```

### Add Trend Filter
```pinescript
// Only trade in direction of 200 SMA
ma200 = ta.sma(close, 200)
allow_long = close > ma200
allow_short = close < ma200
```

### Add Volume Filter
```pinescript
// Only enter if volume confirms
volume_avg = ta.sma(volume, 20)
high_volume = volume > volume_avg * 1.5
long_entry = long_flag and macd_cross_above and high_volume
```

## Version History

- **v1.0** - Initial PineScript v6 implementation
  - RSI with SMA overlay
  - Two-step confirmation logic
  - MACD crossover confirmation
  - Visual signals and dashboard
  - Complete alert system

## Support & Resources

- **PineScript Documentation**: https://www.tradingview.com/pine-script-docs/
- **TradingView Community**: https://www.tradingview.com/scripts/
- **Strategy Testing**: Use TradingView's Strategy Tester for backtesting

## Disclaimer

This strategy is for educational and informational purposes only. Past performance does not guarantee future results. Always:
- Test thoroughly before using real money
- Understand the risks of trading
- Never risk more than you can afford to lose
- Consider consulting a financial advisor
- Use proper risk management

Trading involves substantial risk of loss and is not suitable for every investor.

## License

This code is open source and provided for educational purposes.

## Contributing

Improvements and suggestions are welcome! Areas for enhancement:
- Additional filters
- Risk management features
- Position sizing algorithms
- Multi-timeframe analysis
- Automated optimization
