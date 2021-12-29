#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:34:50 2021

@author: shaunhowe
"""

import yaml
import gpxpy


def get_strava_category(gpxx_file, strava_cats_df):
    '''
    '''
    activity_name = None
    
    gpx = gpxpy.parse(open(gpx_file))

    activity_type = gpx.tracks[0].type

    for tpe in strava_cats_df:
        if tpe is int(activity_type):
            activity_name = strava_cats_df[tpe]
            
    if activity_name == None:
        print(activity_type + ' not in strava activity YML')
        
    return activity_type
            
    
if __name__ == '__main__':
    category_fn = r'/Users/shaunhowe/Documents/GPS/Strava/strava_categories.yml'

    ## Open strava categories
    with open(category_fn) as file:
        strava_cats = yaml.load(file, Loader=yaml.FullLoader)
        strava_cats = strava_cats['strava_activity_categories']


    gpx_file = r'/Users/shaunhowe/Documents/GPS/Strava/Activities/6371954871.gpx'


    activity = get_strava_category(gpx_file, strava_cats)
