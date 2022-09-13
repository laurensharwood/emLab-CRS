#!/usr/bin/ python

import os, sys
import pandas as pd 
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.cm
import matplotlib.colors
from shapely.geometry import shape
import plotly
import plotly.express as px
from IPython.display import Image, display
import json
import ipyleaflet
import ipywidgets as ipyw
from ipyleaflet import * 
from ipywidgets import *
import folium
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')




def temporal_profile_for_practices(grid, index_list):
    for i in index_list:
        input_csv = "time_series/NI/" + grid + "_" + i + "_TimeSeries.csv"
        df1 = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=True)
        df = df1[df1["FieldID"].apply(len) < 15] ## DON'T INCLUDE PLOTS WITH NO PRACTICE DATA
        Y_axis_limit = df["Value"].max()+50
        Y_axis_min = df["Value"].min()-50
        fig = px.line(df, x='Date', y='Value', title= i.upper() + ' Time Series (for plots in grid ' + grid + ")", 
                      color='FieldID', 
                      color_discrete_sequence=px.colors.qualitative.Dark2, # Bold, Vivid, Dark2, Pastel
                      line_dash='Parcela')
        fig.update_layout(xaxis_title='Date', yaxis_title='VI Value')
        fig.update_xaxes(rangeslider_visible=True, 
                         rangeselector=dict(buttons=list([dict(count=6, label="6m", step="month", stepmode="backward"),
                                                          dict(count=1, label="1y", step="year", stepmode="backward"), 
                                                          dict(count=2, label="2y", step="year", stepmode="backward"), 
                                                          dict(step="all")]) ))
        fig.add_trace(go.Bar(name="CC", x=["2016-12-01", "2017-12-01", "2018-12-01", "2019-12-01"], y=[Y_axis_limit, Y_axis_limit, Y_axis_limit, Y_axis_limit], marker=dict(color=px.colors.qualitative.Antique[6]), opacity= 0.3, xperiod="M1", xperiodalignment="middle", xhoverformat="Q%q", hovertemplate="cover crop visibility window"))
        fig.add_trace(go.Bar(name="CR", x=["2017-03-01", "2018-03-01", "2019-03-01", "2020-03-01"], y=[Y_axis_limit, Y_axis_limit, Y_axis_limit, Y_axis_limit], marker=dict(color=px.colors.qualitative.Antique[1]), opacity= 0.3, xperiod="M1", xperiodalignment="middle", xhoverformat="Q%q", hovertemplate="crop residue visibility window"))
        fig.update(layout_yaxis_range = [Y_axis_min,Y_axis_limit])
        fig.show()
      
        
def temporal_profile(grid, index_list):
    for i in index_list:
        input_csv = "time_series/" + grid + "_" + i + "_TimeSeries.csv"
        df = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=True)
        Y_axis_limit = df["Value"].max()+1000
        fig = px.line(df, x='Date', y='Value', title= i.upper() + ' Time Series (for plots in grid ' + grid + ")", 
                      color='FieldID', 
                      color_discrete_sequence=px.colors.qualitative.Dark2, # Bold, Vivid, Dark2, Pastel
                      line_dash='Parcela')
        fig.update_layout(xaxis_title='Date', yaxis_title='VI Value')
        fig.update_xaxes(rangeslider_visible=True, 
                         rangeselector=dict(buttons=list([dict(count=6, label="6m", step="month", stepmode="backward"),
                                                          dict(count=1, label="1y", step="year", stepmode="backward"), 
                                                          dict(count=2, label="2y", step="year", stepmode="backward"), 
                                                          dict(step="all")]) ))
        fig.add_trace(go.Bar(name="CC", x=["2016-12-01", "2017-12-01", "2018-12-01", "2019-12-01"], y=[Y_axis_limit, Y_axis_limit, Y_axis_limit, Y_axis_limit], marker=dict(color=px.colors.qualitative.Antique[6]), opacity= 0.3, xperiod="M1", xperiodalignment="middle", xhoverformat="Q%q", hovertemplate="cover crop visibility window"))
        fig.add_trace(go.Bar(name="CR", x=["2017-03-01", "2018-03-01", "2019-03-01", "2020-03-01"], y=[Y_axis_limit, Y_axis_limit, Y_axis_limit, Y_axis_limit], marker=dict(color=px.colors.qualitative.Antique[1]), opacity= 0.3, xperiod="M1", xperiodalignment="middle", xhoverformat="Q%q", hovertemplate="crop residue visibility window"))
        fig.show()
      


    
    
    
def border(feature):
    if feature["properties"]["Parcela"] == "ASA":
        return 1
    elif feature["properties"]["Parcela"] == "Testigo":
        return 3
    
    
def create_marker(row):
    loc = row['geometry.coordinates']
    name = row['properties.ID_Prod']
    colr = row['properties.color']
    lat_lon = (loc[1], loc[0])
    return CircleMarker(location=lat_lon,
                    draggable=False,
                    title=name,
                    label=name,
                    radius=1,
                    weight=5,
                    color=colr,
                    fillColor="black")


