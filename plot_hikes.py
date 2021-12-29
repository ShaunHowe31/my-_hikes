#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 21:39:58 2021

@author: shaunhowe
"""

import gpxpy
import folium
import pandas as pd


def process_gpx_to_df(file_name):
    '''
    '''
    gpx = gpxpy.parse(open(file_name))
 
    #(1)make DataFrame
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude,point.elevation,
                     point.time, segment.get_speed(point_idx)])
    
    
    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    gpx_df = pd.DataFrame(data, columns=columns)
 
    #2(make points tuple for line)
    points = []
    for track in gpx.tracks:
        for segment in track.segments: 
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
 
    return gpx_df, points

def create_map(df):
    '''
    '''
    mymap = folium.Map( location=[df.Latitude.mean(), df.Longitude.mean() ], zoom_start=6, tiles=None)
    folium.TileLayer('openstreetmap', name='OpenStreet Map').add_to(mymap)
    
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, iPC', name='Nat Geo Map').add_to(mymap)
    folium.TileLayer('http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg', attr='terrain-bcg', name='Terrain Ma').add_to(mymap)
    
    return mymap
    
def plot_on_map(points, map_name):
    '''
    '''
    folium.PolyLine(points, color='cyan', weight=4.5, opacity=.5).add_to(mymap)
    mymap.save(map_name)

if __name__ == '__main__':

    gpx_file = r'/Users/shaunhowe/Documents/GPS/GPS_actual_2020-11-04/Track_2020-11-04 140102.gpx'

    df, points = process_gpx_to_df(gpx_file)

    mymap = create_map(df)
    
    plot_on_map(points, 'mymap.html')
