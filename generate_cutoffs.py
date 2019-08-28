#!/usr/bin/Python

# Created by: Christopher J Adams 8/27/2019
#

###############################################################################
###
### This script generates the cutoffs to be used for a given league
###
###############################################################################

import sys
import getopt
import pandas as pd
import numpy as np

def help(exit_num=1):
    print """-----------------------------------------------------------------
ARGUMENTS
    -g <csv>             REQUIRED: comma-delimited file of game results
                                      FORMAT: score_1 : score_2 , score_1 , score_2
    -f <csv>             REQUIRED: comma-delimited file of fantasy score results
                                      FORMAT: team_1 , score_1 , team_2 , score_2
    -c <csv>             OPTIONAL: comma-delimited current fantasy results file with 
                                      additional scores to use to calculate cutoffs
                                      FORMAT: team_1 , score_1 , team_2 , score_2
    -o <file>            REQUIRED: output file name

"""
    sys.exit(exit_num)


## MAIN ##

def main(argv): 
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "g:f:c:o:")
    except getopt.GetoptError:
        print "Error: Incorrect usage of getopts flags!"
        help() 

    game_results_file = False
    base_fantasy_results_file = False
    current_fantasy_results_file = False
    output_file = False

    for opt, arg in opts:
        print opt,arg

        if opt == "-g":  
            game_results_file = arg

        elif opt == "-f":
            base_fantasy_results_file = arg

        elif opt == "-c":
            current_fantasy_results_file = arg
        
        elif opt == "-o":
            output_file = arg

        else:
            print "Error: Incorrect usage of getopts flags!"
            help()


    ## check arguments
    if not (game_results_file and base_fantasy_results_file and output_file):
        print "Error: At least one of the required inputs is missing."
        help()

    driver(game_results_file, base_fantasy_results_file, current_fantasy_results_file, output_file)

def driver(game_results_file, base_fantasy_results_file, current_fantasy_results_file, output_file):
    
    game_results_df = pd.read_csv(game_results_file, names = ['score', 'goal_home', 'goal_away'])

    base_fantasy_results_df = pd.read_csv(base_fantasy_results_file, names = ['team_1', 'pts_1', 'team_2', 'pts_2'])

    # get total points list
    total_pts_list = np.sort(list(base_fantasy_results_df['pts_1'])+list(base_fantasy_results_df['pts_2']))
    
    if current_fantasy_results_file:
        current_results_df = pd.read_csv(base_fantasy_results_file, names = ['team_1', 'pts_1', 'team_2', 'pts_2'])
        updated_pts_list = np.sort(list(current_results_df['pts_1'])+list(current_results_df['pts_2']))
        total_pts_list = np.sort(list(updated_pts_list) + list(total_pts_list))
    

    # get total goals list
    total_goals_list = np.sort(list(game_results_df['goal_home'])+list(game_results_df['goal_away']))

    cutoff_list = get_cutoffs(total_goals_list, total_pts_list)

    output = open(output_file, 'w')
    for cutoff in cutoff_list:
        output.write(str(cutoff)+'\n')


# get the cutoffs
def get_cutoffs(total_goals_list, total_pts_list):
    cutoff_list = []
    for goal_total in [0,1,2,3,4,5,6,7]:
        num_threshold_reached = float(np.array(np.where(total_goals_list <= goal_total)).shape[1])
        percent = num_threshold_reached / float(len(total_goals_list))
        cutoff_ind = int(percent * len(total_pts_list))
        cutoff_score = total_pts_list[cutoff_ind - 1]
        print "Need {} pts for {} goal(s)".format(cutoff_score, goal_total + 1)
        cutoff_list.append(cutoff_score)
    return cutoff_list


if __name__ == "__main__":
    main(sys.argv[1:])
