from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load the credentials from the JSON file
creds = Credentials.from_authorized_user_info(info=info)

# Build the Drive API service
service = build("drive", "v3", credentials=creds)

# Create a file on Drive
file_metadata = {
    "name": "filename.xlsx",
    "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}
media = MediaFileUpload("filename.xlsx",
                        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        resumable=True)
file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
print(F'File ID: "{file.get("id")}".')