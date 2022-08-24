import pandas as pd




def summarize_hfo_gui_data(hfo_gui_data_file):
    """
    Summarize the data in the hfo_gui_data_file.
    """
    hfo_gui_data = pd.read_excel(hfo_gui_data_file)
    

    return hfo_gui_data_summary