def display_plots(grid, index_list):
    with open("NI_ES_grid_centroids.geojson") as gc:
        grid_center = json.load(gc)
        grid_center_df = pd.json_normalize(grid_center['features'])
        viewing_grid = grid_center_df[grid_center_df["properties.UNQ"] == int(grid[2:])]
        center_map = viewing_grid["geometry.coordinates"].to_list()
    with open("NI_ES_plots.geojson") as f:
        data = json.load(f)
    for feature in data["features"]:
        feature["properties"]["style"] = {
                "weight": 1.5,
                "fillOpacity":0,
                "color":"white",
                "dashArray": border(feature)}        
    with open("NI_ES_points_col.geojson") as p:
        datap = json.load(p)
        points_df = pd.json_normalize(datap['features'])
        markers = points_df.apply(create_marker, axis=1)
        layer_group = LayerGroup(layers=tuple(markers.values), name='Plot Centers')
        marker_cluster = MarkerCluster(markers=tuple(markers.values))
    
    geo = GeoJSON(data=data, name='Plot Boundaries', hover_style={
        'color': 'yellow', 'dashArray': '0', 'fillOpacity': 0.5
    })  
    
    OpenTopoMap = basemap_to_tiles(basemaps.OpenTopoMap)
    OpenTopoMap.base = True
    OpenTopoMap.name = 'Open Topo Map'
    
    background = basemap_to_tiles(basemaps.Esri.WorldImagery)
    background.base = True
    background.name = "ESRI World Imagery"
    
    m = Map(layers=(OpenTopoMap, background,  ), center=(center_map[0][1], center_map[0][0]), zoom=13, scroll_wheel_zoom=True, zoom_control=False, close_popup_on_click=False)

    def update_html(feature, **kwargs):
        html1.value = """ 
        <h4>Producer ID: {} </h4>
        {} Parcela """.format(feature["properties"]["ID_Prod"], feature["properties"]["Parcela"] )
        
    html1 = HTML("""<h4>Plot ID & Parcela </h4>Hover over a plot""")
    html1.layout.margin = "0px 5px 5px 5px"
    control1 = WidgetControl(widget=html1, position="topleft")
    m.add(control1)
    control = LayersControl(position='topright')
    m.add_control(control)
    m.add_control(ScaleControl(position='topright'))
    m.add_control(ZoomControl(position='topright'))
    m.add_layer(layer_group)
    m.add_layer(geo)
    geo.on_hover(update_html)
      
    ## display practice database
    practices_csv = "time_series/practices_NI_ES.csv"
    practices_df = pd.read_csv(practices_csv, dtype=str) 
    grid_practice_df = practices_df.loc[practices_df['Grid'] == str(grid)]
    practices = pd.pivot(grid_practice_df, index=['ID_Prod','Parcela', 'Nom.Cob'], columns=['Temporada','Ano'], values=['Cultivo'])
    cols = practices.columns.tolist()
    practices = practices[[cols[1], cols[0], cols[3], cols[2], cols[5], cols[4], cols[7], cols[6]]]
    display(practices)

    ## display EVI2 time series
    temporal_profile_for_practices(grid, index_list)
    
    ## display map
    return m



def aggregate_plots(input_dir, index):
    index_merge = [ind for ind in sorted(os.listdir(input_dir)) if str(index) in ind] # list of filenames in the input directory that contain the index string
    merged_csv = pd.DataFrame() # initialize df to put plots from all grids into
    for csv in index_merge:
        input_csv = input_dir + csv
        df = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=True) 
        df = df[df["FieldID"].apply(len) < 15] # remove plots without practice data (have a longer code for the name)
        df = df.loc[(df["Date"] >= "2016-04-31") & (df["Date"] <= "2020-04-31")] # subset time series only to 2016-2019 crop calendar year 
        df["YR"] = int(0) # create column for crop calendar year       
        df.loc[df.Parcela == "Testigo", "Value"] = (-1*df["Value"]) # add negative to Testigo for subtraction difference (val should be higher if ASA plot is higher than test)
        df_diff = df.groupby(by=['FieldID', 'Date']).sum() # subtract Testigo from ASA plot at each date for each plot 
        #df = df.reset_index()        
        df_diff = df_diff.rename(columns = {'Value': "ATdiff"})
        merged_csv = pd.concat([merged_csv, df_diff])
    merged_csv = merged_csv.reset_index()
    merged_csv.loc[(merged_csv['Date'] > "2016-04-31") & (merged_csv["Date"] <= "2017-04-31"), 'YR'] = "2016"
    merged_csv.loc[(merged_csv['Date'] > "2017-04-31") & (merged_csv["Date"] <= "2018-04-31"), 'YR'] = "2017"
    merged_csv.loc[(merged_csv['Date'] > "2018-04-31") & (merged_csv["Date"] <= "2019-04-31"), 'YR'] = "2018"
    merged_csv.loc[(merged_csv['Date'] > "2019-04-31") & (merged_csv["Date"] <= "2020-04-31"), 'YR'] = "2019"
    out_csv_path = input_dir + "ATdiffmerged/" + str(index) + "_ATdiff_merged.csv"
    return merged_csv.to_csv(out_csv_path)    

