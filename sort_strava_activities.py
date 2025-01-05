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

def determine_strava_gpx(initial_gpx):
    '''
    Determine if strava GPX files store activity type using the new (string) 
    or old (number category) method
    '''
    
    initial_act = initial_gpx.tracks[0].type
    
    if isinstance(initial_act, str):
        act_stor = 'new'
    elif isinstance(initial_act, int):
        act_stor = 'old'
        
    ## Open strava categories YML to create dictionary
    with open(category_fn) as file:
        strava_cats = yaml.load(file, Loader=yaml.FullLoader)
        strava_cats = strava_cats[act_stor]['strava_activity_categories']
        
    return act_stor, strava_cats

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
    

def get_strava_category(gpx_file, activity_storage, strava_cats_df):
    '''
    Function for getting the Strava Category (activity) type
    from the GPX file
    '''
    
    activity_name = None
    
    gpx = gpxpy.parse(open(gpx_file))

    activity_type = gpx.tracks[0].type

    if activity_storage == 'new':
        activity_name = activity_type
    
    elif activity_storage == 'old':
        ## loop through Strava category dictionary to find the activity type
        for tpe in strava_cats_df:
            if tpe is int(activity_type):
                activity_name = strava_cats_df[tpe]

        if activity_name == None:
            print(activity_type + ' not in strava activity YML')
        
    return activity_name

            
def sort_strava_gpx(gpx_activity, new_dir, gpx_file):
    '''
    Sort Strava GPX files by activity type
    '''
    
    gpx_fn = os.path.basename(gpx_file)
    
    if gpx_activity != None:
        new_dir_final = os.path.join(new_dir, gpx_activity)
        if os.path.exists(new_dir) == True:
            new_fp = os.path.join(new_dir_final, gpx_fn)
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
    
    orig_dir    = '/path/to/original/dir'
    act_dir     = rf'{orig_dir}/Activities'
    new_dir     = r'/path/to/new/dir'
    category_fn = r'./strava_categories.yml'
    
    ## Find out which strava activity type we are dealing with
    gpx_files   = glob.glob(rf'{act_dir}/*.gpx')
    initial_gpx = gpxpy.parse(open(gpx_files[0]))
    
    activity_storage, strava_cats = determine_strava_gpx(initial_gpx)
    
    ## Create activity directories
    create_activity_dirs(strava_cats, new_dir)

    ## Loop through GPX files
    for gpx_file in gpx_files:
        
        activity = get_strava_category(gpx_file, activity_storage, strava_cats)
        
        sort_strava_gpx(activity, new_dir, gpx_file)

    ## Combine activities
    combine_activities(orig_dir, new_dir)