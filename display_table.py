#!/usr/bin/Python

# Created by: Christopher J Adams 8/27/2019
#

###############################################################################
###
### This script displays the standings 
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
    -s <json>             REQUIRED: json of dictionary holding standings information 
                                   (Output from generate_base_table.py)
"""
    sys.exit(exit_num)


## MAIN ##

def main(argv): 
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "s:")
    except getopt.GetoptError:
        print "Error: Incorrect usage of getopts flags!"
        help() 

    standings_file = False

    for opt, arg in opts:
        print opt,arg

        if opt == "-s":
            standings_file = arg
        
        else:
            print "Error: Incorrect usage of getopts flags!"
            help()


    ## check arguments
    if not standings_file:
        print "Error: At least one of the required inputs is missing."
        help()

    driver(standings_file)


def driver(standings_file):
    
    with open(standings_file, 'r') as s_j:
        standings_dict = json.load(s_j)


    standings_list = []
    for team in standings_dict:
        new_list = [team]
        new_list += standings_dict[team]
        standings_list.append(new_list)

    standings_columns = ["Team", "Points", "Wins", "Draws", "Losses", "Goals For", "Goals Against", "Goal Difference"]
    standings_df = pd.DataFrame(standings_list, columns = standings_columns)
    standings_df.sort_values(by=["Points", "Goals For","Goal Difference"], ascending = False, inplace = True)
    print standings_df


if __name__ == "__main__":
    main(sys.argv[1:])