def AT_stats(input_csv, plotID, output_csv=False, seasonal_csv=False, plot=True):
    merged_csv = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=True)
    ## STATISTICS BY AG YEAR
    df16 = merged_csv.loc[(merged_csv['YR'] == 2016)] # subset for each ag year 
    df17 = merged_csv.loc[(merged_csv['YR'] == 2017)]
    df18 = merged_csv.loc[(merged_csv['YR'] == 2018)] 
    df19 = merged_csv.loc[(merged_csv['YR'] == 2019)]
    mean16 = df16.groupby("Date")["ATdiff"].mean().to_frame().reset_index()  # mean as dataframe
    stDev16 = df16.groupby("Date")["ATdiff"].std().to_frame().reset_index() # standard deviation as dataframe
    mean17 = df17.groupby("Date")["ATdiff"].mean().to_frame().reset_index()
    stDev17 = df17.groupby("Date")["ATdiff"].std().to_frame().reset_index()
    mean18 = df18.groupby("Date")["ATdiff"].mean().to_frame().reset_index()
    stDev18 = df18.groupby("Date")["ATdiff"].std().to_frame().reset_index()
    mean19 = df19.groupby("Date")["ATdiff"].mean().to_frame().reset_index()
    stDev19 = df19.groupby("Date")["ATdiff"].std().to_frame().reset_index()
    plot16 = df16.loc[df16['FieldID'] == plotID]
    plot17 = df17.loc[df17['FieldID'] == plotID]
    plot18 = df18.loc[df18['FieldID'] == plotID]
    plot19 = df19.loc[df19['FieldID'] == plotID]
     # seasonal stats for threshold grouping 
    df16.loc[(df16['Date'] >= "2016-05-01") & (df16["Date"] <= "2016-10-31"), 'Season'] = "main crop"
    df16.loc[(df16['Date'] >= "2016-11-01") & (df16["Date"] <= "2017-01-31"), 'Season'] = "COVER CROP"
    df16.loc[(df16['Date'] >= "2017-02-01") & (df16["Date"] <= "2017-04-31"), 'Season'] = "CROP RESIDUE"
    df17.loc[(df17['Date'] >= "2017-05-01") & (df17["Date"] <= "2017-10-31"), 'Season'] = "main crop"
    df17.loc[(df17['Date'] >= "2017-11-01") & (df17["Date"] <= "2018-01-31"), 'Season'] = "COVER CROP"
    df17.loc[(df17['Date'] >= "2018-02-01") & (df17["Date"] <= "2018-04-31"), 'Season'] = "CROP RESIDUE"
    df18.loc[(df18['Date'] >= "2018-05-01") & (df18["Date"] <= "2018-10-31"), 'Season'] = "main crop"
    df18.loc[(df18['Date'] >= "2018-11-01") & (df18["Date"] <= "2019-01-31"), 'Season'] = "COVER CROP"
    df18.loc[(df18['Date'] >= "2019-02-01") & (df18["Date"] <= "2019-04-31"), 'Season'] = "CROP RESIDUE"
    df19.loc[(df19['Date'] >= "2019-05-01") & (df19["Date"] <= "2019-10-31"), 'Season'] = "main crop"
    df19.loc[(df19['Date'] >= "2019-11-01") & (df19["Date"] <= "2020-01-31"), 'Season'] = "COVER CROP"
    df19.loc[(df19['Date'] >= "2020-02-01") & (df19["Date"] <= "2020-04-31"), 'Season'] = "CROP RESIDUE"

    # merge DF back together
    all_years = [df16, df17, df18, df19]
    all_years_merged = pd.DataFrame()
    for i in all_years:
        all_years_merged = pd.concat([all_years_merged, i])
    date_u =  all_years_merged.groupby(["Date"])["ATdiff"].mean().to_frame().reset_index()
    date_std =  all_years_merged.groupby(["Date"])["ATdiff"].std().to_frame().reset_index()
    seasonal_std = all_years_merged.groupby(["YR", "Season"])["ATdiff"].std().to_frame().reset_index()
    seasonal_std.rename(columns = {'YR':'YR','Season':'Season', 'ATdiff':'SznStd'}, inplace = True)
    seasonal_u = all_years_merged.groupby(["YR", "Season"])["ATdiff"].mean().to_frame().reset_index()
    plot_season_mean = all_years_merged.groupby(["FieldID", "YR", "Season"])["ATdiff"].mean().to_frame().reset_index()
    plot_season_mean.rename(columns = {'FieldID':'FieldID', 'YR':'YR','Season':'Season', 'ATdiff':'plotSZNmean'}, inplace = True)

    all_years_merged1 = pd.merge(all_years_merged, date_u, on=["Date"])
    all_years_stat = pd.merge(all_years_merged1, date_std, on=["Date"])
    all_years_stat.rename(columns = {'FieldID':'FieldID', 'Date':'Date','ATdiff_x':'AT_VIdiff', 'YR':'YR','Season':'Season', 'ATdiff_y':'DATEmean','ATdiff':'DATEstd'}, inplace = True)
    #all_years_stat = pd.merge(all_years_stat, seasonal_u, on=(["YR", "Season"]))
    all_years_stats = pd.merge(all_years_stat, seasonal_std, on=(["YR", "Season"]))
    all_years_seasons_stats = pd.merge(all_years_stats, plot_season_mean, on=(["FieldID", "YR", "Season"]))
    all_years_seasons_stats.rename(columns = {'FieldID':'FieldID', 'Date':'Date','AT_VIdiff':'AT_VIdiff', 'YR':'AgYR','Season':'SZNwindow', 'DATEmean':'DATEmean','DATEstd':'DATEstd'}, inplace = True)
    all_years_seasons_stats['Group'] = 'main crop'
    all_years_seasons_stats.loc[(all_years_seasons_stats["AT_VIdiff"] <= (all_years_seasons_stats['DATEmean']-all_years_seasons_stats['DATEstd'])), 'Group'] = "4: (T>A) less than MEAN-1SD"
    all_years_seasons_stats.loc[(all_years_seasons_stats["AT_VIdiff"] >= (all_years_seasons_stats['DATEmean']-all_years_seasons_stats['DATEstd'])) & (all_years_seasons_stats["AT_VIdiff"] <= 0), 'Group'] = "3: (t>a) btwn 0 and MEAN-1SD"
    all_years_seasons_stats.loc[(all_years_seasons_stats["AT_VIdiff"] <= (all_years_seasons_stats['DATEmean']+all_years_seasons_stats['DATEstd'])) & (all_years_seasons_stats["AT_VIdiff"] >= 0), 'Group'] = "2: (a>t) btwn 0 and MEAN+1SD"
    all_years_seasons_stats.loc[(all_years_seasons_stats["AT_VIdiff"] >= (all_years_seasons_stats['DATEmean']+all_years_seasons_stats['DATEstd'])), 'Group'] = "1: (A>T) more than MEAN+1SD"   
    # mean / sd by season 
    szn_stats = all_years_seasons_stats.loc[:, all_years_seasons_stats.columns.isin(['FieldID', 'SZNwindow', 'SznStd', 'plotSZNmean'])].drop_duplicates()   
    szn_stats['Group'] = 'main crop'
    szn_stats.loc[(szn_stats["plotSZNmean"] <= (0 - szn_stats['SznStd'])), 'Group'] = "4: (T>A) avg seasonal A-T diff less than -1SD"
    szn_stats.loc[(szn_stats["plotSZNmean"] >= (-1*szn_stats['SznStd'])) & (szn_stats["plotSZNmean"] <= 0), 'Group'] = "3: (t>a) avg seasonal A-T diff btwn 0 and -1SD"
    szn_stats.loc[(szn_stats["plotSZNmean"] <= (1*szn_stats['SznStd'])) & (szn_stats["plotSZNmean"] >= 0), 'Group'] = "2: (a>t)  avg seasonal A-T diff btwn 0 and +1SD"
    szn_stats.loc[(szn_stats["plotSZNmean"] >= (0 + szn_stats['SznStd'])), 'Group'] = "1: (A>T) avg seasonal A-T diff greater than +1SD"
    
    if output_csv==True:
        out_csv_path = input_csv[:-4] + "_stats.csv"
        all_years_stats.to_csv(out_csv_path)
    
    if seasonal_csv==True:
        out_csv_path = input_csv[:-4] + "_SZN_stats.csv"
        szn_stats.to_csv(out_csv_path)
        
    if plot==True:
        full_fig = go.Figure()
        upperB16=mean16["ATdiff"]+stDev16["ATdiff"]
        lowerB16=mean16["ATdiff"]-stDev16["ATdiff"]
        upperB17=mean17["ATdiff"]+stDev17["ATdiff"]
        lowerB17=mean17["ATdiff"]-stDev17["ATdiff"]
        upperB18=mean18["ATdiff"]+stDev18["ATdiff"]
        lowerB18=mean18["ATdiff"]-stDev18["ATdiff"]
        upperB19=mean19["ATdiff"]+stDev19["ATdiff"]
        lowerB19=mean19["ATdiff"]-stDev19["ATdiff"]
        # plot user input fieldID
        full_fig.add_trace(go.Scatter(x=plot16["Date"], y=plot16["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2016 A-T diff"))
        full_fig.add_trace(go.Scatter(x=plot17["Date"], y=plot17["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2017 A-T diff"))
        full_fig.add_trace(go.Scatter(x=plot18["Date"], y=plot18["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2018 A-T diff"))
        full_fig.add_trace(go.Scatter(x=plot19["Date"], y=plot19["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2019 A-T diff"))
        full_fig.add_trace(go.Scatter(x=mean19["Date"], y=upperB19, mode='lines', line=dict(color=px.colors.sequential.thermal[7],width =0.1),name=""))
        full_fig.add_trace(go.Scatter(x=mean19["Date"], y=mean19["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[7]),fill='tonexty', name='2019 Mean'))
        full_fig.add_trace(go.Scatter(x=mean19["Date"], y=lowerB19, mode='lines', line=dict(color=px.colors.sequential.thermal[7],width =0.1), fill='tonexty',name='2019 SD'))        
        full_fig.add_trace(go.Scatter(x=mean18["Date"], y=upperB18, mode='lines', line=dict(color=px.colors.sequential.thermal[6],width =0.1), name=''))
        full_fig.add_trace(go.Scatter(x=mean18["Date"], y=mean18["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[6]),fill='tonexty', name='2018 Mean'))
        full_fig.add_trace(go.Scatter(x=mean18["Date"], y=lowerB18, mode='lines', line=dict(color=px.colors.sequential.thermal[6],width =0.1), fill='tonexty',name='2018 SD'))
        full_fig.add_trace(go.Scatter(x=mean17["Date"], y=upperB17, mode='lines', line=dict(color=px.colors.sequential.thermal[5],width =0.1), name=''))
        full_fig.add_trace(go.Scatter(x=mean17["Date"], y=mean17["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[5]),fill='tonexty', name='2017 Mean'))
        full_fig.add_trace(go.Scatter(x=mean17["Date"], y=lowerB17, mode='lines', line=dict(color=px.colors.sequential.thermal[5],width =0.1), fill='tonexty',name='2017 SD'))
        full_fig.add_trace(go.Scatter(x=mean16["Date"], y=upperB16, mode='lines', line=dict(color=px.colors.sequential.thermal[4],width =0.1), name=''))
        full_fig.add_trace(go.Scatter(x=mean16["Date"], y=mean16["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[4]),fill='tonexty', name='2016 Mean'))
        full_fig.add_trace(go.Scatter(x=mean16["Date"], y=lowerB16, mode='lines', line=dict(color=px.colors.sequential.thermal[4],width =0.1), fill='tonexty',name='2016 SD'))
        splitpath = input_csv.split('/')
        splitfile = splitpath[-1].split('_')
        index = splitfile[0].upper()
        full_fig.update_layout(title_text='Mean and Standard Deviation ' + str(index) +  ' ASA-Testigo difference across all plots (every 10 days)', title_x=0.5)
        Y_axis_limit = stDev18["ATdiff"].max()+50
        Y_axis_min = stDev18["ATdiff"].min()-50        
        full_fig.add_trace(go.Bar(name="CR", x=["2017-01-01", "2018-01-01", "2019-01-01", "2020-01-01"], y=[800, 800, 800, 800], marker=dict(color=px.colors.qualitative.Antique[1]), opacity= 0.3, xperiod="M3", xperiodalignment="end", xhoverformat="Q%q", hovertemplate="crop residue visibility window"))
        full_fig.add_trace(go.Bar(name="CC", x=["2016-10-01", "2017-10-01", "2018-10-01", "2019-10-01"], y=[800, 800, 800, 800], marker=dict(color=px.colors.qualitative.Antique[6]), opacity= 0.3, xperiod="M3", xperiodalignment="end", xhoverformat="Q%q", hovertemplate="cover crop visibility window"))
        full_fig.show()
        

def OLD_AT_stats(input_csv, plotID, output_csv=False, plot=True):
    merged_csv = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=True)
    ## STATISTICS BY AG YEAR
    df16 = merged_csv.loc[(merged_csv['YR'] == 2016)] # subset for each ag year 
    df17 = merged_csv.loc[(merged_csv['YR'] == 2017)]
    df18 = merged_csv.loc[(merged_csv['YR'] == 2018)] 
    df19 = merged_csv.loc[(merged_csv['YR'] == 2019)]
    mean16 = df16.groupby("Date")["ATdiff"].mean().to_frame().reset_index()  # mean as dataframe
    stDev16 = df16.groupby("Date")["ATdiff"].std().to_frame().reset_index() # standard deviation as dataframe
    mean17 = df17.groupby("Date")["ATdiff"].mean().to_frame().reset_index()
    stDev17 = df17.groupby("Date")["ATdiff"].std().to_frame().reset_index()
    mean18 = df18.groupby("Date")["ATdiff"].mean().to_frame().reset_index()
    stDev18 = df18.groupby("Date")["ATdiff"].std().to_frame().reset_index()
    mean19 = df19.groupby("Date")["ATdiff"].mean().to_frame().reset_index()
    stDev19 = df19.groupby("Date")["ATdiff"].std().to_frame().reset_index()
    plot16 = df16.loc[df16['FieldID'] == plotID]
    plot17 = df17.loc[df17['FieldID'] == plotID]
    plot18 = df18.loc[df18['FieldID'] == plotID]
    plot19 = df19.loc[df19['FieldID'] == plotID]
     # seasonal stats for threshold grouping 
    df16.loc[(df16['Date'] >= "2016-05-01") & (df16["Date"] <= "2016-10-31"), 'Season'] = "main crop"
    df16.loc[(df16['Date'] >= "2016-11-01") & (df16["Date"] <= "2017-01-31"), 'Season'] = "COVER CROP"
    df16.loc[(df16['Date'] >= "2017-02-01") & (df16["Date"] <= "2017-04-31"), 'Season'] = "CROP RESIDUE"
    df17.loc[(df17['Date'] >= "2017-05-01") & (df17["Date"] <= "2017-10-31"), 'Season'] = "main crop"
    df17.loc[(df17['Date'] >= "2017-11-01") & (df17["Date"] <= "2018-01-31"), 'Season'] = "COVER CROP"
    df17.loc[(df17['Date'] >= "2018-02-01") & (df17["Date"] <= "2018-04-31"), 'Season'] = "CROP RESIDUE"
    df18.loc[(df18['Date'] >= "2018-05-01") & (df18["Date"] <= "2018-10-31"), 'Season'] = "main crop"
    df18.loc[(df18['Date'] >= "2018-11-01") & (df18["Date"] <= "2019-01-31"), 'Season'] = "COVER CROP"
    df18.loc[(df18['Date'] >= "2019-02-01") & (df18["Date"] <= "2019-04-31"), 'Season'] = "CROP RESIDUE"
    df19.loc[(df19['Date'] >= "2019-05-01") & (df19["Date"] <= "2019-10-31"), 'Season'] = "main crop"
    df19.loc[(df19['Date'] >= "2019-11-01") & (df19["Date"] <= "2020-01-31"), 'Season'] = "COVER CROP"
    df19.loc[(df19['Date'] >= "2020-02-01") & (df19["Date"] <= "2020-04-31"), 'Season'] = "CROP RESIDUE"

    # merge DF back together
    all_years = [df16, df17, df18, df19]
    all_years_merged = pd.DataFrame()
    for i in all_years:
        all_years_merged = pd.concat([all_years_merged, i])
    date_u =  all_years_merged.groupby(["Date"])["ATdiff"].mean().to_frame().reset_index()
    date_std =  all_years_merged.groupby(["Date"])["ATdiff"].std().to_frame().reset_index()
    seasonal_std = all_years_merged.groupby(["YR", "Season"])["ATdiff"].std().to_frame().reset_index()
    seasonal_u = all_years_merged.groupby(["YR", "Season"])["ATdiff"].mean().to_frame().reset_index()

    all_years_merged1 = pd.merge(all_years_merged, date_u, on=["Date"])
    all_years_stat = pd.merge(all_years_merged1, date_std, on=["Date"])
    all_years_stat.rename(columns = {'FieldID':'FieldID', 'Date':'Date','ATdiff_x':'AT_VIdiff', 'YR':'YR','Season':'Season', 'ATdiff_y':'DATEmean','ATdiff':'DATEstd'}, inplace = True)
    all_years_stat = pd.merge(all_years_stat, seasonal_u, on=(["YR", "Season"]))
    all_years_stats = pd.merge(all_years_stat, seasonal_std, on=(["YR", "Season"]))
    all_years_stats.rename(columns = {'FieldID':'FieldID', 'Date':'Date','AT_VIdiff':'AT_VIdiff', 'YR':'AgYR','Season':'SZNwindow', 'DATEmean':'DATEmean','DATEstd':'DATEstd', 'ATdiff_x':'SZNmean','ATdiff_y':'SZNstd'}, inplace = True)
    all_years_stats['Group'] = 'main crop'
    all_years_stats.loc[(all_years_stats["AT_VIdiff"] <= (all_years_stats['DATEmean']-all_years_stats['DATEstd'])), 'Group'] = "4: (T>A) less than MEAN-1SD"
    all_years_stats.loc[(all_years_stats["AT_VIdiff"] >= (all_years_stats['DATEmean']-all_years_stats['DATEstd'])) & (all_years_stats["AT_VIdiff"] <= 0), 'Group'] = "3: (t>a) btwn 0 and MEAN-1SD"
    all_years_stats.loc[(all_years_stats["AT_VIdiff"] <= (all_years_stats['DATEmean']+all_years_stats['DATEstd'])) & (all_years_stats["AT_VIdiff"] >= 0), 'Group'] = "2: (a>t) btwn 0 and MEAN+1SD"
    all_years_stats.loc[(all_years_stats["AT_VIdiff"] >= (all_years_stats['DATEmean']+all_years_stats['DATEstd'])), 'Group'] = "1: (A>T) more than MEAN+1SD"
    # count number in each category by YEAR and SEASON 
    
    if output_csv==True:
        out_csv_path = input_csv[:-4] + "_stats.csv"
        print(out_csv_path)
        all_years_stats.to_csv(out_csv_path)
    
    if plot==True:
        full_fig = go.Figure()
        upperB16=mean16["ATdiff"]+stDev16["ATdiff"]
        lowerB16=mean16["ATdiff"]-stDev16["ATdiff"]

        upperB17=mean17["ATdiff"]+stDev17["ATdiff"]
        lowerB17=mean17["ATdiff"]-stDev17["ATdiff"]

        upperB18=mean18["ATdiff"]+stDev18["ATdiff"]
        lowerB18=mean18["ATdiff"]-stDev18["ATdiff"]
        
        upperB19=mean19["ATdiff"]+stDev19["ATdiff"]
        lowerB19=mean19["ATdiff"]-stDev19["ATdiff"]
        
        # plot user input field
        full_fig.add_trace(go.Scatter(x=plot16["Date"], y=plot16["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2016 A-T diff"))
        full_fig.add_trace(go.Scatter(x=plot17["Date"], y=plot17["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2017 A-T diff"))
        full_fig.add_trace(go.Scatter(x=plot18["Date"], y=plot18["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2018 A-T diff"))
        full_fig.add_trace(go.Scatter(x=plot19["Date"], y=plot19["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[1],width =3.0), name=str(plotID) + " 2019 A-T diff"))
                # add Y16 mean and SD 
        full_fig.add_trace(go.Scatter(x=mean19["Date"], y=upperB19, mode='lines', line=dict(color=px.colors.sequential.thermal[7],width =0.1),name=""))
        full_fig.add_trace(go.Scatter(x=mean19["Date"], y=mean19["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[7]),fill='tonexty', name='2019 Mean'))
        full_fig.add_trace(go.Scatter(x=mean19["Date"], y=lowerB19, mode='lines', line=dict(color=px.colors.sequential.thermal[7],width =0.1), fill='tonexty',name='2019 SD'))        
        full_fig.add_trace(go.Scatter(x=mean18["Date"], y=upperB18, mode='lines', line=dict(color=px.colors.sequential.thermal[6],width =0.1), name=''))
        full_fig.add_trace(go.Scatter(x=mean18["Date"], y=mean18["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[6]),fill='tonexty', name='2018 Mean'))
        full_fig.add_trace(go.Scatter(x=mean18["Date"], y=lowerB18, mode='lines', line=dict(color=px.colors.sequential.thermal[6],width =0.1), fill='tonexty',name='2018 SD'))
        full_fig.add_trace(go.Scatter(x=mean17["Date"], y=upperB17, mode='lines', line=dict(color=px.colors.sequential.thermal[5],width =0.1), name=''))
        full_fig.add_trace(go.Scatter(x=mean17["Date"], y=mean17["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[5]),fill='tonexty', name='2017 Mean'))
        full_fig.add_trace(go.Scatter(x=mean17["Date"], y=lowerB17, mode='lines', line=dict(color=px.colors.sequential.thermal[5],width =0.1), fill='tonexty',name='2017 SD'))
        full_fig.add_trace(go.Scatter(x=mean16["Date"], y=upperB16, mode='lines', line=dict(color=px.colors.sequential.thermal[4],width =0.1), name=''))
        full_fig.add_trace(go.Scatter(x=mean16["Date"], y=mean16["ATdiff"], mode='lines', line=dict(color=px.colors.sequential.thermal[4]),fill='tonexty', name='2016 Mean'))
        full_fig.add_trace(go.Scatter(x=mean16["Date"], y=lowerB16, mode='lines', line=dict(color=px.colors.sequential.thermal[4],width =0.1), fill='tonexty',name='2016 SD'))

        splitpath = input_csv.split('/')
        splitfile = splitpath[-1].split('_')
        index = splitfile[0].upper()
        full_fig.update_layout(title_text='Mean and Standard Deviation ' + str(index) +  ' ASA-Testigo difference across all plots (every 10 days)', title_x=0.5)
        Y_axis_limit = stDev18["ATdiff"].max()+50
        Y_axis_min = stDev18["ATdiff"].min()-50        
        full_fig.add_trace(go.Bar(name="CR", x=["2017-01-01", "2018-01-01", "2019-01-01", "2020-01-01"], y=[800, 800, 800, 800], marker=dict(color=px.colors.qualitative.Antique[1]), opacity= 0.3, xperiod="M3", xperiodalignment="end", xhoverformat="Q%q", hovertemplate="crop residue visibility window"))
        full_fig.add_trace(go.Bar(name="CC", x=["2016-10-01", "2017-10-01", "2018-10-01", "2019-10-01"], y=[800, 800, 800, 800], marker=dict(color=px.colors.qualitative.Antique[6]), opacity= 0.3, xperiod="M3", xperiodalignment="end", xhoverformat="Q%q", hovertemplate="cover crop visibility window"))
        full_fig.show()
        
def AT_diff_SZN_barchart(input_csv):
    all_stats = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=False)
    VI_stats_count = all_stats.groupby(['AgYR', 'SZNwindow', 'Group'])['Group'].count().to_frame() # how many plots + days in each category
    VI_stats_count.columns = ["SZNcount"]
    VI_stats_count.reset_index(inplace=True)
    VI_stats_count.columns = ["AgYear", "Season", "avgATdiff", 'SZNcount']
    plot_list_count = all_stats.groupby([ 'AgYR', 'SZNwindow','Group'])['FieldID'].value_counts().to_frame() #.to_dict() #number of times a plot shows up in a seasonal window
    plot_list_count.columns = ['PLOTcount']
    plot_list_count.reset_index(inplace=True)
    plot_list_count.columns = ["AgYear", "Season", "avgATdiff", 'FieldID', 'PLOTcount']
    plot_list_count['FieldID'] = plot_list_count['FieldID'] # + str(plot_list_count['plotCOUNT'])
    VIdff_count_list = pd.merge(plot_list_count, VI_stats_count, on=(["AgYear", "Season", "avgATdiff"]))
    VIdff_count_list_CC_CR = VIdff_count_list[VIdff_count_list['Season'] != "main crop"]
    VIdff_count_list_CC_CR["Season"] = VIdff_count_list_CC_CR['AgYear'].astype(str) +"-"+ VIdff_count_list_CC_CR["Season"]
    VIdff_count_list_CC_CR = VIdff_count_list_CC_CR.iloc[: , 1:]
    splitpath = input_csv.split('/')
    splitfile = splitpath[-1].split('_')
    TITL = splitfile[0].upper() + " Avg seasonal ASA-Test plot differences (grouped relative to seasonal SD of all NI plots)"
    fig = px.bar(VIdff_count_list_CC_CR, x="Season", y="PLOTcount", title=TITL, hover_data=["FieldID","SZNcount"],  color="avgATdiff", color_discrete_sequence=[px.colors.diverging.RdYlBu[10],px.colors.diverging.RdYlBu[7], px.colors.diverging.RdYlBu[3], px.colors.diverging.RdYlBu[1]])
    fig.show()
    
def AT_diff_barchart(input_csv):
    all_stats = pd.read_csv(input_csv, header=0, index_col=0, parse_dates=False)
    VI_stats_count = all_stats.groupby(['AgYR', 'SZNwindow', 'Group'])['Group'].count().to_frame() # how many plots + days in each category
    VI_stats_count.columns = ["SZNcount"]
    VI_stats_count.reset_index(inplace=True)
    VI_stats_count.columns = ["AgYear", "Season", "ATdiff", 'SZNcount']
    plot_list_count = all_stats.groupby([ 'AgYR', 'SZNwindow','Group'])['FieldID'].value_counts().to_frame() #.to_dict() #number of times a plot shows up in a seasonal window
    plot_list_count.columns = ['PLOTcount']
    plot_list_count.reset_index(inplace=True)
    plot_list_count.columns = ["AgYear", "Season", "ATdiff", 'FieldID', 'PLOTcount']
    plot_list_count['FieldID'] = plot_list_count['FieldID'] # + str(plot_list_count['plotCOUNT'])
    VIdff_count_list = pd.merge(plot_list_count, VI_stats_count, on=(["AgYear", "Season", "ATdiff"]))
    VIdff_count_list_CC_CR = VIdff_count_list[VIdff_count_list['Season'] != "main crop"]
    VIdff_count_list_CC_CR["Season"] = VIdff_count_list_CC_CR['AgYear'].astype(str) +"-"+ VIdff_count_list_CC_CR["Season"]
    VIdff_count_list_CC_CR = VIdff_count_list_CC_CR.iloc[: , 1:]
    splitpath = input_csv.split('/')
    splitfile = splitpath[-1].split('_')
    TITL = splitfile[0].upper() + " ASA/Test plot differences (compared to 10-day mean & binned within CC/CR window)"
    fig = px.bar(VIdff_count_list_CC_CR, x="Season", y="PLOTcount", title=TITL, hover_data=["FieldID","PLOTcount","SZNcount"],  color="ATdiff", color_discrete_sequence=[px.colors.diverging.RdYlBu[10],px.colors.diverging.RdYlBu[7], px.colors.diverging.RdYlBu[3], px.colors.diverging.RdYlBu[1]])
    fig.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
### CLUSTER CODE

## export a list of unmasked images that intersect each plot point 
# read points. for each point, read L7 images and create list of images that intersect or contain each point         

def list_images(proj_path, grid_list, inputShape):
    plots_df = pd.DataFrame(columns=['InputFID', 'ProdID', 'Parcela', 'L7count' , 'L7images', 'L8count', 'L8images', 'S2count', 'S2images'])

    for grid in grid_list:    
        L7_img_list = []
        L8_img_list = []
        S2_img_list = []
        imagePath = proj_path + "raster/grids/" + grid + "/brdf/"
        for img in sorted(os.listdir(imagePath)):   
            if img.startswith('LE07') & img.endswith('_T1.nc'):
                L7_img_list.append(os.path.join(imagePath,img))
            if img.startswith('LC08') & img.endswith('_T1.nc'):
                L8_img_list.append(os.path.join(imagePath,img))            
            if img.startswith('L1C') & img.endswith('_MTD.nc'):
                S2_img_list.append(os.path.join(imagePath,img))   
        print('number of L7 images in grid', str(grid), ": " , len(L7_img_list))      
        print('number of L8 images in grid', str(grid), ": " , len(L8_img_list))
        print('number of S2 images in grid', str(grid), ": " , len(S2_img_list))
        
        strip_landsat_path = "netcdf:/raid-cel/sandbox" + proj_path[5:15] + proj_path[15:] + "raster/grids/" + grid + "/gee/"
        strip_sentinel_path = proj_path[:15] + proj_path[15:] + "raster/grids/" + grid + "/brdf/"   
        with fiona.open(inputShape) as shp:
            for feature in shp:
                if feature['properties']['UNQ'] == float(grid):
                    siteID = feature['properties']['Target_FID']
                    prodID = feature['properties']['oldIDPROD']
                    parcela = feature['properties']['Parcela']
                    coords = feature['geometry']['coordinates']
                    print('FID: ', str(int(siteID)), str(coords))
                    
                    L7_point_rast_dict = {}
                    for rast in L7_img_list:
                        with xr.open_dataset(rast) as xrimg:
                            point = xrimg.sel(x=coords[0], y=coords[1], method="nearest")
                            val = point['nir']
                            val_arr = val.data
                            L7_rast_dict={point.filename: val_arr}
                            L7_smaller_things = {key: value for key, value in L7_rast_dict.items() if value != 65535}
                        L7_point_rast_dict.update(L7_smaller_things)
                    new_L7_dict = {key.replace(strip_landsat_path, ""): value for key, value in L7_point_rast_dict.items()}
                    feature['properties']['L7'] = list(new_L7_dict.keys())
                    print(len(new_L7_dict), ' images with data from L7')
                    
                    L8_point_rast_dict = {}
                    for rast in L8_img_list:
                        with xr.open_dataset(rast) as xrimg:
                            point = xrimg.sel(x=coords[0], y=coords[1], method="nearest")
                            val = point['nir']
                            val_arr = val.data
                            L8_rast_dict={point.filename: val_arr}
                            L8_smaller_things = {key: value for key, value in L8_rast_dict.items() if value != 65535}
                        L8_point_rast_dict.update(L8_smaller_things)
                    new_L8_dict = {key.replace(strip_landsat_path, ""): value for key, value in L8_point_rast_dict.items()}
                    feature['properties']['L8'] = list(new_L8_dict.keys())
                    print(len(new_L8_dict), 'images with data from L8')
                    
                    S2_point_rast_dict = {}
                    for rast in S2_img_list:
                        with xr.open_dataset(rast) as xrimg:
                            point = xrimg.sel(x=coords[0], y=coords[1], method="nearest")
                            val = point['nir']
                            val_arr = val.data
                            S2_rast_dict={point.filename: val_arr}
                            S2_smaller_things = {key: value for key, value in S2_rast_dict.items() if value != 65535}
                        S2_point_rast_dict.update(S2_smaller_things)
                    new_S2_dict = {key.replace(strip_sentinel_path, ""): value for key, value in S2_point_rast_dict.items()}
                    feature['properties']['S2'] = list(new_S2_dict.keys())
                    print(len(new_S2_dict), 'images with data from S2')
                    
                    feature_list = [int(siteID), prodID, parcela, len(new_L7_dict), list(new_L7_dict.keys()), len(new_L8_dict), list(new_L8_dict.keys()), len(new_S2_dict), list(new_S2_dict.keys())]
                    plots_df.loc[len(plots_df)] = feature_list
                    
    out_path = inputShape[:-4] + "_image_list.csv"
    return plots_df.to_csv(out_path)



## stack ALL VIs in a folder. if return_csv is True - output points too 

## TO-DO:
## CRS check that reprojects polys to raster crs

def stack_extract(input_dir, out_name, inputShape, return_csv=True):
    
    rasList = []
    bandList = []
    
    for img in sorted(os.listdir(input_dir)):
        if img.endswith('.tif'):
            rasList.append(os.path.join(input_dir,img))
    print('number of images: ', len(rasList))
    band_paths=rasList
    # Read in metadata
    first_band = rio.open(band_paths[0], 'r')
    meta = first_band.meta.copy()
    # Replace metadata with new count and create a new file
    counts = 0
    for ifile in band_paths:
        with rio.open(ifile, 'r') as ff:
            counts += ff.meta['count']
    meta.update(count=counts)
    out_path = out_name + ".tif"
    with rio.open(out_path, 'w', **meta) as ff:
        for ii, ifile in tqdm(enumerate(band_paths)):
            bands = rio.open(ifile, 'r').read()
            if bands.ndim != 3:
                bands = bands[np.newaxis, ...]
            for band in bands:
                ff.descriptions = tuple([i[-11:-4] for i in band_paths])
                ff.write(band, ii+1)
            bandList.append(ff.descriptions)
            
    plots = []            
    multi_values_points = pd.Series()
    with fiona.open(inputShape) as shp:
        for feature in shp:
            siteID = feature['properties']['Target_FID']
            ProdID = feature['properties']['oldIDPROD']
            Parcela = feature['properties']['Parcela']
            coords = feature['geometry']['coordinates']
            # Read pixel value at the given coordinates using Rasterio
            # NB: `sample()` returns an iterable of ndarrays.
            with rio.open(out_path) as stack_src:            
                value = [v for v in stack_src.sample([coords])] 
            # Update the pandas series accordingly
            multi_values_points.loc[siteID] = value
            plots.append(int(siteID))
            plots.append(ProdID)
            plots.append(Parcela)
            
    plots_arr = np.array(plots)
    plots_arr_reshape = plots_arr.reshape(int(plots_arr.shape[0]/3), -1)
    plots_df = pd.DataFrame(plots_arr_reshape, columns = ['FID','FieldID','Parcela'])
    df1 = pd.DataFrame(multi_values_points.values, index=multi_values_points.index)
    df1.columns = ['Val']
    df2 = pd.DataFrame(df1['Val'].explode())
    extracted_vals = pd.DataFrame(df2["Val"].to_list())
    extracted_vals.columns = bandList[0]
    extracted_vals['FID'] = np.arange(len(extracted_vals)).astype(str)
    extracted_plots = pd.merge(plots_df, extracted_vals, how = 'outer', on='FID')
    extracted_plots =  extracted_plots.set_index("FID")
    single_grid_vals = extracted_plots[~(extracted_plots.T == 0).any()]
    #print(single_grid_vals) # print if nothing is outputting, export as wide format
    ## REFORMAT
    df2 = single_grid_vals.set_index(["FieldID", "Parcela"])
    df2_T = df2.T
    df3 = df2_T.reset_index(level=0)
    df3["Julian"] = df3["index"].str.slice(start=0, stop=9).astype(str)
    df3["Date"] = pd.to_datetime(df3['Julian'], format='%Y%j')
    df4 = df3.set_index('Date')
    df5 = df4.drop(['index', 'Julian'], axis=1)
    df5 =  df5.reset_index(level=0) 
    df5_melt = pd.melt(df5, id_vars='Date')
    df5_melt.rename(columns = {'Date':'Date', 'ProdID': 'Code', 'Parcela': 'Parcela', 'value': 'Value'}, inplace=True)
    #print(df5_melt.to_string())

    if return_csv is True:
        out_csv_path = out_name + ".csv"
        print('exporting csv: ' + out_csv_path)
        return df5_melt.to_csv(out_csv_path)
    else:
        return('no csv for ' + out_csv_path)
