import numpy as np
import pandas as pd 
import plotly.graph_objects as go
from scipy.stats import linregress
from tqdm import tqdm
from typing import Union



def find_pivot_point(ohlc: pd.DataFrame, current_row: int, left_count:int = 3, right_count:int =3, 
                     progress: bool = False) -> int:
    """
    Check if the current row (i.e. point) is a pivot point
    
    :params ohlc is a dataframe with Open, High, Low, Close data
    :type :pd.DataFrame
    
    :params current_row is the index number of the row 
    :type :int
    
    :params left_count is the number of candles to the left to consider
    :type :int 
    
    :params right_count is the number of candles to right to consider 
    :type :int
    
    :return (int) 
    """
 
    # Check if ohlc dataframe meets certain conditions
    # check_ohlc_names(ohlc)
    
    
    # Check if the length conditions are met
    if current_row - left_count < 0 or current_row + right_count >= len(ohlc):
        return 0
    
    pivot_Low  = 1
    pivot_High = 1

    if not progress:
        index_iter = range(current_row - left_count, current_row + right_count + 1)
    else:
        index_iter = tqdm(range(current_row - left_count, current_row + right_count + 1), desc="Finding all pivot points...")

    for idx in index_iter:
        if(ohlc.loc[current_row, "Low"] > ohlc.loc[idx, "Low"]):
            pivot_Low = 0

        if(ohlc.loc[current_row, "High"] < ohlc.loc[idx, "High"]):
            pivot_High = 0

    if pivot_Low and pivot_High:
        return 3

    elif pivot_Low:
        return 1

    elif pivot_High:
        return 2
    else:
        return 0

def find_all_pivot_points(ohlc: pd.DataFrame, left_count:int = 3, right_count:int = 3, name_pivot: Union[None, str] = None, 
                          progress: bool = False ) -> pd.DataFrame:
    """
    Find the all the pivot points for the given OHLC dataframe

    :params ohlc is a dataframe with Open, High, Low, Close data
    :type :pd.DataFrame
    
    :params left_count is the number of candles to the left to consider
    :type :int 
    
    :params right_count is the number of candles to right to consider 
    :type :int 
    
    :params progress bar to be displayed or not 
    :type :bool 
     
    :return (pd.DataFrame)
    """


    if name_pivot != None:
        ohlc.loc[:,name_pivot] = ohlc.apply(lambda row: find_pivot_point(ohlc, row.name, left_count, right_count), axis=1)
        ohlc.loc[:,f"{name_pivot}_pos"] =  ohlc.apply(lambda row: find_pivot_point_position(row), axis=1)
    else:
        # Get the pivot points 
        ohlc.loc[:,"pivot"]     = ohlc.apply(lambda row: find_pivot_point(ohlc, row.name, left_count, right_count), axis=1)
        ohlc.loc[:,'pivot_pos'] = ohlc.apply(lambda row: find_pivot_point_position(row), axis=1)


    return ohlc 


def find_pivot_point_position(row: pd.Series) -> float:
    """
    Get the Pivot Point position and assign the Low or High value.  

    :params row to assign the pivot point position value if applicable. There must be a 'pivot' value
    :type :pd.Series 
    
    :return (float)
    """
   
   
    try:
        if row['pivot']==1:
            return row['Low']-1e-3
        elif row['pivot']==2:
            return row['High']+1e-3
        else:
            return np.nan

    except Exception as e:
        print(f"Error: {e}")
        return np.nan
    

