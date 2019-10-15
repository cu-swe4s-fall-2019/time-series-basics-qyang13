import csv
import sys
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
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
        # open file, create a reader from csv.DictReader, and read input times and values
        with open(data_csv, 'r') as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                if 'time' not in row.keys() or 'value' not in row.keys():
                    raise ValueError('Input data needs contain time and values')

                try:
                    if row['value'] == 'low':
                        row['value'] = 40.0
                        continue
                    elif row['value'] == 'high':
                        row['value'] = 300.0
                        continue

                    val = float(row['value'])
                    if val is not None:
                        self._time.append(dateutil.parser.parse(row['time']))
                        self._value.append(val)

                except ValueError:
                    print('Invalid value found' + row['value'])

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

def roundTimeArray(obj, res, ops = 'sum'):
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
    proc_times = []
    proc_values = []
    uniq_times = []

    # Process time following round time implementation
    for times in obj._time:
        minminus = datetime.timedelta(minutes = (times.minute % res))
        minplus = datetime.timedelta(minutes = res) - minminus
        if (times.minute % res) <= res/2:
            newtime = times - minminus
        else:
            newtime=times + minplus
        proc_times.append(newtime)

    # De-duplication
        for times in proc_times:
            if times not in uniq_times:
                if ops == 'average':
                    val = np.average(obj.linear_search_value(times))
                if ops == 'sum':
                    val = np.sum(obj.linear_search_value(times))
                proc_values.append(val)
                uniq_times.append(times)
            else:
                continue

    obj._time = uniq_times
    obj._value = proc_values
    return(zip(obj._time, obj._value))


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    out_data = []
    key_index = 0
    data_list = [list(obj) for obj in data_list]

    # Try to find the index for the key_file
    for i in range(len(annotation_list)):
        if annotation_list[i] == key_file:
            out_data = data_list[i]
            key_index = i
            break

    if i == len(annotation_list)-1:
        print("Key not found ")
        sys.exit(1)

    # Start writing into base_name.csv
    with open(base_name+'.csv', 'w') as f:
        f.write('time,')
        f.write(annotation_list[key_index].split('_')[0]+',')
        non_key = list(range(len(annotation_list)))
        non_key.remove(key_index)

        for index in non_key:
            f.write(annotation_list[index].split('_')[0]+',')
        f.write('\n')

        for time, value in out_data:
            f.write(str(time)+','+str(value)+',')
            for n in non_key:
                t_list = [entry[0] for entry in data_list[n]]
                if time in t_list:
                    f.write(str(data_list[n][t_list.index(time)][1])+',')
                else:
                    f.write('0,')
            f.write('\n')

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
