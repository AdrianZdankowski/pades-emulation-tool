import psutil
import os

def searchForPendrive():
        pendrives = []
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts.lower():
                pendrives.append(partition.device)
        return pendrives

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