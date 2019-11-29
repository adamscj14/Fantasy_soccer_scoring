#!/usr/bin/Python

# Created by: Christopher J Adams 8/27/2019
#

###############################################################################
###
### This script updates the standings given a new cutoff file and new results 
###
###############################################################################

import sys
import getopt
import pandas as pd
import numpy as np
import json


def help(exit_num=1):
    print """-----------------------------------------------------------------
ARGUMENTS
    -f <csv>             REQUIRED: comma-delimited current fantasy results file with 
                                   new scores to 
                                   FORMAT: team_1 , score_1 , team_2 , score_2
    -s <json>            REQUIRED: standings json
    -c <file>            REQUIRED: return-delimited list of cutoff values in order
    -o <file>            OPTIONAL: output file name, if none, overwrite standings file
    -r <file>            REQUIRED: results file to append to
    -w <int>             OPTIONAL: number of game weeks to consider from results file

"""
    sys.exit(exit_num)


## MAIN ##

def main(argv): 
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "f:o:c:r:s:w:")
    except getopt.GetoptError:
        print "Error: Incorrect usage of getopts flags!"
        help() 

    fantasy_results_file = False
    output_file = False
    cutoff_file = False
    results_file = False
    standings_file = False
    weeks = 1

    for opt, arg in opts:
        print opt,arg

        if opt == "-f":
            fantasy_results_file = arg
        
        elif opt == "-c":
            cutoff_file = arg

        elif opt == "-o":
            output_file = arg
        
        elif opt == "-r":
            results_file = arg

        elif opt == "-s":
            standings_file = arg

        elif opt == "-w":
            weeks = int(arg)

        else:
            print "Error: Incorrect usage of getopts flags!"
            help()


    ## check arguments
    if not (fantasy_results_file and standings_file and cutoff_file and results_file):
        print "Error: At least one of the required inputs is missing."
        help()

    driver(fantasy_results_file, output_file, cutoff_file, results_file, standings_file, weeks)


def driver(fantasy_results_file, output_file, cutoff_file, results_file, standings_file, weeks):
    
    fantasy_results_df = pd.read_csv(fantasy_results_file, names = ['team_1', 'pts_1', 'team_2', 'pts_2'])
    cutoff_list = parse_cutoff_file(cutoff_file)
    
    with open(standings_file, 'r') as standings_json:
        standings_dict = json.load(standings_json)

    new_standings_dict = get_standings_dict(fantasy_results_df, cutoff_list, results_file, standings_dict, weeks)

    if not output_file:
        output_file = standings_file

    with open(output_file, 'w') as out_file:
        json.dump(standings_dict, out_file)


def get_standings_dict(fantasy_results_df, cutoff_list, results_file, standings_dict, weeks):
    # prep data structures to hold relevant score data
    team_dict = standings_dict
    tie_count = 0
    non_tie = 0
    
    results = open(results_file, 'a')

    total_goals = []
    num_games = len(fantasy_results_df.index)
    num_games_of_interest = int(weeks) * 5
    ignore_games = num_games - num_games_of_interest
    # cycle through games to find results
    game_count = 0
    for ind, row in fantasy_results_df.iterrows():
        game_count += 1
        if game_count <= ignore_games:
            continue
        team_1_goals = find_goals(cutoff_list, row.pts_1)
        team_2_goals = find_goals(cutoff_list, row.pts_2)
        team_1_fp = row.pts_1
        team_2_fp = row.pts_2
        total_goals.append(team_1_goals)
        total_goals.append(team_2_goals)
        
        team_dict[str(int(row.team_1))][4] += team_1_goals
        team_dict[str(int(row.team_1))][5] += team_2_goals
        team_dict[str(int(row.team_1))][6] += (team_1_goals - team_2_goals)
        
        team_dict[str(int(row.team_2))][4] += team_2_goals
        team_dict[str(int(row.team_2))][5] += team_1_goals
        team_dict[str(int(row.team_2))][6] += (team_2_goals - team_1_goals)
        
        # tie
        if team_1_goals == team_2_goals:
            
            tie_count += 1
            team_dict[str(int(row.team_1))][0] += 1
            team_dict[str(int(row.team_1))][2] += 1
            team_dict[str(int(row.team_2))][0] += 1
            team_dict[str(int(row.team_2))][2] += 1
        # team 1 win
        elif team_1_goals > team_2_goals:
            non_tie += 1
            team_dict[str(int(row.team_1))][0] += 3
            team_dict[str(int(row.team_1))][1] += 1
            team_dict[str(int(row.team_2))][3] += 1
        # team 2 win
        elif team_1_goals < team_2_goals:
            non_tie += 1
            team_dict[str(int(row.team_2))][0] += 3
            team_dict[str(int(row.team_2))][1] += 1
            team_dict[str(int(row.team_1))][3] += 1
        #prstr(int team_dict
        results.write("{}\t{}\t{}-{}\t{}\t{}\n".format(int(row.team_1), float(team_1_fp), team_1_goals, team_2_goals, float(team_2_fp), int(row.team_2)))
    print "avg fantasy goals: {}".format(np.mean(total_goals))

    results.close()
    return team_dict

def find_goals(cutoff_list, points):
    goals = 0
    for cutoff in cutoff_list:
        if points >= cutoff:
            goals += 1
        else:
            return goals
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
