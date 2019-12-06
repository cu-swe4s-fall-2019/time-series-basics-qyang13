test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_overall python pandas_import.py; test -e 5min_small.csv; test -e 5min_small.csv
assert_no_stderr
assert_exit_code 0

rm ssshtest
