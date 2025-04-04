##
#@file commonFunctions.py
#@brief Provides common functions used across the project.
#
#This module provides various common functions used across the project.
#
import psutil
import os

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


##
#@brief Searches for a file containing the user's private key on mounted pendrives and reads its contents.
#
#@param pendrives List of mounted pendrives.
#@param filePath Relative path to the file containing the user's private key.
#
#@return Returns the private key as bytes if the file was found and successfully read. On the other hand, returns the string "Not found" if no file has been found. 
#
def searchAndReadPrivateKey(pendrives, filePath):
        for pendrive in pendrives:

            fullFilePath = os.path.join(pendrive, filePath)
            if os.path.exists(fullFilePath):
                try:
                    with open(fullFilePath, 'rb') as f:
                        privateKey = f.read()
                        return privateKey
                except Exception as e:
                    print(f"Error during opening the file: {e}")
                    return "Not found"
                                
        return "Not found" 