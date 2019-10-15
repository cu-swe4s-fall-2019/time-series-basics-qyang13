import unittest
import os
import random
import decimal
import statistics
import datetime
import data_import as di


class Test_Data_Import(unittest.TestCase):
    '''
    Testing class for unit test of functions in data_import
    '''
    def test_ImportData_class(self):
        '''
        Test to see if both time and value are imported correctly
        '''
        file = './smallData/activity_small.csv'
        instance = di.ImportData(file)
        self.assertEqual(len(instance._time), len(instance._value))

    def test_Init(self):
        file = open('test.csv', 'w')
        file.write('time,value\n')
        file.write('4/20/20 4:20,20.0\n')
        file.write('4/21/20 4:20,10.0')
        file.close()
        instance = di.ImportData('test.csv')
        self.assertEqual(instance._value[0], 20.0)
        self.assertEqual(instance._value[1], 10.0)
        os.remove('test.csv')

    def test_Init_replace_high_low(self):
        file = open('test.csv', 'w')
        file.write('time,value\n')
        file.write('4/20/20 4:20,low\n')
        file.write('4/21/20 4:20,high')
        file.close()
        instance = di.ImportData('test.csv')
        self.assertEqual(instance._value[0], 40.0)
        self.assertEqual(instance._value[1], 300.0)
        os.remove('test.csv')

    def test_linear_search_notfound(self):
        in_file = './smallData/bolus_small.csv'
        dt = datetime.datetime(2018, 3, 12, 0, 0,)
        instance = di.ImportData(in_file)
        output = instance.linear_search_value(dt)
        self.assertEqual(output, -1)

    def test_linear_search_found(self):
        in_file = './smallData/bolus_small.csv'
        dt = datetime.datetime(2018, 3, 16, 20, 17)
        instance = di.ImportData(in_file)
        output = instance.linear_search_value(dt)
        self.assertEqual(output, [4.5])

    def test_print_array_round_to_5(self):
        data = []
        for f in os.listdir('smallData'):
            data.append(di.ImportData('smallData/'+f))
        rdata_5 = []
        for i in data:
            rdata_5.append(di.roundTimeArray(i, 5))
        self.assertNotEqual(di.printArray(rdata_5,
                                          os.listdir('smallData'),
                                          'out_5', 'meal_small.csv'), -1)
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')

    def test_print_array_round_to_15(self):
        data = []
        for f in os.listdir('smallData'):
            data.append(di.ImportData('smallData/'+f))
        rdata_15 = []
        for i in data:
            rdata_15.append(di.roundTimeArray(i, 15))
        self.assertNotEqual(di.printArray(rdata_15,
                                          os.listdir('smallData'),
                                          'out_15', 'meal_small.csv'), -1)
        self.assertTrue(os.path.exists('out_15.csv'))
        os.remove('out_15.csv')


if __name__ == '__main__':
    unittest.main()
