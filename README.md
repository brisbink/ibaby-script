Python script to convert ibaby Android HTML data to CSV. 

About
=====

The script creates a CSV file with iBaby data. Each column represents a day,
and each row represents a ten-minute interval during the day. The iBaby data is rounded
to the nearest 10 minutes, and the length of time for that activity is used
to fill in all rows with the activity for that time. For example:

,2013-07-02,...
00:00:00,Sleep,...
00:10:00,Sleep,...
00:20:00,Nurse,...
...

NOTE: This script *only* uses the nursing and sleep data.

The CSV file is saved as output.csv and can be imported into your favorite Spreadsheet software for analysis.

To run
======

To run, place ibaby Android HTML in same directory as script and change the
file name to input.html. Use the following command to run the script:

python baby.py

CSV file is saved as output.csv.

Contribute!
===========

This script is very, very far from perfect. Please contribute to make it better!!!
