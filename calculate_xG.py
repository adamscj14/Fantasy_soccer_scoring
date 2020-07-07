#!/usr/bin/Python

# Created by: Christopher J Adams 12/31/2019
#

###############################################################################
###
### This script generates the xG results for each team
###
###############################################################################

import sys
import getopt
import pandas as pd
import numpy as np
import json


def help(exit_num=1):
    print ("""-----------------------------------------------------------------
ARGUMENTS
    -f <csv>             REQUIRED: comma-delimited current fantasy results file 
                                   FORMAT: team_1 , score_1 , team_2 , score_2
    -c <file>            REQUIRED: return-delimited list of cutoff values in order
    -o <file>            REQUIRED: output file name for xG results

""")
    sys.exit(exit_num)


## MAIN ##

def main(argv): 
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "f:o:c:n:")
    except getopt.GetoptError:
        print("Error: Incorrect usage of getopts flags!")
        help() 

    fantasy_results_file = False
    output_file = False
    cutoff_file = False

    for opt, arg in opts:
        print opt,arg

        if opt == "-f":
            fantasy_results_file = arg
        
        elif opt == "-c":
            cutoff_file = arg

        elif opt == "-o":
            output_file = arg

        elif opt == '-n':
            name_file = arg

        else:
            print("Error: Incorrect usage of getopts flags!")
            help()


    ## check arguments
    if not (fantasy_results_file and output_file and cutoff_file and name_file):
        print("Error: At least one of the required inputs is missing.")
        help()

    driver(fantasy_results_file, output_file, cutoff_file, name_file)


def driver(fantasy_results_file, output_file, cutoff_file, name_file):

    fantasy_results = open(fantasy_results_file, 'r')
    
    cutoff_list = parse_cutoff_file(cutoff_file)
    
    xg_dict = get_xg_dict(fantasy_results, cutoff_list)
    '''
    with open(output_file, 'w') as out_file:
        json.dump(standings_dict, out_file)
    '''
    name_conversion_dict = parse_name_file(name_file)
    print name_conversion_dict
    for team in xg_dict:
        team_name = name_conversion_dict[int(team)]
        print"{} -- {}".format(team_name, xg_dict[team])


def parse_name_file(name_file):
    
    name_conversion_dict = {}

    with open(name_file, 'r') as name_conversions:
        for line in name_conversions:
            line_list = line.strip().split(',')
            name_conversion_dict[int(line_list[0])] = line_list[1]

    return name_conversion_dict


def get_xg_dict(fantasy_results, cutoff_list):
    # prep data structures to hold relevant score data
    team_dict = {}
    tie_count = 0
    non_tie = 0
    
    total_goals = []
    # cycle through games to find results
    for line in fantasy_results:
        if line.startswith('Team'):
            continue
        line = line.strip().split('\t')
        #print line
        
        team_1_id = line[0]
        team_1_pts = float(line[1])
        team_1_xg = find_goal_xg(cutoff_list, team_1_pts) - 0.6
        try:
            team_dict[team_1_id] += team_1_xg
        except KeyError:
            team_dict[team_1_id] = team_1_xg

        team_2_id = line[4]
        team_2_pts = float(line[3])
        team_2_xg = find_goal_xg(cutoff_list, team_2_pts) - 0.6
        try:
            team_dict[team_2_id] += team_2_xg 
        except KeyError:
            team_dict[team_2_id] = team_2_xg
        '''
        if team_1_id == '1':
            print team_1_pts
            print team_1_xg
            print team_dict[team_1_id]
            print '---------'
           
        if team_2_id == '1':
            print team_2_pts
            print team_2_xg
            print team_dict[team_2_id]
            print '---------'
        '''

    return team_dict

def find_goal_xg(cutoff_list, points):
    goals = 0
    prev_cutoff = 0
    for cutoff in cutoff_list:
        #print cutoff
        if points >= cutoff:
            prev_cutoff = cutoff
            goals += 1
        else:
            total_interval = cutoff - prev_cutoff
            fraction = (points - prev_cutoff) / total_interval
            goals += fraction
            #print goals
            #print points
            break

    return goals


# get the cutoffs
def parse_cutoff_file(cutoff_file):
    cutoff_list = []
    cutoff_file = open(cutoff_file, 'r')

    for cutoff in cutoff_file:
        cutoff_list.append(float(cutoff))
    
    return cutoff_list


if __name__ == "__main__":
    main(sys.argv[1:])
