import pandas as pd
import numpy as np

def main(df_anon, df_original):
    df_orig = df_original.copy()
    df_anon = df_anon.copy()

    df_date_utility = pd.DataFrame({ 'DayOfTheWeek_orig': df_orig['DateTime'].dt.dayofweek, 'DayOfTheWeek_anon': df_anon['DateTime'].dt.dayofweek, 'Week_orig':df_orig['DateTime'].dt.isocalendar().week, 'Week_anon': df_anon['DateTime'].dt.isocalendar().week })
    df_date_utility['DiffDate'] = abs(df_date_utility['DayOfTheWeek_orig']-df_date_utility['DayOfTheWeek_anon'])
    #pour tout changement de semaine l'utilite doit etre 0 
    df_date_utility.loc[~(df_date_utility['Week_orig']==df_date_utility['Week_anon']),'DiffDate']=7
    df_date_utility['date_util']= 1- df_date_utility['DiffDate']/7

    score = df_date_utility["date_util"].mean().round(3)
    return score