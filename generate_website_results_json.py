#!/usr/bin/Python

# Created by: Christopher J Adams 8/27/2019
#

###############################################################################
###
### This script generates the standings given a cutoff file and the results 
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
    -r <tsv>             REQUIRED: tsv of results
    -n <csv>             REQUIRED: comma-delimited conversion of team number to name
                                   FORMAT: Number,Name
    -o <json>            REQUIRED: output file name for website formatted json results
"""
    sys.exit(exit_num)


## MAIN ##

def main(argv): 
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "r:n:o:")
    except getopt.GetoptError:
        print "Error: Incorrect usage of getopts flags!"
        help() 
    
    output_file = False
    results_file = False
    name_file = False

    for opt, arg in opts:
        print opt,arg

        if opt == "-n":
            name_file = arg

        elif opt == "-o":
            output_file = arg

        elif opt == "-r":
            results_file = arg

        else:
            print "Error: Incorrect usage of getopts flags!"
            help()


    ## check arguments
    if not (output_file and name_file and results_file):
        print "Error: At least one of the required inputs is missing."
        help()

    driver(output_file, name_file, results_file)


def driver(output_file, name_file, results_file):

    name_conversion_dict = parse_name_file(name_file)

    output_dict = {}
    count = -1
    game_week = 0
    with open(results_file, 'r') as results:
        
        for line in results:
            if count == -1:
                count += 1
                continue
            if count % 5 == 0:
                game_week += 1
                output_dict[game_week] = []
            line_list = line.strip().split('\t')
            team_1 = name_conversion_dict[int(line_list[0])]
            team_2 = name_conversion_dict[int(line_list[4])]
            
            output_dict[game_week].append({"homeTeam": team_1,
                                           "awayTeam": team_2, 
                                           "homePoints": line_list[1], 
                                           "awayPoints": line_list[3],
                                            "convertedResult": line_list[2]
                                           })
            count += 1

    with open(output_file, 'w') as out_file:
        json.dump(output_dict, out_file)


def parse_name_file(name_file):

    name_conversion_dict = {}
 
    with open(name_file, 'r') as name_conversions:
        for line in name_conversions:
            line_list = line.strip().split(',')
            name_conversion_dict[int(line_list[0])] = line_list[1]
 
    return name_conversion_dict


if __name__ == "__main__":
    main(sys.argv[1:])
