import os
import numpy as np
import pandas as pd
import re


def write_batch_summary_to_csv(data_directory, output_path):
    """
    Write the summary to a csv file in the
    same directory as the script is run from.
    """
    batch_summary = batch_summarize_hfo_gui_data(data_directory)
    for key, value in batch_summary.items():
        assert len(batch_summary['settings']) == len(value), 'The number of settings does not match the number of values in the {} column. The length of settings is {} and the length of the {} column is {}'.format(key, len(batch_summary['settings']), key, len(value))
    output_dataframe = pd.DataFrame(batch_summary)
    output_dataframe.to_csv(output_path, header=True, index=False)

def batch_summarize_hfo_gui_data(data_directory):
    """
    """
    file_paths = get_excel_file_paths(data_directory)

    batch_summary = dict()
    for file_path in file_paths:
        experiment_name = get_base_file_name_from_path(file_path)
        workbook_summary = summarize_hfo_gui_workbook(file_path)
        workbook_summary['experiment'] = [experiment_name]*int(len(workbook_summary['settings']))
        if batch_summary == dict():
            batch_summary = workbook_summary
        else:
            assert batch_summary.keys() == workbook_summary.keys(), 'The keys of the summary dictionaries do not match. \n\n batch:  \n {} \n\n sheet: \n {}'.format(batch_summary.keys(), workbook_summary.keys())
            for key, value in workbook_summary.items():
                assert type(value) == list, 'The value of the summary dictionary is not a list. The value type is {}'.format(type(value))
                batch_summary[key].extend(value)
    return batch_summary



def get_excel_file_paths(directory):
    """
    Get the excel file paths in the directory.
    """
    files = os.listdir(directory)
    excel_files = [os.path.join(directory, file) for file in files if file.endswith('.xlsx')]
    return excel_files

def get_base_file_name_from_path(file_path):
    """
    Get the file name from the file path.
    """
    file_name = re.split(r'/|\\', file_path)[-1]
    base_file_name = os.path.splitext(file_name)[0]

    return base_file_name

def summarize_hfo_gui_workbook(hfo_gui_data_file):
    """
    Summarize the data in the hfo_gui_data_file.
    """
    workbook = pd.read_excel(hfo_gui_data_file, sheet_name=None)

    assert type(workbook) == dict, 'hfo_gui_data is not a dictionary. Something went wrong when calling pd.read_excel().'

    workbook_summary = dict()

    for sheet_name, sheet in workbook.items():
        sheet_summary = summarize_hfo_gui_sheet(sheet)
        sheet_summary['settings'] = [sheet_name]
        assert type(sheet_summary) == dict, 'sheet_summary is not a dictionary. Something went wrong when calling summarize_hfo_gui_sheet().'
        assert type(sheet_summary['settings']) == list, 'sheet_summary["settings"] is not a list. Something went wrong when calling summarize_hfo_gui_sheet(). The type of sheet_summary["settings"] is {}.'.format(type(sheet_summary['settings']))
        if workbook_summary == dict():
            workbook_summary = sheet_summary
        else:
            assert workbook_summary.keys() == sheet_summary.keys(), 'The keys of the summary dictionaries do not match. \n\n workbook:  \n {} \n\n sheet: \n {}'.format(workbook_summary.keys(), sheet_summary.keys())
            for key, value in sheet_summary.items():
                assert type(value) == list, 'The value of the summary dictionary is not a list. The value type is {}'.format(type(value))
                workbook_summary[key].extend(value)

    return workbook_summary


def summarize_hfo_gui_sheet(sheet):
    """
    Summarize the data in the hfo_gui_data_file.
    """
    if 'Duration' in sheet.columns:
        duration = sheet['Duration']
    elif 'Durations' in sheet.columns:
        duration = sheet['Durations']
    if 'Interval' in sheet.columns:
        interval = sheet['Interval']
    elif 'Intervals' in sheet.columns:
        interval = sheet['Intervals']

    summary = {
        'experiment': [],
        'settings': []
    }

    duraton_summary = append_var_name_to_dict_keys('duration', summarize_column(duration))

    interval_summary = append_var_name_to_dict_keys('interval', summarize_column(interval))

    summary.update(duraton_summary)
    summary.update(interval_summary)

    return summary

def append_var_name_to_dict_keys(var_name, dictionary):
    """
    Append the var_name to the keys of the dict.
    """
    new_dict = dict()
    for key in dictionary.keys():
        new_dict[var_name + ' ' + key] = dictionary[key]
    return new_dict

def summarize_column(raw_column):
    """
    Summarize the data in the hfo_gui_data_file.
    """
    column = raw_column.dropna()
    summary = {
        'mean': [np.mean(column)],
        'min': [np.min(column)],
        '75%': [np.percentile(column, 75)],
        'median': [np.median(column)],
        '25%': [np.percentile(column, 25)],
        'max': [np.max(column)],
        'std': [np.std(column)],
        'variance': [np.var(column)],
        'count': [np.count_nonzero(column)],
    }

    return summary

def main():
    script_path = os.path.realpath (__file__)
    script_directory = os.path.dirname(script_path)
    data_directory = os.path.join(script_directory, 'hfo_gui_data')
    output_path = os.path.join(script_directory, 'hfo_gui_data_summary.csv')
    write_batch_summary_to_csv(data_directory, output_path)

if __name__ == '__main__':
    main()