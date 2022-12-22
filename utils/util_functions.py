import pandas as pd
import geopandas as gpd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def get_df_in_buffer(path_df,geodf_buffer, get_orig = False):
    df = pd.read_csv(path_df)
    # print(len(df))
    df_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude)) # X,Y coordinates in longitude and latitude
    df_geo = df_geo.drop(['index_right'], axis=1) # drop index_right column (no tener problemas)
    df_in_buffer = gpd.sjoin(df_geo, geodf_buffer)
    df_in_buffer = df_in_buffer[df_in_buffer["ID_1"].notna()]
    if get_orig:
        return df, df_in_buffer
    else:
        return df_in_buffer

def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_

def get_all_dis():
    # for path_disaggregated in sorted(glob.glob("colombia_disaggregated/*07*.csv")):
    for i,path_disaggregated in enumerate(sorted(glob.glob("../../colombia_disaggregated/*.csv"))):
        df_dis = pd.read_csv(path_disaggregated) 
        if i > 0:
            df_dis = pd.concat([df_dis,df_dis_ant], axis = 0)
            df_dis_ant = df_dis
        else:
            df_dis_ant = df_dis
    return df_dis

def plot_corr_join(data, x, y, **kwargs):
    g = sns.jointplot(data=data, 
                  x= x, 
                  y= y,
                  **kwargs)
        
    g1 = sns.regplot(y=y, x=x, 
                    data = data, 
                    scatter=False, ax=g.ax_joint)
    regline = g1.get_lines()[0]
    regline.set_color('red')
    regline.set_zorder(5)

    maxarr = np.max(list(data[x])+list(data[y]))
    xx = np.linspace(0,maxarr)
    g1.plot(xx,xx, c = 'r', ls = "--")        
    # plt.loglog()
    # plt.show()  