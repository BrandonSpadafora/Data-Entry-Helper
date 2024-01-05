import streamlit as st
import pandas as pd
import re
import base64
from io import BytesIO
import time
from datetime import datetime

# Define regex patterns
phone_pattern = re.compile(r'Phone: (\S+)')
fax_pattern = re.compile(r'Fax: (\S+)')
email_pattern = re.compile(r'Email: (\S+)')

# Initialize session state variables if they don't exist
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Celebrity', 'Agent', 'Phone', 'Fax', 'Email'])
if 'duplicate_entry' not in st.session_state:
    st.session_state.duplicate_entry = None
if 'allow_duplicate' not in st.session_state:
    st.session_state.allow_duplicate = False

# Function to check for duplicates in the 'Celebrity' column and return the index(es)
def get_celebrity_duplicate_indices(celebrity):
    return st.session_state.df[st.session_state.df['Celebrity'] == celebrity].index.tolist()

# Initialize session state for the last reminder time if it doesn't exist
if 'last_reminder_time' not in st.session_state:
    st.session_state.last_reminder_time = time.time()

# Function to check if it's time to show the reminder
def is_time_for_reminder():
    current_time = time.time()
    # Check if 30 minutes (1800 seconds) have passed
    if current_time - st.session_state.last_reminder_time > 1800:
        st.session_state.last_reminder_time = current_time
        return True
    return False

# Streamlit interface
st.title('Data Entry for Management Teams')

# Check if it's time to show the reminder
if is_time_for_reminder():
    st.warning('⏰ Reminder: Consider saving your progress.')

# Form for data input
with st.form('data_entry_form'):
    celebrity_name = st.text_input('Celebrity Name', value=st.session_state.duplicate_entry['Celebrity'] if st.session_state.duplicate_entry else "")
    agent_name = st.text_input('Agent Name', value=st.session_state.duplicate_entry['Agent'] if st.session_state.duplicate_entry else "")
    contact_info = st.text_area('Contact Info Block', value=st.session_state.duplicate_entry['Contact'] if st.session_state.duplicate_entry else "")
    submitted = st.form_submit_button('Check Entry')

# Process the form submission
if submitted:
    if not (celebrity_name and agent_name and contact_info):
        st.error("Please fill in all the fields before submitting.")
    else:
        # Search for duplicate celebrity names
        duplicate_indices = get_celebrity_duplicate_indices(celebrity_name)
        
        # If there is a duplicate
        if duplicate_indices:
            st.warning(f"The celebrity name you just entered matches the one in row {duplicate_indices[0]}.")
            # Save the current entry in session state to pre-fill the form in case they want to edit it
            st.session_state.duplicate_entry = {'Celebrity': celebrity_name, 'Agent': agent_name, 'Contact': contact_info}
            if st.button('Cancel and Edit'):
                st.session_state.allow_duplicate = False  # Keep the flag false to edit
        else:
            # Process the contact info
            phone_match = phone_pattern.search(contact_info)
            fax_match = fax_pattern.search(contact_info)
            email_match = email_pattern.search(contact_info)
            
            # Append to DataFrame
            st.session_state.df = st.session_state.df.append({
                'Celebrity': celebrity_name,
                'Agent': agent_name,
                'Phone': phone_match.group(1) if phone_match else None,
                'Fax': fax_match.group(1) if fax_match else None,
                'Email': email_match.group(1) if email_match else None,
            }, ignore_index=True)
            st.success('Entry saved!')
            # Reset the duplicate entry and flag
            st.session_state.duplicate_entry = None
            st.session_state.allow_duplicate = False
            # Clear the form
            st.experimental_rerun()

# Function to generate a download link for the DataFrame
def get_table_download_link(df):
    # Generate a CSV file and encode it into a base64 string
    towrite = BytesIO()
    df.to_csv(towrite, encoding='utf-8', index=False)
    towrite.seek(0)  # move to the beginning after writing
    b64 = base64.b64encode(towrite.read()).decode()  # encode to base64 (string)
    
    # Create the download button and return it
    href = f'<a href="data:file/csv;base64,{b64}" download="celebrity_management_teams.csv">Download CSV File</a>'
    return href

# Display the DataFrame in the app
st.dataframe(st.session_state.df)

# Save button to manually save the DataFrame to CSV and provide a download link
if st.button('Save and Download CSV'):
    st.success('Data is ready to download!')
    # Generate and display the download link
    st.markdown(get_table_download_link(st.session_state.df), unsafe_allow_html=True)
