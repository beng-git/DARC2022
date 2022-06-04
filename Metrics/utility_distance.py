import pandas as pd
import numpy as np
# cette metrique calcule la difference de distance entre le point GPS original et les nouvelles lat lon (en km) en utilisant la metrique de Haversine
#le score final est l'inverse de la moyenne de diffrence de distance calculee pour chauqe point
def main(df_anon, df_original):

    df_orig = df_original.copy()
    df_anon = df_anon.copy()
    df_orig.rename(columns={'id':'ID', 'date':'DateTime', 'latitude':'lat', 'longitude':'lon'},inplace=True)
    df_anon.rename(columns={'id':'ID', 'date':'DateTime', 'latitude':'lat', 'longitude':'lon'},inplace=True)
    df_anon.rename(columns={'ID':'ID_ano', 'DateTime':'DateTime_ano', 'lat':'lat_ano', 'lon':'lon_ano'}, inplace = True)
    
    df_orig['lat']= df_orig['lat'].astype('float64')
    df_orig['lon']= df_orig['lon'].astype('float64')
    df_anon['lat_ano']= df_anon['lat_ano'].astype('float64')
    df_anon['lon_ano']= df_anon['lon_ano'].astype('float64')
    
    df = pd.concat([df_orig.reset_index(drop=True),df_anon.reset_index(drop=True)], axis=1)
   
    #Haversine metrqiue
    to_radians = np.pi/180
    R = 6371.009 #en km
    #a=np.sin(((df.lat*to_radians-df.lat_ano*to_radians)/2)**2) + np.sin((((df.lon*to_radians-df.lon_ano*to_radians)/2)**2))*np.cos(df.lat*to_radians)*np.cos(df.lat_ano*to_radians)
    a = np.sin(((df.lat*to_radians-df.lat_ano*to_radians)/2))**2 + (np.sin((((df.lon*to_radians-df.lon_ano*to_radians)/2)))**(2))*np.cos(df.lat*to_radians)*np.cos(df.lat_ano*to_radians)
    b = np.sqrt(a)
    df['Haversine_score']= 2 * R * np.arcsin(b)
    if(df["Haversine_score"].mean().round(3)==0):
        score = 1
    else:
        #print(df["Haversine_score"].mean())
        score = (1/(df["Haversine_score"].mean())).round(3)
    return score