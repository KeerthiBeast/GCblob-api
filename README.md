﻿# GCblob-API
A Flask endpoint for [Azblob](https://github.com/keerthibeast/Azblob)

Uses Spotdl library to download Songs and Playlists and upload them to an GCP Bucket.

# Usage
- Download required packages from requirements.txt
- Download ffmpeg for spotdl to work
- Rename .env_example to .env and add the require information
- Get a key json file from you principle account with the required permissions from GCP
- `GET /api`: Used to check the status of the applicatoin
- `POST /playlist`: Used to download playlists. A POST request with json body value playlist_url is expected 
- `POST /song`: Used to download songs. A POST request with json body value song_url is expected
- `GET /bloblist`: Used to get the Blob list in the GCP

# How it works
You launch the application and send the required data to the endpoint. When the request is a success a  subprocess is started for the corresponding function. The subprocess will start in a different thread and the response will be send without waiting for the songs to download.
