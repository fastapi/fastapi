from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form id="file" enctype="multipart/form-data">
    <input id="files" name="files" type="file" multiple>
</form>
<input type="submit" value="files" onclick="submit('/files/')">
<input type="submit" value="uploadfiles" onclick="submit('/uploadfiles/')">
<pre id="json"></pre>
<script>
    function submit(url){
        const xhr = new XMLHttpRequest();
        // with this you can use PUT or PATCH
        xhr.open('POST', url);
        xhr.onload = function () {
            document.getElementById("json").textContent = JSON.stringify(JSON.parse(this.response), undefined, 2);
        };
        Data = new FormData(document.getElementById('file'));
        xhr.send(Data);
    }
</script>
</body>
    """
    return HTMLResponse(content=content)
