# README

This script takes any excel files you place into the `hfo_gui_data` folder that contain the column names `Duration` and `Interval` (or, if those aren't present, `Durations` and/or `Intervals`). It returns a summary of the data in a new excel file with several statistical parameters.

You can find and edit the parameters in the `summarize_column` function in the `summarize_hfo_gui_data` module.

The module defines a function called `write_batch_summary_to_csv` that writes a batch summary to csv, and several support functions that make it easier to read, edit and mantain the code.

There is a `main()` function that can be used to run the script from the `summarize_hfo_gui_data` module.

You can run the `summarize_hfo_gui_output` script by typing `python summarize_hfo_gui_output.py` in the command line or openning the file in an ide such as vs code and pressing the play button.

You can run the tests contained in the `test_summarize_hfo_gui_data` module by installing pytest, using `cd` to get into the project directory and typing `pytest`. If you want to uncomment and see any of the `print`lines in the tests, you can do so by typing `pytest -s`.

