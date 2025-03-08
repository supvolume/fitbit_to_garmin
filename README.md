# Fitbit to Garmin
Process exported Fitbit JSON files to create a CSV file suitable for importing into Garmin Connect.

The following data will be import:
1. Body: weight in fitbit export as lbs and will get converted to kg
2. Activities: there might be timezone different in datetime data. Please recheck if it crucial.
3. Calories Burned
4. Steps
5. Distance: export data from Fitbit is in cm and will get converted to km
6. Floors: altitude, every 10 altitude = 1 floor
7. Minutes Sedentary
8. Minutes Lightly Active
9. Minutes Fairly Active
10. Minutes Very Active


The data that **will NOT** be import<br>
Activity Calories: Data is not listed as importable in Garmin guide.

**Please double check the data units**

When you upload the CSV files in Garmin dashboard, if the import page remains in "Your Upload is Still Processing, Please Check Upload Status" for an extended time, the file may be too large. Try increasing the 'number_of_export_files' setting. The default setting creates 2 CSV files.

For more details on how to request and export your data from Fitbit, please follow Fitbit's guide: [Export your Fitbit data](https://support.google.com/fitbit/answer/14236615).<br>
For a list of acceptable data, please check Garmin's guide: [Import Data From Fitbit to Garmin Connect](https://support.garmin.com/en-US/?faq=HfJ4xPchdD3cmZ2qtDpOR8)

