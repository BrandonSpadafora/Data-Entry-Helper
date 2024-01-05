# Data-Entry-Helper

## Link
https://data-entry-apper-yx5c4whyt7mfc3blxv63se.streamlit.app/

## Overview
This Streamlit application is designed for efficient data entry of celebrity management team information. It allows users to input data related to celebrities, their agents, and contact information, and then save this data into a CSV file.

## Features
Data Entry for celebrity names, agent names, and their contact details.
Regular reminders to save progress to avoid data loss.
Validation to ensure all fields are filled before submitting.
Duplicate entry detection to maintain data integrity.
CSV file generation for data export.
Installation
To run this application, you will need Python and Streamlit installed on your system. If you don't have Streamlit installed, you can install it using pip:

bash
Copy code
pip install streamlit
Running the App
Clone or download this repository to your local machine.

Navigate to the folder containing the app.

Run the app using Streamlit:

bash
Copy code
streamlit run app.py
The app should open in your default web browser, or you can access it at http://localhost:8501.

## Usage
Data Entry
Input the celebrity's name, the agent's name, and their contact information in the respective fields.
Click 'Check Entry' to submit the data.

## Duplicate Detection
The app checks for duplicate entries of the same celebrity.
If a duplicate is detected, a warning is shown.

## Saving Data
You are reminded every 30 minutes to save your progress.
Click 'Save and Download CSV' to download the entered data as a CSV file.
The downloaded CSV file can be named as per your choice.

## Tips
Regularly save your progress to avoid potential data loss.
Ensure all fields are filled before submitting to avoid empty entries.
Use the 'Cancel and Edit' button to correct any potential duplicates.
