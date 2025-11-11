"""
Example usage of RSI and MACD Crossover Strategy
"""

import numpy as np
import pandas as pd
from strategy import RSIMACDStrategy


def generate_sample_data(length=200, start_price=100, volatility=0.02):
    """
    Generate sample price data for demonstration

    Args:
        length: number of data points
        start_price: starting price
        volatility: price volatility

    Returns:
        pandas Series with simulated prices
    """
    # Generate random walk with trend
    np.random.seed(42)
    returns = np.random.normal(0.0005, volatility, length)
    prices = start_price * (1 + returns).cumprod()
    return pd.Series(prices)


def main():
    """
    Demonstrate RSI and MACD strategy usage
    """
    print("=" * 60)
    print("RSI and MACD Crossover Strategy Example")
    print("=" * 60)

    # Generate sample data
    print("\nGenerating sample price data...")
    prices = generate_sample_data(length=200, start_price=100)

    # Initialize strategy
    strategy = RSIMACDStrategy(
        rsi_period=14,
        rsi_oversold=30,
        rsi_overbought=70,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9
    )

    # Analyze price data
    print("\nAnalyzing price data with RSI and MACD indicators...")
    analysis = strategy.analyze(prices)

    # Display recent data
    print("\nLast 10 data points:")
    print(analysis[['price', 'rsi', 'macd', 'macd_signal', 'macd_histogram']].tail(10).to_string())

    # Generate signals with different strategies
    print("\n" + "=" * 60)
    print("Strategy Comparison")
    print("=" * 60)

    strategies = ['rsi_only', 'macd_only', 'combined', 'confirmation']

    for strat in strategies:
        signals = strategy.generate_signals(prices, strategy=strat)
        buy_count = signals['buy'].sum()
        sell_count = signals['sell'].sum()

        print(f"\n{strat.upper().replace('_', ' ')}:")
        print(f"  Buy signals:  {buy_count}")
        print(f"  Sell signals: {sell_count}")

    # Get latest signal
    print("\n" + "=" * 60)
    print("Latest Signal (Combined Strategy)")
    print("=" * 60)
    latest = strategy.get_latest_signal(prices, strategy='combined')
    print(f"\nSignal:          {latest['signal']}")
    print(f"Current Price:   ${latest['price']:.2f}")
    print(f"RSI:             {latest['rsi']:.2f}")
    print(f"MACD:            {latest['macd']:.4f}")
    print(f"MACD Signal:     {latest['macd_signal']:.4f}")
    print(f"MACD Histogram:  {latest['macd_histogram']:.4f}")

    # Run backtest
    print("\n" + "=" * 60)
    print("Backtest Results (Combined Strategy)")
    print("=" * 60)
    backtest_result = strategy.backtest(prices, initial_capital=10000, strategy='combined')

    print(f"\nInitial Capital: ${backtest_result['initial_capital']:,.2f}")
    print(f"Final Capital:   ${backtest_result['final_capital']:,.2f}")
    print(f"Return:          {backtest_result['return_pct']:.2f}%")
    print(f"Number of Trades: {backtest_result['num_trades']}")

    if backtest_result['trades']:
        print("\nTrade History:")
        for i, trade in enumerate(backtest_result['trades'][:5], 1):  # Show first 5 trades
            print(f"  {i}. {trade['type']} at ${trade['price']:.2f} (Capital: ${trade['capital']:,.2f})")
        if len(backtest_result['trades']) > 5:
            print(f"  ... and {len(backtest_result['trades']) - 5} more trades")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
