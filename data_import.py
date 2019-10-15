import csv
import sys
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import numpy as np


class ImportData:
    '''
    Class for importing and parsing data for time series
    '''

    def __init__(self, data_csv):
        '''
        Class constructor, read value and time from input file
        '''
        self._time = []
        self._value = []

        # Use a handle to determine how to summarize duplicated values
        # Default set to 0 meaning sum the duplicated
        self._dedup = 0
        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._dedup = 0
        elif 'hr' in data_csv or 'smbg' in data_csv or 'cgm' in data_csv or \
            'basal' in data_csv:
            self._dedup = 1

        # open file, create a reader from csv.DictReader, and read input times and values
        with open(data_csv, 'r') as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                if 'time' not in row.keys() or 'value' not in row.keys():
                    raise ValueError('Input data needs contain time and values')
                if (row['time'] == ''):
                    continue


                try:
                    if row['value'] == 'low':
                        row['value'] = 40.0
                    elif row['value'] == 'high':
                        row['value'] = 300.0

                    val = float(row['value'])

                    if val is not None:
                        self._time.append(dateutil.parser.parse(row['time']))
                        self._value.append(val)
                except ValueError:
                    print('Skipping value' + row['value'])

            fhandle.close()


    def linear_search_value(self, key_time):
        '''
        Linear search to find key in the self._time vector
        '''
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        out_list = []
        for i in range(len(self._time)):
            if self._time[i] == key_time:
                out_list.append(self._value[i])
        if len(out_list) == 0:
            print('The specified time key is not found.')
            return(-1)
        else:
            return(out_list)

    def binary_search_value(self,key_time):
        pass
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

def roundTimeArray(obj, res):
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    time_lst = []
    vals = []
    num_times = len(obj._time)
    type = obj._dedup
    for i in range(num_times):
        time = obj._time[i]
        bad = datetime.timedelta(minutes=time.minute % res,
                                 seconds=time.second)
        time -= bad
        if (bad >= datetime.timedelta(minutes=math.ceil(res/2))):
            time += datetime.timedelta(minutes=res)
        obj._time[i] = time

    if num_times > 0:
        time_lst.append(obj._time[0])
        sch = obj.linear_search_value(obj._time[0])  # search
        if type == 0:
            vals.append(sum(sch))  # summed
        elif type == 1:
            vals.append(sum(sch)/len(sch))  # averaged

    for i in range(1, num_times):  # check for duplicates
        if obj._time[i] == obj._time[i - 1]:
            continue
        else:
            time_lst.append(obj._time[i])
            sch = obj.linear_search_value(obj._time[i])
            if type == 0:
                vals.append(sum(sch))  # summed
            elif type == 1:
                vals.append(sum(sch)/len(sch))  # averaged
    output = zip(time_lst, vals)
    return output



def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    key_list = []
    out = []
    annotation = []

    if key_file not in annotation_list:
        raise ValueError("Key_file not found!")
    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                key_list.append(data_list[i])
            else:
                annotation.append(annotation_list[i])
                out.append(data_list[i])

    with open(base_name+'.csv', mode='w') as output:
        writer = csv.writer(output, delimiter=',')
        writer.writerow(['time', key_file] + annotation)
        for (time, val) in key_list[0]:
            old = []
            for data in out:
                start_length = len(old)
                for (timex, valsx) in data:
                    if time == timex:
                        old.append(valsx)
                if len(old) == start_length:
                    old.append(0)
            writer.writerow([time, val] + old)
    return(0)

if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('output_file', type=str, help = 'Name of Output file')

    parser.add_argument('sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()

    #pull all the folders in the file
    folder_path = args.folder_name
    try:
        # append file list while checking to see if file exists
        files_lst = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    except FileNotFoundError:
        print('Specified input folder not found.')
        sys.exit(1)

    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for files in files_lst:
        data_lst.append[ImportData(folder_path + files)]

    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min
    for i in data_lst:
        data_5.append(roundTimeArray(i, 5))
        data_15.append(roundTimeArray(i, 15))

    #print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
