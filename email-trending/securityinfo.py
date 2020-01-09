from pandas_datareader import data


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ScrapeError(Error):
    """Raised when error in scraping article"""
    pass


def get_sec_info(ticker, start_date, end_date, rounding=2, change_rounding=2):
    """
    Returns security info

    Args:
    - ticker
    - start_date
    - end_date
    - rounding -- for prices
    - change_rounding -- decimals returned for change %
    """
    df = data.DataReader(ticker, "yahoo", start_date, end_date)
    # get just the most recent prices
    df = df.tail(1)
    result = {"open": round(df["Open"].values[0], rounding),
              "close": round(df["Close"].values[0], rounding),
              "high": round(df["High"].values[0], rounding),
              "low": round(df["Low"].values[0], rounding),
              "volume": df["Volume"].values[0],
              "change": df["Close"].values[0] / df["Open"].values[0],
              "change_pc": round((df["Close"].values[0] / df["Open"].values[0] - 1) * 100, change_rounding)}
    if "open" is None:
        raise ScrapeError(f"Exception when getting {ticker} info")
    return result
