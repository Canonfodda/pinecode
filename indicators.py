"""
Technical Indicators: RSI and MACD
Provides calculation functions for Relative Strength Index and Moving Average Convergence Divergence
"""

import pandas as pd
import numpy as np


def calculate_rsi(data, period=14):
    """
    Calculate Relative Strength Index (RSI)

    Args:
        data: pandas Series or list of prices
        period: lookback period (default: 14)

    Returns:
        pandas Series with RSI values
    """
    if isinstance(data, list):
        data = pd.Series(data)

    # Calculate price changes
    delta = data.diff()

    # Separate gains and losses
    gains = delta.copy()
    losses = delta.copy()
    gains[gains < 0] = 0
    losses[losses > 0] = 0
    losses = abs(losses)

    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period, min_periods=period).mean()
    avg_losses = losses.rolling(window=period, min_periods=period).mean()

    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate MACD (Moving Average Convergence Divergence)

    Args:
        data: pandas Series or list of prices
        fast_period: fast EMA period (default: 12)
        slow_period: slow EMA period (default: 26)
        signal_period: signal line EMA period (default: 9)

    Returns:
        dict with 'macd', 'signal', and 'histogram' as pandas Series
    """
    if isinstance(data, list):
        data = pd.Series(data)

    # Calculate EMAs
    ema_fast = data.ewm(span=fast_period, adjust=False).mean()
    ema_slow = data.ewm(span=slow_period, adjust=False).mean()

    # Calculate MACD line
    macd_line = ema_fast - ema_slow

    # Calculate signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # Calculate histogram
    histogram = macd_line - signal_line

    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def detect_rsi_crossover(rsi, oversold=30, overbought=70):
    """
    Detect RSI crossover signals

    Args:
        rsi: pandas Series with RSI values
        oversold: oversold threshold (default: 30)
        overbought: overbought threshold (default: 70)

    Returns:
        dict with 'buy_signals' and 'sell_signals' as boolean Series
    """
    buy_signals = (rsi.shift(1) < oversold) & (rsi >= oversold)
    sell_signals = (rsi.shift(1) > overbought) & (rsi <= overbought)

    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }


def detect_macd_crossover(macd_data):
    """
    Detect MACD line and signal line crossovers

    Args:
        macd_data: dict with 'macd' and 'signal' Series from calculate_macd()

    Returns:
        dict with 'bullish_cross' and 'bearish_cross' as boolean Series
    """
    macd = macd_data['macd']
    signal = macd_data['signal']

    # Bullish crossover: MACD crosses above signal line
    bullish_cross = (macd.shift(1) <= signal.shift(1)) & (macd > signal)

    # Bearish crossover: MACD crosses below signal line
    bearish_cross = (macd.shift(1) >= signal.shift(1)) & (macd < signal)

    return {
        'bullish_cross': bullish_cross,
        'bearish_cross': bearish_cross
    }


def detect_macd_zero_cross(macd_data):
    """
    Detect MACD zero line crossovers

    Args:
        macd_data: dict with 'macd' Series from calculate_macd()

    Returns:
        dict with 'bullish_zero_cross' and 'bearish_zero_cross' as boolean Series
    """
    macd = macd_data['macd']

    # Bullish zero crossover: MACD crosses above zero
    bullish_zero_cross = (macd.shift(1) <= 0) & (macd > 0)

    # Bearish zero crossover: MACD crosses below zero
    bearish_zero_cross = (macd.shift(1) >= 0) & (macd < 0)

    return {
        'bullish_zero_cross': bullish_zero_cross,
        'bearish_zero_cross': bearish_zero_cross
    }
