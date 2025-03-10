import psutil

def searchForPendrive():
        pendrives = []
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts.lower():
                pendrives.append(partition.device)
        return pendrives