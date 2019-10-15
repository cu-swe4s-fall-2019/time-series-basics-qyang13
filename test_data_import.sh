#!/bin/bash

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_pycodestyle pycodestyle *.py
assert_exit_code 0

run test_all python data_import.py smallData out hr_small.csv
assert_exit_code 0
rm out5.csv
rm out15.csv

run test_no_input python data_import.py notExist out hr_small.csv
assert_exit_code 1
