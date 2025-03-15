##
#@file commonFunctions.py
#@brief Provides common functions used across the project.
#
#This module provides various common functions used across the project.
#
import psutil
##
#@brief Searches for paths of the connected pendrives.
#
#@return List of connected pendrive paths. Returns empty list if no connected pendrive has been found.
#
def searchForPendrive():
        pendrives = []
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts.lower():
                pendrives.append(partition.device)
        return pendrives