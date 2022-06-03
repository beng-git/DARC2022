import pandas as pd

def main(df_anon, df_original, params, nb_orig_lines):
    df_orig = df_original.copy()
    df_anon = df_anon.copy()
    df_orig.rename(columns={'id':'ID', 'date':'DateTime', 'latitude':'lat', 'longitude':'lon'},inplace=True)
    df_anon.rename(columns={'id':'ID', 'date':'DateTime', 'latitude':'lat', 'longitude':'lon'},inplace=True)

    df_orig['DateTime']= df_orig['DateTime'].astype('datetime64[ns]')
    #df_orig['ID']= df_orig['ID'].astype('string')
    df_anon['DateTime']= df_anon['DateTime'].astype('datetime64[ns]')
    #df_anon['ID']= df_anon['ID'].astype('string')

    df = pd.DataFrame({ 'df_hour': df_anon['DateTime'].dt.hour, 'df_origin_hour': df_orig['DateTime'].dt.hour })
    #Chaque ligne vaut 1 point
    #Une fraction de point eguale a 1/24 est enlevée à chaque heure d'écart
    df['hour_util'] = 1- abs(df['df_hour'] - df['df_origin_hour'])/24
    # le score finale est la moyenne d'ecart d'heures sur tous les points detecter
    score_hour_utility = df["hour_util"].sum()/len(df_orig)
    
    return score_hour_utility