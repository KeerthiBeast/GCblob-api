#Download songs

"""Works almost the same as playlist.py but does not see if the file is already present in 
the blob storage. If the file exists an exception will be thrown and the process end."""

import os
from google.cloud import storage
from spotdl import Spotdl
from dotenv import load_dotenv

load_dotenv() #Load .env

#Get mp3 files in the local folder
def get_mp3_files():
    all_files = os.listdir('.')
    mp3_files = [file for file in all_files if file.endswith('.mp3')]
    return mp3_files

#Initialize the spotdl library
spotdl = Spotdl(
    client_id=os.getenv('SP_CLIENT_ID'),
    client_secret=os.getenv('SP_CLIENT_SECRET')
)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpkey.json"

#Main function
def download_upload():
    print("Downloading songs")
    storageClient = storage.Client()
    bucket = storageClient.bucket("local-songs-bucket")

    songs = spotdl.search([os.getenv('SONG')])
    spotdl.download(songs[0])
    mp3files = get_mp3_files()

    for name in mp3files: 
        try:
            print(f"Now uploading {name}")
            blob = bucket.blob(name)
            blob.upload_from_filename(name)
            os.remove(name)
        except Exception as e:
            print(f"Error in uploading {name}")


    print("Complete")

download_upload()

mp3_files = get_mp3_files()
for files in mp3_files:
    os.remove(files)
