import pandas as pd
import numpy as np
from triangle import find_triangle_pattern
# import config as cfg
# from eodhd import APIClient

# api = APIClient(cfg.API_KEY)


def candle_hammer(df: pd.DataFrame = None) -> pd.Series:
    """* Candlestick Detected: Hammer ("Weak - Reversal - Bullish Signal - Up"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["High"] - df["Low"]) > 3 * (df["Open"] - df["Close"]))
        & (((df["Close"] - df["Low"]) / (0.001 + df["High"] - df["Low"])) > 0.6)
        & (((df["Open"] - df["Low"]) / (0.001 + df["High"] - df["Low"])) > 0.6)
    )

def candle_inverted_hammer(df: pd.DataFrame = None) -> pd.Series:
    """* Candlestick Detected: Inverted Hammer ("Weak - Continuation - Bullish Pattern - Up")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["High"] - df["Low"]) > 3 * (df["Open"] - df["Close"]))
        & ((df["High"] - df["Close"]) / (0.001 + df["High"] - df["Low"]) > 0.6)
        & ((df["High"] - df["Open"]) / (0.001 + df["High"] - df["Low"]) > 0.6)
    )


def candle_shooting_star(df: pd.DataFrame = None) -> pd.Series:
    """* Candlestick Detected: Shooting Star ("Weak - Reversal - Bearish Pattern - Down")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["Open"].shift(1) < df["Close"].shift(1)) & (df["Close"].shift(1) < df["Open"]))
        & (df["High"] - np.maximum(df["Open"], df["Close"]) >= (abs(df["Open"] - df["Close"]) * 3))
        & ((np.minimum(df["Close"], df["Open"]) - df["Low"]) <= abs(df["Open"] - df["Close"]))
    )

def candle_hanging_man(df: pd.DataFrame = None) -> pd.Series:
    """* Candlestick Detected: Hanging Man ("Weak - Reliable - Bearish Pattern - Down")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["High"] - df["Low"]) > (4 * (df["Open"] - df["Close"])))
        & (((df["Close"] - df["Low"]) / (0.001 + df["High"] - df["Low"])) >= 0.75)
        & (((df["Open"] - df["Low"]) / (0.001 + df["High"] - df["Low"])) >= 0.75)
        & (df["High"].shift(1) < df["Open"])
        & (df["High"].shift(2) < df["Open"])
    )
    
def candle_three_white_soldiers(df: pd.DataFrame = None) -> pd.Series:
    """*** Candlestick Detected: Three White Soldiers ("Strong - Reversal - Bullish Pattern - Up")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["Open"] > df["Open"].shift(1)) & (df["Open"] < df["Close"].shift(1)))
        & (df["Close"] > df["High"].shift(1))
        & (df["High"] - np.maximum(df["Open"], df["Close"]) < (abs(df["Open"] - df["Close"])))
        & ((df["Open"].shift(1) > df["Open"].shift(2)) & (df["Open"].shift(1) < df["Close"].shift(2)))
        & (df["Close"].shift(1) > df["High"].shift(2))
        & (
            df["High"].shift(1) - np.maximum(df["Open"].shift(1), df["Close"].shift(1))
            < (abs(df["Open"].shift(1) - df["Close"].shift(1)))
        )
    )
    
    
def candle_three_black_crows(df: pd.DataFrame = None) -> pd.Series:
    """* Candlestick Detected: Three Black Crows ("Strong - Reversal - Bearish Pattern - Down")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["Open"] < df["Open"].shift(1)) & (df["Open"] > df["Close"].shift(1)))
        & (df["Close"] < df["Low"].shift(1))
        & (df["Low"] - np.maximum(df["Open"], df["Close"]) < (abs(df["Open"] - df["Close"])))
        & ((df["Open"].shift(1) < df["Open"].shift(2)) & (df["Open"].shift(1) > df["Close"].shift(2)))
        & (df["Close"].shift(1) < df["Low"].shift(2))
        & (
            df["Low"].shift(1) - np.maximum(df["Open"].shift(1), df["Close"].shift(1))
            < (abs(df["Open"].shift(1) - df["Close"].shift(1)))
        )
    )
