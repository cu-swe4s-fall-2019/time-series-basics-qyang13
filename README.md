# Time Series basics - importing, cleaning, printing to csv
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
