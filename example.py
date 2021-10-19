from fastapi import FastAPI, Query, File, UploadFile, Body
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.plugins.snippet import SnippetPlugin, PremadeSnippets, CodeSampleFactory

PERL = CodeSampleFactory(language="perl", title="PERL", syntax="perl")

app = FastAPI(openapi_plugins=[SnippetPlugin(snippets={**PremadeSnippets.get_all(), **PERL.snippet()})],)


@app.post("/a")
def do_a(demo: str = Query(..., example="lol")):
    return {"answer": "a"}


@app.post("/b", openapi_extra={"x-codeSamples": [PERL.sample("this is how you do it in perl")]})
def do_b(demo: str = Query(..., example="lol"), ex: str = Body(..., example="hey")):
    return {"answer": "a"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


app.mount("/public", StaticFiles(directory="public"), name="public")