def candle_doji(df: pd.DataFrame = None) -> pd.Series:
    """! Candlestick Detected: Doji ("Indecision / Neutral")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((abs(df["Close"] - df["Open"]) / (df["High"] - df["Low"])) < 0.1)
        & ((df["High"] - np.maximum(df["Close"], df["Open"])) > (3 * abs(df["Close"] - df["Open"])))
        & ((np.minimum(df["Close"], df["Open"]) - df["Low"]) > (3 * abs(df["Close"] - df["Open"])))
    )
def candle_three_line_strike(df: pd.DataFrame = None) -> pd.Series:
    """** Candlestick Detected: Three Line Strike ("Reliable - Reversal - Bullish Pattern - Up")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["Open"].shift(1) < df["Open"].shift(2)) & (df["Open"].shift(1) > df["Close"].shift(2)))
        & (df["Close"].shift(1) < df["Low"].shift(2))
        & (
            df["Low"].shift(1) - np.maximum(df["Open"].shift(1), df["Close"].shift(1))
            < (abs(df["Open"].shift(1) - df["Close"].shift(1)))
        )
        & ((df["Open"].shift(2) < df["Open"].shift(3)) & (df["Open"].shift(2) > df["Close"].shift(3)))
        & (df["Close"].shift(2) < df["Low"].shift(3))
        & (
            df["Low"].shift(2) - np.maximum(df["Open"].shift(2), df["Close"].shift(2))
            < (abs(df["Open"].shift(2) - df["Close"].shift(2)))
        )
        & ((df["Open"] < df["Low"].shift(1)) & (df["Close"] > df["High"].shift(3)))
    )

def candle_two_black_gapping(df: pd.DataFrame = None) -> pd.Series:
    """*** Candlestick Detected: Two Black Gapping ("Reliable - Reversal - Bearish Pattern - Down")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        ((df["Open"] < df["Open"].shift(1)) & (df["Open"] > df["Close"].shift(1)))
        & (df["Close"] < df["Low"].shift(1))
        & (df["Low"] - np.maximum(df["Open"], df["Close"]) < (abs(df["Open"] - df["Close"])))
        & (df["High"].shift(1) < df["Low"].shift(2))
    )
    
def candle_morning_star(df: pd.DataFrame = None) -> pd.Series:
    """*** Candlestick Detected: Morning Star ("Strong - Reversal - Bullish Pattern - Up")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        (np.maximum(df["Open"].shift(1), df["Close"].shift(1)) < df["Close"].shift(2)) & (df["Close"].shift(2) < df["Open"].shift(2))
    ) & ((df["Close"] > df["Open"]) & (df["Open"] > np.maximum(df["Open"].shift(1), df["Close"].shift(1))))


def candle_evening_star(df: pd.DataFrame = None) -> np.ndarray:
    """*** Candlestick Detected: Evening Star ("Strong - Reversal - Bearish Pattern - Down")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        (np.minimum(df["Open"].shift(1), df["Close"].shift(1)) > df["Close"].shift(2)) & (df["Close"].shift(2) > df["Open"].shift(2))
    ) & ((df["Close"] < df["Open"]) & (df["Open"] < np.minimum(df["Open"].shift(1), df["Close"].shift(1))))


def candle_abandoned_baby(df: pd.DataFrame = None) -> pd.Series:
    """** Candlestick Detected: Abandoned Baby ("Reliable - Reversal - Bullish Pattern - Up")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (
        (df["Open"] < df["Close"])
        & (df["High"].shift(1) < df["Low"])
        & (df["Open"].shift(2) > df["Close"].shift(2))
        & (df["High"].shift(1) < df["Low"].shift(2))
    )


