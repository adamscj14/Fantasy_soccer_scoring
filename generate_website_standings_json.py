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
    -n <csv>              OPTIONAL: comma-delimited conversion of team number to name
                                    FORMAT: Number,Name
    -o <json>             REQUIRED: name of output file
"""
    sys.exit(exit_num)


## MAIN ##

def main(argv): 
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "s:n:o:")
    except getopt.GetoptError:
        print "Error: Incorrect usage of getopts flags!"
        help() 

    standings_file = False
    name_file = False
    output_file = False

    for opt, arg in opts:
        print opt,arg

        if opt == "-s":
            standings_file = arg

        elif opt == "-n":
            name_file = arg
        
        elif opt == "-o":
            output_file = arg

        else:
            print "Error: Incorrect usage of getopts flags!"
            help()


    ## check arguments
    if not (standings_file and output_file):
        print "Error: At least one of the required inputs is missing."
        help()

    driver(standings_file, name_file, output_file)


def driver(standings_file, name_file, output_file):
    
    with open(standings_file, 'r') as s_j:
        standings_dict = json.load(s_j)

    if name_file:
        name_conversion_dict = parse_name_file(name_file)
        print name_conversion_dict

    standings_list = []
    for team_num in standings_dict:
        new_list = [team_num]
        if name_file:
            team_name = name_conversion_dict[int(team_num)]
            new_list = [team_name]
        new_list += standings_dict[team_num]
        standings_list.append(new_list)

    standings_columns = ["Team", "Points", "Wins", "Draws", "Losses", "Goals For", "Goals Against", "Goal Difference"]
    standings_df = pd.DataFrame(standings_list, columns = standings_columns)
    standings_df.sort_values(by=["Points", "Goals For","Goals Against"], ascending = False, inplace = True)
    
    standings_list = create_standings_list(standings_df)
    
    with open(output_file, 'w') as out_file:
        json.dump(standings_list, out_file)


def create_standings_list(standings_df):
    
    standings_list = []

    for index, row in standings_df.iterrows():
        row_dict = {"teamName": row["Team"],
                    "points": row["Points"],
                    "wins": row["Wins"],
                    "draws": row["Draws"],
                    "losses": row["Losses"],
                    "gf": row["Goals For"],
                    "ga": row["Goals Against"],
                    "gd": row["Goal Difference"]
                    }
        
        standings_list.append(row_dict)

    return standings_list

def parse_name_file(name_file):
    
    name_conversion_dict = {}

    with open(name_file, 'r') as name_conversions:
        for line in name_conversions:
            line_list = line.strip().split(',')
            name_conversion_dict[int(line_list[0])] = line_list[1]

    return name_conversion_dict



if __name__ == "__main__":
    main(sys.argv[1:])
