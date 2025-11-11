"""
RSI and MACD Crossover Strategy
Combines RSI and MACD indicators to generate trading signals
"""

import pandas as pd
from indicators import (
    calculate_rsi,
    calculate_macd,
    detect_rsi_crossover,
    detect_macd_crossover,
    detect_macd_zero_cross
)


class RSIMACDStrategy:
    """
    Trading strategy combining RSI and MACD crossover signals
    """

    def __init__(self, rsi_period=14, rsi_oversold=30, rsi_overbought=70,
                 macd_fast=12, macd_slow=26, macd_signal=9):
        """
        Initialize strategy parameters

        Args:
            rsi_period: RSI calculation period
            rsi_oversold: RSI oversold threshold
            rsi_overbought: RSI overbought threshold
            macd_fast: MACD fast EMA period
            macd_slow: MACD slow EMA period
            macd_signal: MACD signal line period
        """
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal

    def analyze(self, prices):
        """
        Analyze price data and generate trading signals

        Args:
            prices: pandas Series or list of prices

        Returns:
            pandas DataFrame with indicators and signals
        """
        if isinstance(prices, list):
            prices = pd.Series(prices)

        # Calculate indicators
        rsi = calculate_rsi(prices, period=self.rsi_period)
        macd_data = calculate_macd(
            prices,
            fast_period=self.macd_fast,
            slow_period=self.macd_slow,
            signal_period=self.macd_signal
        )

        # Detect crossovers
        rsi_signals = detect_rsi_crossover(
            rsi,
            oversold=self.rsi_oversold,
            overbought=self.rsi_overbought
        )
        macd_signals = detect_macd_crossover(macd_data)
        macd_zero_signals = detect_macd_zero_cross(macd_data)

        # Create result DataFrame
        result = pd.DataFrame({
            'price': prices,
            'rsi': rsi,
            'macd': macd_data['macd'],
            'macd_signal': macd_data['signal'],
            'macd_histogram': macd_data['histogram'],
            'rsi_buy': rsi_signals['buy_signals'],
            'rsi_sell': rsi_signals['sell_signals'],
            'macd_bullish': macd_signals['bullish_cross'],
            'macd_bearish': macd_signals['bearish_cross'],
            'macd_zero_bullish': macd_zero_signals['bullish_zero_cross'],
            'macd_zero_bearish': macd_zero_signals['bearish_zero_cross']
        })

        return result

    def generate_signals(self, prices, strategy='combined'):
        """
        Generate buy/sell signals based on strategy

        Args:
            prices: pandas Series or list of prices
            strategy: 'combined', 'rsi_only', 'macd_only', or 'confirmation'
                - combined: Signal when either RSI or MACD triggers
                - rsi_only: Only RSI signals
                - macd_only: Only MACD signals
                - confirmation: Signal when both RSI and MACD agree

        Returns:
            pandas DataFrame with 'buy' and 'sell' signal columns
        """
        result = self.analyze(prices)

        if strategy == 'rsi_only':
            result['buy'] = result['rsi_buy']
            result['sell'] = result['rsi_sell']

        elif strategy == 'macd_only':
            result['buy'] = result['macd_bullish']
            result['sell'] = result['macd_bearish']

        elif strategy == 'combined':
            # Signal when either indicator triggers
            result['buy'] = result['rsi_buy'] | result['macd_bullish']
            result['sell'] = result['rsi_sell'] | result['macd_bearish']

        elif strategy == 'confirmation':
            # Signal only when both indicators agree
            result['buy'] = result['rsi_buy'] & result['macd_bullish']
            result['sell'] = result['rsi_sell'] & result['macd_bearish']

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        return result

    def get_latest_signal(self, prices, strategy='combined'):
        """
        Get the most recent trading signal

        Args:
            prices: pandas Series or list of prices
            strategy: signal generation strategy

        Returns:
            dict with latest signal information
        """
        signals = self.generate_signals(prices, strategy=strategy)
        latest = signals.iloc[-1]

        signal_type = None
        if latest['buy']:
            signal_type = 'BUY'
        elif latest['sell']:
            signal_type = 'SELL'
        else:
            signal_type = 'HOLD'

        return {
            'signal': signal_type,
            'price': latest['price'],
            'rsi': latest['rsi'],
            'macd': latest['macd'],
            'macd_signal': latest['macd_signal'],
            'macd_histogram': latest['macd_histogram']
        }

    def backtest(self, prices, initial_capital=10000, strategy='combined'):
        """
        Simple backtest of the strategy

        Args:
            prices: pandas Series or list of prices
            initial_capital: starting capital
            strategy: signal generation strategy

        Returns:
            dict with backtest results
        """
        signals = self.generate_signals(prices, strategy=strategy)

        capital = initial_capital
        position = 0  # Number of units held
        trades = []

        for i in range(len(signals)):
            if signals['buy'].iloc[i] and position == 0:
                # Buy signal - enter position
                position = capital / signals['price'].iloc[i]
                trades.append({
                    'index': i,
                    'type': 'BUY',
                    'price': signals['price'].iloc[i],
                    'capital': capital
                })

            elif signals['sell'].iloc[i] and position > 0:
                # Sell signal - exit position
                capital = position * signals['price'].iloc[i]
                trades.append({
                    'index': i,
                    'type': 'SELL',
                    'price': signals['price'].iloc[i],
                    'capital': capital
                })
                position = 0

        # Close any open position
        if position > 0:
            capital = position * signals['price'].iloc[-1]

        return {
            'initial_capital': initial_capital,
            'final_capital': capital,
            'return_pct': ((capital - initial_capital) / initial_capital) * 100,
            'num_trades': len(trades),
            'trades': trades
        }