def candle_morning_doji_star(df: pd.DataFrame = None) -> pd.Series:
    """** Candlestick Detected: Morning Doji Star ("Reliable - Reversal - Bullish Pattern - Up")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (df["Close"].shift(2) < df["Open"].shift(2)) & (
        abs(df["Close"].shift(2) - df["Open"].shift(2)) / (df["High"].shift(2) - df["Low"].shift(2)) >= 0.7
    ) & (abs(df["Close"].shift(1) - df["Open"].shift(1)) / (df["High"].shift(1) - df["Low"].shift(1)) < 0.1) & (
        df["Close"] > df["Open"]
    ) & (
        abs(df["Close"] - df["Open"]) / (df["High"] - df["Low"]) >= 0.7
    ) & (
        df["Close"].shift(2) > df["Close"].shift(1)
    ) & (
        df["Close"].shift(2) > df["Open"].shift(1)
    ) & (
        df["Close"].shift(1) < df["Open"]
    ) & (
        df["Open"].shift(1) < df["Open"]
    ) & (
        df["Close"] > df["Close"].shift(2)
    ) & (
        (df["High"].shift(1) - np.maximum(df["Close"].shift(1), df["Open"].shift(1)))
        > (3 * abs(df["Close"].shift(1) - df["Open"].shift(1)))
    ) & (
        np.minimum(df["Close"].shift(1), df["Open"].shift(1)) - df["Low"].shift(1)
    ) > (
        3 * abs(df["Close"].shift(1) - df["Open"].shift(1))
    )


def candle_evening_doji_star(df: pd.DataFrame = None) -> pd.Series:
    """** Candlestick Detected: Evening Doji Star ("Reliable - Reversal - Bearish Pattern - Down")"""

    # Fill NaN values with 0
    df = df.fillna(0)

    return (df["Close"].shift(2) > df["Open"].shift(2)) & (
        abs(df["Close"].shift(2) - df["Open"].shift(2)) / (df["High"].shift(2) - df["Low"].shift(2)) >= 0.7
    ) & (abs(df["Close"].shift(1) - df["Open"].shift(1)) / (df["High"].shift(1) - df["Low"].shift(1)) < 0.1) & (
        df["Close"] < df["Open"]
    ) & (
        abs(df["Close"] - df["Open"]) / (df["High"] - df["Low"]) >= 0.7
    ) & (
        df["Close"].shift(2) < df["Close"].shift(1)
    ) & (
        df["Close"].shift(2) < df["Open"].shift(1)
    ) & (
        df["Close"].shift(1) > df["Open"]
    ) & (
        df["Open"].shift(1) > df["Open"]
    ) & (
        df["Close"] < df["Close"].shift(2)
    ) & (
        (df["High"].shift(1) - np.maximum(df["Close"].shift(1), df["Open"].shift(1)))
        > (3 * abs(df["Close"].shift(1) - df["Open"].shift(1)))
    ) & (
        np.minimum(df["Close"].shift(1), df["Open"].shift(1)) - df["Low"].shift(1)
    ) > (
        3 * abs(df["Close"].shift(1) - df["Open"].shift(1))
    )    
    

    
if __name__ == "__main__":
    df = pd.read_csv("HCLTECH_LAST_50_15MIN_IST.csv")

    choice = 15 # 1=hammer, 2=inverted hammer, 3=shooting star, 4=doji

    match choice:
        case 1:
            df["candle_hammer"] = candle_hammer(df)
            col = "candle_hammer"

        case 2:
            df["candle_inverted_hammer"] = candle_inverted_hammer(df)
            col = "candle_inverted_hammer"

        case 3:
            df["candle_shooting_star"] = candle_shooting_star(df)
            col = "candle_shooting_star"

        case 4:
            df["candle_hanging_man"] = candle_hanging_man(df)
            col = "candle_hanging_man"

        case 5:
            df["candle_three_white_soldiers"] = candle_three_white_soldiers(df)
            col = "candle_three_white_soldiers"
        case 6:
            df["candle_three_black_crows"]=candle_three_black_crows(df)
            col="candle_three_black_crows"
        case 7:
            df["candle_doji"]=candle_doji(df)
            col="candle_doji"
        case 8:
            df["candle_three_line_strike"]=candle_three_line_strike(df)
            col="candle_three_line_strike"
        case 9:
            df['candle_two_black_gapping']=candle_two_black_gapping(df)
            col="candle_two_black_gapping"
        case 10:
            df["candle_morning_star"]=candle_morning_star(df)
            col="candle_morning_star"
        case 11:
            df["candle_evening_star"]=candle_evening_star(df)
            col="candle_evening_star"
        case 12:
            df["candle_abandoned_baby"]=candle_abandoned_baby(df)
            col="candle_abandoned_baby"
        case  13:
            df["candle_morning_doji_star"]=candle_morning_doji_star(df)
            col="candle_morning_doji_star"
        case 14:
            df["candle_evening_doji_star"]=candle_evening_doji_star(df)
            col="candle_evening_doji_star"
        case 15:
           df = find_triangle_pattern(df)
           df["triangle_ascending"] = df["triangle_type"] == "ascending"

        case _:
            raise ValueError("Invalid choice")

