# Time Series basics - importing, cleaning, printing to csv V2.0
## Usage
This is a demonstration of usage of time series utilities. The program `data_import.py` will take in `csv` files, sort, round, de-dup the entries and store the output into a new file.

The standard usage is as following:
```
python data_import.py <Input_folder_name> <out_file_name> <sort_key>
```

## Unit Testing
To test individual functions in the program, use the `test_data_import.py` module:
```
python test_data_import.py
```

The unit test uses python package `unittest`.

## Functional Testing
To run the program using test data set, you can run the functional test `test_data_import.sh`:

```
bash test_data_import.sh
```

The functional test uses a package developed by Ryan Layer, called `ssshtest`.

## Version 2.0 Pandas Import
A new module pandas import is added. This module uses panda to store data frame so that data processing can be more efficient.
### usage
To run `pandas_import.py`, simply type in:
```
python pandas_import.py
```
There is one optional parameter `--data_dir` where you can specify where data is stored, if it's different than the default `./smallData/`.
### Functional Testing
To run functional test, execute the included bash script:
```
bash test_pandas_import.py
```
The command will use `ssshtest` to verify if the import is executed successfully and output files are generated.
### Benchmarking
The panda data import is able to execute and import data much more efficiently. Comparing to the traditional `data_import.py` from version 1.0, which used `8.62 seconds` and `73268 KB` memory.  Pandas data import used `2.20 seconds` and `15416 KB` memory.
