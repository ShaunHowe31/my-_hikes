#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:34:50 2021

@author: shaunhowe
"""


import os
import yaml
import glob
import gpxpy
import shutil


def create_activity_dirs(activities, act_dir):
    '''
    Function to create activity directories
    '''
    for act in activities:
        new_dir =  os.path.join(act_dir, activities[act])
        if new_dir == False:
            os.mkdir(new_dir)
            print(new_dir + ' made')
        else:
            print(new_dir + ' already exists')
    

def get_strava_category(gpxx_file, strava_cats_df):
    '''
    Function for getting the Strava Category (activity) type
    from the GPX file
    '''
    activity_name = None
    
    gpx = gpxpy.parse(open(gpx_file))

    activity_type = gpx.tracks[0].type

    ## loop through Strava category dictionary to find the activity type
    for tpe in strava_cats_df:
        if tpe is int(activity_type):
            activity_name = strava_cats_df[tpe]
            
    if activity_name == None:
        print(activity_type + ' not in strava activity YML')
        
    return activity_name
            
def sort_strava_gpx(gpx_activity, act_dir, gpx_file):
    '''
    Sort Strava GPX files by activity type
    '''
    gpx_fn = os.path.basename(gpx_file)
    
    if gpx_activity != None:
        new_dir = os.path.join(act_dir, gpx_activity)
        if os.path.exists(new_dir) == True:
            new_fp = os.path.join(new_dir, gpx_fn)
            shutil.move(gpx_file, new_fp)
            
            print(new_fp +' moved')
    
    
if __name__ == '__main__':
    category_fn = r'/Users/shaunhowe/Documents/geospat/my_hikes/strava_categories.yml'

    ## Open strava categories YML to create dictionary
    with open(category_fn) as file:
        strava_cats = yaml.load(file, Loader=yaml.FullLoader)
        strava_cats = strava_cats['strava_activity_categories']

    act_dir = r'/Users/shaunhowe/Documents/GPS/Strava/activities'
    
    create_activity_dirs(strava_cats, act_dir)
    
    gpx_files = glob.glob(r'/Users/shaunhowe/Documents/GPS/Strava/Activities/*.gpx')

    ## loop through GPX files
    for gpx_file in gpx_files:
        
        activity = get_strava_category(gpx_file, strava_cats)
        
        sort_strava_gpx(activity, act_dir, gpx_file)