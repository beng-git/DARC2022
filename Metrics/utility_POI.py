#######################################
# --- Taille des points d'intérêts ---#
#######################################
# size = 2
# 4 : cellule au mètre
# 3 : cellule à la rue
# 2 : cellule au quartier
# 1 : cellule à la ville
# 0 : cellule à la région
# -1 : cellule au pays

######################################
# --- Nb de POI à vérifier par ID ---#
######################################
# nbPOI = 3
# 3: Vérification des 3 POI les plus fréquentés en terme de temps de présence.

################################
# --- Définition des heures ---#
################################
# Détection des POI -nuit, travail et weekend- durant les heures suivantes:
# night_start, night_end = 22, 6
# De 22h00 à 6h00
# work_start, work_end = 9, 16
# De 9h00 à 16h00
# weekend_start, weekend_end = 10, 18

import pandas as pd
import numpy as np

def main(df_anon, df_original):
    #Global variables
    size = 2
    values = ['NIGHT', 'NIGHT','WORK', 'WEEKEND']
    df_orig = df_original.copy()
    df_anon = df_anon.copy()

    df_orig['DateTime']= df_orig['DateTime'].astype('datetime64[ns]')
    df_orig['ID']= df_orig['ID'].astype('string')
    df_anon['DateTime']= df_anon['DateTime'].astype('datetime64[ns]')
    df_anon['ID']= df_anon['ID'].astype('string')
    df_anon['ID']=df_orig['ID']

    #Pre-treatment of original dataframe
    df_orig['lat']=df_orig['lat'].round(size)
    df_orig['lon']=df_orig['lon'].round(size)
    df_orig['Hour'] = df_orig['DateTime'].dt.hour
    df_orig['Day'] = df_orig['DateTime'].dt.day
    df_orig['Month'] = df_orig['DateTime'].dt.month
    df_orig['Week'] = df_orig['DateTime'].dt.isocalendar().week
    df_orig['DayOfTheWeek'] = df_orig['DateTime'].dt.dayofweek
    df_orig.sort_values(by=['ID', 'DateTime'], inplace=True)
    df_orig.reset_index(drop=True, inplace=True)
    df_orig['DatetimeIndex'] = np.select(conditions(df_orig), values, 'RegularTime')
    df_orig['time_spent']=0

    df_orig['Index_of_POI'] = df_orig['ID'] + '-' + df_orig['Day'].astype('string') + '-' + df_orig['Week'].astype('string') + '-' + df_orig['lat'].astype('string') + '-' + df_orig['lon'].astype('string') + '-' + df_orig['DatetimeIndex'].astype('string')
    df_orig['Index_of_POI_shifted_backward'] = df_orig['Index_of_POI'].shift(-1)
    df_orig['Index_of_POI_shifted_forward'] = df_orig['Index_of_POI'].shift(+1)
    df_orig.loc[0,'Index_of_POI_shifted_forward']='0'
    df_orig.loc[len(df_orig)-1,'Index_of_POI_shifted_backward']='0'
    df_orig['start_time'] = df_orig.loc[~(df_orig['Index_of_POI']==df_orig['Index_of_POI_shifted_forward']), 'DateTime']
    df_orig.fillna(method="ffill", inplace=True)
    df_orig['time_spent'] = (df_orig['DateTime'] - df_orig['start_time'])

    #Getting the POI
    df_orig2 = df_orig.loc[~(df_orig['Index_of_POI_shifted_backward']==df_orig['Index_of_POI']),['ID', 'lat', 'lon', 'Week', 'DatetimeIndex', 'time_spent']].groupby(by=['ID', 'lat', 'lon', 'Week', 'DatetimeIndex']).sum().reset_index()
    df_orig2 = df_orig2.sort_values(by=['ID', 'Week', 'time_spent',  'DatetimeIndex'], ascending=[True, True, False, False]).reset_index(drop=True)
    df_orig2 = df_orig2.groupby(by=['ID', 'Week', 'DatetimeIndex']).head(1).reset_index(drop=True)
    
    #Pre-treatment of original dataframe

    df_anon['lat']=df_anon['lat'].round(size)
    df_anon['lon']=df_anon['lon'].round(size)
    df_anon['Hour'] = df_anon['DateTime'].dt.hour
    df_anon['Day'] = df_anon['DateTime'].dt.day
    df_anon['Month'] = df_anon['DateTime'].dt.month
    df_anon['Week'] = df_anon['DateTime'].dt.isocalendar().week
    df_anon['DayOfTheWeek'] = df_anon['DateTime'].dt.dayofweek
    df_anon.sort_values(by=['ID', 'DateTime'], inplace=True)
    df_anon.reset_index(drop=True, inplace=True)
    df_anon['DatetimeIndex'] = np.select(conditions(df_anon), values, 'RegularTime')
    df_anon['time_spent']=0

    df_anon['Index_of_POI'] = df_anon['ID'] + '-' + df_anon['Day'].astype('string') + '-' + df_anon['Week'].astype('string') + '-' + df_anon['lat'].astype('string') + '-' + df_anon['lon'].astype('string') + '-' + df_anon['DatetimeIndex'].astype('string')
    df_anon['Index_of_POI_shifted_backward'] = df_anon['Index_of_POI'].shift(-1)
    df_anon['Index_of_POI_shifted_forward'] = df_anon['Index_of_POI'].shift(+1)
    df_anon.loc[0,'Index_of_POI_shifted_forward']='0'
    df_anon.loc[len(df_anon)-1,'Index_of_POI_shifted_backward']='0'
    
    df_anon['start_time'] = df_anon.loc[~(df_anon['Index_of_POI']==df_anon['Index_of_POI_shifted_forward']), 'DateTime']
    df_anon.fillna(method="ffill", inplace=True)
    df_anon['time_spent'] = (df_anon['DateTime'] - df_anon['start_time'])

    df_anon2 = df_anon.loc[~(df_anon['Index_of_POI_shifted_backward']==df_anon['Index_of_POI']),['ID', 'lat', 'lon', 'Week', 'DatetimeIndex', 'time_spent']].groupby(by=['ID', 'lat', 'lon', 'Week', 'DatetimeIndex']).sum().reset_index()
    
    #Comparing the time spent in POI between original and anonymized dataset
    df_orig2 = df_orig2.loc[~(df_orig2.DatetimeIndex =='RegularTime')]
    left_join_df = pd.merge(df_orig2, df_anon2, on=['ID','lat','lon','Week','DatetimeIndex'], how='left')
    
    left_join_df['time_spent_y'] = left_join_df['time_spent_y'].fillna(pd.Timedelta(seconds=0))
    left_join_df['diff_time_spent'] = abs( left_join_df['time_spent_y'].dt.total_seconds() - left_join_df['time_spent_x'].dt.total_seconds() )
    left_join_df['time_spent_x'] = left_join_df['time_spent_x'].dt.total_seconds()
    
    #Calculating the scrore
    score = 1- (left_join_df['diff_time_spent'].sum()/left_join_df['time_spent_x'].sum())
    return score

def conditions(df):
    return [
        (df['DayOfTheWeek'] < 4) & (df['Hour']>=22) & (df['Hour']<=23), 
        (df['DayOfTheWeek'] < 4) & (df['Hour']>=0) & (df['Hour']<=6),
        (df['DayOfTheWeek'] < 4) & (df['Hour']>=9) & (df['Hour']<=17),
        (df['DayOfTheWeek'] >= 4) & (df['Hour']>=10) & (df['Hour']<=18)
    ]
