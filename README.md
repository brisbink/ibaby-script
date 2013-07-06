Python script to convert ibaby Android HTML data to CSV. 

About
=====

The script creates a CSV file with iBaby data. Each column represents a day,
and each row represents a ten-minute interval during the day. The iBaby data is rounded
to the nearest 10 minutes, and the length of time for that activity is used
to fill in all rows with the activity for that time. For example:

,2013-07-02,...<br>
00:00:00,Sleep,...<br>
00:10:00,Sleep,...<br>
00:20:00,Nurse,...<br>
...

At the bottom of the CSV is a set of data: ave time nursing, ave time between nursing,
and the total time nursing. For example:

,2013-07-06,2013-07-05,2013-07-04...<br>
Time nursing,2.350000,6.216667,7.316667...<br>
Ave time nursing,0.335714,0.444048,0.522619...<br>
Ave time between nursing,1.083333,1.809524,1.675000...

The CSV file is saved as output.csv and can be imported into your favorite Spreadsheet software for analysis.

NOTE: This script *only* uses the nursing and sleep iBaby data.


To run
======

To run, place ibaby Android HTML in same directory as script and change the
file name to input.html. Use the following command to run the script:

python baby.py

CSV file is saved as output.csv.

Contribute!
===========

This script is very, very far from perfect. Please contribute to make it better!!!
