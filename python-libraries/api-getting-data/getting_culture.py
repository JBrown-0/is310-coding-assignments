import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Updated path to your JSON key file
SERVICE_ACCOUNT_FILE = '/Users/justinbrown/Downloads/GoogleDriveAPI.json'

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate and create a service client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Function to list files in Google Drive
def list_files():
    try:
        results = drive_service.files().list(pageSize=10).execute()
        files = results.get('files', [])

        if not files:
            print('No files found.')
            return None
        else:
            # Print file names and IDs
            for file in files:
                print(f"{file['name']} ({file['id']})")
            return files[0]  # Return the first file as an example
    except Exception as e:
        print(f'An error occurred while listing files: {e}')
        return None

# Function to get related data from Europeana
def get_europeana_data(item_title):
    europeana_api_key = 'yrdstore'  # Replace with your Europeana API Key
    europeana_url = f'https://www.europeana.eu/api/v2/search.json?query={item_title}&wskey={europeana_api_key}'
    response = requests.get(europeana_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from Europeana: {response.status_code} - {response.text}")
        return None

# Function to save data as JSON
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

# Main execution
if __name__ == '__main__':
    google_drive_file = list_files()  # Get a file from Google Drive
    if google_drive_file:
        # Extracting the name to find related data in Europeana
        file_name = google_drive_file['name']
        print(f"Using file name: {file_name} for Europeana search")
        
        europeana_data = get_europeana_data(file_name)  # Get related data from Europeana
        
        if europeana_data:
            print("Europeana Data:")
            print(json.dumps(europeana_data, indent=4))  # Print formatted Europeana data
            
            # Saving the combined data into a JSON file
            combined_data = {
                'google_drive_file': google_drive_file,
                'europeana_data': europeana_data
            }
            save_to_json(combined_data, 'google_drive_europeana_data.json')
        else:
            print("No data retrieved from Europeana.")
    else:
        print("No Google Drive file to process.")

