from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os, json
import youtube, tiktok, instagram
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/getVideos/{search_term}", response_model = dict)
def search_youtube(search_term: str):
    paths = {}
    # you = youtube.search(search_term)
    # paths["youtube"] = you
    # tik = tiktok.search(search_term)
    # paths["tiktok"] = tik
    insta = instagram.search(search_term)
    paths["instagram"] = insta
    return paths

CONTENT_CHUNK_SIZE=100*1024

@app.get("/stream/{name:path}")
async def stream(name:str,range: Optional[str] = Header(None)):
    def get_file(name:str):
        f = open(name,'rb')
        return f, os.path.getsize(name)    
    
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
    print(name)
    start_byte = int(asked.split("=")[-1].split('-')[0])

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