def find_triangle_pattern(ohlc: pd.DataFrame, lookback: int = 25, min_points: int = 3, rlimit: int = 0.9, 
                          slmax_limit: float = 0.00001, slmin_limit: float = 0.00001,
                          triangle_type: str = "ascending", progress: bool = False ) -> pd.DataFrame:
    """
    Find the specified triangle pattern 
    
    :params ohlc is the OHLC dataframe 
    :type :pd.DataFrame
    
    :params lookback is the number of periods to use for back candles
    :type :int 

    :params min_points is the minimum of pivot points to use to detect a flag pattern
    :type :int
    
    :params rlimit is the R-squared fit Lower limit for the pivot points
    :type :float
    
    :params slmax_limit is the limit for the slope of the pivot Highs
    :type :float
    
    :params slmin_limit is the limit for the slope of the pivot Lows
    :type :float
    
    :params triangle_type is the type of triangle pattern to detect. Options - ["ascending", "descending", "symmetrical"]
    :type :str 
    
    :params progress bar to be displayed or not
    :type :bool
    
    :return (pd.DataFrame)
    """
    
    
    ohlc["chart_type"]            = ""
    ohlc["triangle_type"]         = ""
    ohlc["triangle_slmax"]        = np.nan
    ohlc["triangle_slmin"]        = np.nan
    ohlc["triangle_intercmin"]    = np.nan
    ohlc["triangle_intercmax"]    = np.nan
    ohlc["triangle_High_idx"]     = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["triangle_Low_idx"]      = [np.array([]) for _ in range(len(ohlc)) ]
    
    
    # Find the pivot points
    ohlc = find_all_pivot_points(ohlc)   
    
    if not progress:
        candle_iter = range(lookback, len(ohlc))
    else:
        candle_iter = tqdm(range(lookback, len(ohlc)), desc="Finding triangle patterns")
    
    for candle_idx in candle_iter:
        
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candle_idx - lookback, candle_idx+1):
            if ohlc.loc[i,"pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "Low"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"High"])
                xxmax = np.append(xxmax, i)

       
        if (xxmax.size < min_points and xxmin.size < min_points) or xxmax.size==0 or xxmin.size==0:
               continue

        slmin, intercmin, rmin, _, _ = linregress(xxmin, minim)
        slmax, intercmax, rmax, _, _ = linregress(xxmax, maxim)

        if triangle_type == "symmetrical":
            if abs(rmax)>=rlimit and abs(rmin)>=rlimit and slmin>=slmin_limit and slmax<=-1*slmax_limit:
                    ohlc.loc[candle_idx, "chart_type"]            = "triangle"
                    ohlc.loc[candle_idx, "triangle_type"]         = "symmetrical"
                    ohlc.loc[candle_idx, "triangle_slmax"]        = slmax
                    ohlc.loc[candle_idx, "triangle_slmin"]        = slmin
                    ohlc.loc[candle_idx, "triangle_intercmin"]    = intercmin
                    ohlc.loc[candle_idx, "triangle_intercmax"]    = intercmax
                    ohlc.at[candle_idx,  "triangle_High_idx"]     = xxmax
                    ohlc.at[candle_idx,  "triangle_Low_idx"]      = xxmin
                    ohlc.loc[candle_idx, "triangle_point"]        = candle_idx
                    

        elif triangle_type == "ascending":
            if abs(rmax)>=rlimit and abs(rmin)>=rlimit and slmin>=slmin_limit and (slmax>=-1*slmax_limit and slmax <= slmax_limit):
                    ohlc.loc[candle_idx, "chart_type"]            = "triangle"
                    ohlc.loc[candle_idx, "triangle_type"]         = "ascending"
                    ohlc.loc[candle_idx, "triangle_slmax"]        = slmax
                    ohlc.loc[candle_idx, "triangle_slmin"]        = slmin
                    ohlc.loc[candle_idx, "triangle_intercmin"]    = intercmin
                    ohlc.loc[candle_idx, "triangle_intercmax"]    = intercmax
                    ohlc.at[candle_idx,  "triangle_High_idx"]     = xxmax
                    ohlc.at[candle_idx,  "triangle_Low_idx"]      = xxmin
                    ohlc.loc[candle_idx, "triangle_point"]        = candle_idx
                    
    
        elif triangle_type == "descending":
            if abs(rmax)>=rlimit and abs(rmin)>=rlimit and slmax<=-1*slmax_limit and (slmin>=-1*slmin_limit and slmin <= slmin_limit):
                    ohlc.loc[candle_idx, "chart_type"]            = "triangle"
                    ohlc.loc[candle_idx, "triangle_type"]         = "descending"
                    ohlc.loc[candle_idx, "triangle_slmax"]        = slmax
                    ohlc.loc[candle_idx, "triangle_slmin"]        = slmin
                    ohlc.loc[candle_idx, "triangle_intercmin"]    = intercmin
                    ohlc.loc[candle_idx, "triangle_intercmax"]    = intercmax
                    ohlc.at[candle_idx,  "triangle_High_idx"]     = xxmax
                    ohlc.at[candle_idx,  "triangle_Low_idx"]      = xxmin
                    ohlc.loc[candle_idx, "triangle_point"]        = candle_idx   
                    print(f"Found pattern at index: {candle_idx}")
    return ohlc