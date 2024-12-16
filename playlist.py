#Downloads Playlists

import os
from spotdl import Spotdl
from spotdl.utils.formatter import create_file_name
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv() #loads the .env file

#Get files with .mp3 extension
def get_mp3_files():
    all_files = os.listdir('.')
    mp3_files = [file for file in all_files if file.endswith('.mp3')]
    return mp3_files

#Initializes spotdl library with client_id and client_secret
spotdl = Spotdl(
    client_id=os.getenv('SP_CLIENT_ID'),
    client_secret=os.getenv('SP_CLIENT_SECRET')
)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpkey.json"

"""Searches songs in the playlist url and get the list of songs already present in the
Blob storage. Compares them and remove existing songs from the download list and downloads
songs. The songs are then uploaded to the Blob and deleted from the local folder"""

def download_upload():
    print("Downloading songs")

    storageClient = storage.Client()
    bucket = storageClient.bucket("local-songs-bucket")

    songs = spotdl.search([os.getenv('PLAYLIST')]) #Search for songs in the playlist. Returns a list
    blobList = bucket.list_blobs() #Songs present in the container
    blobl = [] #List to save the names of the blobs
    songsl = [] #List to save the songs to download

    for blob in blobList:
        blobl.append(blob.name)

    for song in songs:
        """create_file_name function present in the spotdl function is used to find the name
        which will be given to a song when downloaded by the spotdl library. This is then used to
        compare with the name of the songs present in the container"""
        
        currSong = create_file_name(song, "", "mp3") 
        if blobl and currSong.name not in blobl:
            songsl.append(song)
        elif not blobl:
            songsl.append(song) 

    if songsl:
        spotdl.download_songs(songsl) #files are downloaded using the spotdl library
    mp3files = get_mp3_files() #Files present in the local folder are compiled in a list to be uploaded

    #A log.txt is create just to see which files are uploaded
    for name in mp3files:
        #Create a blob with the name of the file to be uploaded
        try:
            print(f"Now uploading {name}")
            blob = bucket.blob(name)
            blob.upload_from_filename(name)
            os.remove(name)
        except Exception as e:
            print(f"Error in uploading {name}, {e}")

    print("Complete")

download_upload()

#Cleanup if any mp3 file is present after the upload
mp3_files = get_mp3_files()
for files in mp3_files:
    os.remove(files)
