# Make sure you cd to the directory containing this file before suing the pytest or pytest -s commands.

from summarize_hfo_gui_data import (
    write_batch_summary_to_csv
    ,batch_summarize_hfo_gui_data
    ,get_excel_file_paths
    ,get_base_file_name_from_path
    ,summarize_hfo_gui_workbook
    ,summarize_hfo_gui_sheet
    ,append_var_name_to_dict_keys
    ,summarize_column
)

import os
import numpy as np
import pandas as pd


script_path = os.path.realpath (__file__)
script_directory = os.path.dirname(script_path)
data_dir = os.path.join(script_directory, 'hfo_gui_data')
data_file_path = os.path.join(data_dir, '20170223-NO-3400.xlsx')

def test_write_batch_summary_to_csv():
    output_path = os.path.join(data_dir, 'batch_summary.csv')
    (data_dir, os.path.join(data_dir, output_path))
    write_batch_summary_to_csv(data_dir, output_path)
    in_memory_summary = pd.DataFrame(batch_summarize_hfo_gui_data(data_dir))
    summary_from_csv = pd.read_csv(output_path, header=0)
    os.remove(output_path)
    try:
        pd.testing.assert_frame_equal(in_memory_summary, summary_from_csv)
    except:
        raise AssertionError('\n\nThe in memory summar is not equal to the summary read from the output csv file.')


def test_batch_summarize_hfo_gui_data():
    summary = batch_summarize_hfo_gui_data(data_dir)
    #print('\n\n', summary)

def test_excel_file_paths():
    file_paths = get_excel_file_paths(data_dir)
    #print('\n\n', file_paths)

def test_get_base_file_name_from_path():
    file_path = 'C:\\Users\\james\\Desktop\\hfo_gui_data\\20170223-NO-3400.xlsx'
    base_file_name = get_base_file_name_from_path(file_path)
    #print('\n\n', base_file_name)
    assert base_file_name == '20170223-NO-3400'


def test_summarize_hfo_gui_workbook():
    summary = summarize_hfo_gui_workbook(data_file_path)
    #print('\n\n', summary)

def test_summarize_hfo_gui_sheet():
    workbook = pd.read_excel(data_file_path, sheet_name=None)
    sheet = list(workbook.values())[0]
    summary = summarize_hfo_gui_sheet(sheet)
    #print('\n\n', summary)

def test_append_var_name_to_dict_keys():
    dictionary = {
        'mean': 1,
        'std': 2,
        'min': 3,
        'max': 4,
        'count': 5,
    }
    var_name = 'duration'
    new_dict = append_var_name_to_dict_keys(var_name, dictionary)
    assert new_dict['duration mean'] == 1
    assert new_dict['duration std'] == 2
    assert new_dict['duration min'] == 3
    assert new_dict['duration max'] == 4
    assert new_dict['duration count'] == 5
    assert len(new_dict) == 5
    #print('\n\n', new_dict)

def test_summarize_column():
    column = pd.Series([1,2,3,4,5, 6, 7, 8, 9, 10])
    summary = summarize_column(column)
    assert summary['mean'] == [5.5]
    assert summary['min'] == [1]
    assert summary['25%'] == [3.25]
    assert summary['median'] == [5.5]
    assert summary['75%'] == [7.75]
    assert summary['max'] == [10]
    assert np.round(summary['std'][0], 2) == 2.87
    assert summary['variance'] == [8.25]
    assert summary['count'] == [10]
    #print('\n\n', summary)
