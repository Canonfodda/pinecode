# Andys Indicator - PineCode Project

## Overview
A collection of self-adjusting Pine Script v6 indicators for adaptive trading strategies. Built with a modular approach: small, testable components that graduate to production libraries.

## Philosophy
- **Minimal code**: Clean, focused implementations
- **Modular design**: Small code sets, thoroughly tested before library consolidation
- **Adaptive mechanisms**: Indicators that adjust to market conditions
- **Pure Pine Script v6**: No line continuations, no Python/JavaScript structures

## Project Structure

```
/indicators/     → Individual indicator files (.pine)
/components/     → Reusable code snippets (pre-library)
/tests/          → Test versions with debug outputs
/library/        → Final consolidated library code
/docs/           → Documentation and implementation notes
```

## Current Indicators

### 1. Adaptive Fibonacci Pullback Monitor
**File**: `indicators/adaptive_fib_pullback.pine`
**Purpose**: Detect pullbacks from swing highs and signal at specific retracement levels for position scaling

**Features**:
- Auto-detect swing highs with optional ATR-adaptive lookback
- Monitor pullback percentage in real-time
- Alert at configurable levels (25%, 33%, 50%, 61.8%)
- Visual table with current status and metrics
- Clean ~120 lines of Pine Script v6

**Use Case**: Scale out of long positions when price pulls back 33%, 50%, etc. from recent high

[Full Documentation](docs/adaptive_fib_pullback.md)

## Development Workflow
1. Build indicator in `/indicators/` directory
2. Test thoroughly on multiple timeframes and instruments
3. Extract reusable functions to `/components/`
4. Document lessons learned in `/docs/`
5. Graduate stable components to `/library/`

## Getting Started
1. Copy indicator code from `/indicators/` folder
2. Paste into TradingView Pine Editor
3. Add to chart and configure inputs
4. Set up alerts as needed

## Roadmap
- [ ] Test Adaptive Fib Pullback on multiple assets
- [ ] Add swing low detection for short positions
- [ ] Extract swing detection logic to component
- [ ] Build additional adaptive indicators
- [ ] Create first production library

## Version
Pine Script v6

## Author
Andy