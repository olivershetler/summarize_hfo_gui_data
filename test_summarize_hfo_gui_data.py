import os

cwd = os.getcwd()
data_dir = os.path.join(cwd, 'hfo_gui_data')
data_file_path = os.path.join(data_dir, '20170223-NO-3400.xlsx')

def test_summarize_hfo_gui_data():
    summary = summarize_hfo_gui_data(data_dir)