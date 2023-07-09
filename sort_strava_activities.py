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
        if os.path.exists(new_dir) == False:
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
            
            print('Moving: ', new_fp)
            
            
def combine_activities(strava_dir, new_dir):
    '''
    Function for comparing Strava GPX files in two directories
    '''

    ## Get activity directory file paths
    orig_dir_paths = glob.glob(f'{strava_dir}/*/', recursive = True)
    new_dir_paths = glob.glob(f'{new_dir}/*/', recursive = True)
    
    ## Get activity directory names
    orig_dirs = [os.path.basename(os.path.dirname(odir)) for odir in orig_dir_paths]
    new_dirs = [os.path.basename(os.path.dirname(ndir)) for ndir in new_dir_paths]
    
    ## Loop through activity directories
    for i in range(len(new_dir_paths)):
        orig_activity_dir = os.path.join(strava_dir, new_dirs[i])
        
        ## Continue if activity directory exists in Strava Master
        if os.path.exists(orig_activity_dir) == True:
            print('Looking through ', new_dirs[i])
            
            gpx_files = glob.glob(os.path.join(new_dir_paths[i], '*.gpx'))
            
            ## Loop through GPX files in new directory
            for file in gpx_files:
                new_gpx_filename = os.path.basename(file)

                orig_files = glob.glob(os.path.join(orig_activity_dir, '*.gpx'))
                orig_file_list = [os.path.basename(gpfile) for gpfile in orig_files]
                
                ## If GPX file from new directory isn't in Strava master then move it
                if new_gpx_filename not in orig_file_list:
                    print('Moving ', new_gpx_filename)
                    
                    shutil.move(file, os.path.join(orig_activity_dir, new_gpx_filename))

    
    
if __name__ == '__main__':
    category_fn = r'./strava_categories.yml'

    ## Open strava categories YML to create dictionary
    with open(category_fn) as file:
        strava_cats = yaml.load(file, Loader=yaml.FullLoader)
        strava_cats = strava_cats['strava_activity_categories']

    act_dir = r'/path/to/new/directory'
    
    
    create_activity_dirs(strava_cats, act_dir)
    
    gpx_files = glob.glob(rf'{act_dir}/*.gpx')

    ## loop through GPX files
    for gpx_file in gpx_files:
        
        activity = get_strava_category(gpx_file, strava_cats)
        
        sort_strava_gpx(activity, act_dir, gpx_file)
        
    
    orig_strava_dir = r'/path/to/orig/direcotry'
    
    combine_activities(orig_strava_dir, act_dir) 