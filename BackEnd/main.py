from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os, json
import youtube, tiktok, instagram
from fastapi.responses import StreamingResponse

app = FastAPI()

#Allowing requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

#GET path to call each of the three python files. Returns a dictionary of routes
@app.get("/getVideos/{search_term}", response_model = dict)
def search_youtube(search_term: str):
    paths = {}
    insta = instagram.search(search_term)
    paths["instagram"] = insta
    you = youtube.search(search_term)
    paths["youtube"] = you
    tik = tiktok.search(search_term)
    paths["tiktok"] = tik
    return paths

CONTENT_CHUNK_SIZE=100*1024 #Block size of video stream

#GET path to stream any video in folder
@app.get("/stream/{name:path}")
async def stream(name:str,range: Optional[str] = Header(None)):
    #Opens file and reads size
    def get_file(name:str):
        f = open(name,'rb')
        return f, os.path.getsize(name)    
    
    #Extracts chunk from stream given start and size
    def chunk_generator_from_stream(stream, chunk_size, start, size):
        bytes_read = 0
        stream.seek(start)
        while bytes_read < size:
            bytes_to_read = min(chunk_size,size - bytes_read)
            yield stream.read(bytes_to_read)
            bytes_read = bytes_read + bytes_to_read
        stream.close()

    asked = range or "bytes=0-"
    stream,total_size=get_file(name)
    start_byte = int(asked.split("=")[-1].split('-')[0])

    #FASTAPI method to stream sequence data
    return StreamingResponse(
        chunk_generator_from_stream(
            stream,
            start=start_byte,
            chunk_size=CONTENT_CHUNK_SIZE,
            size=total_size
        )
        ,headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte}-{start_byte+CONTENT_CHUNK_SIZE}/{total_size}",
            "Content-Type": "video/mp4"
        },
        status_code=206)
