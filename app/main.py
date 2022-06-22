from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from tmc_summarizer import write_summary_file

app = FastAPI()


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<h1>
Upload your TMC Files here! 
</h1>
<h2>
File names must meet the following criteria:
<h2/>
<ul>
        <li> file ends in ``.xls``</li>
        <li> filename has at least 1 underscore</li>
        <li> text before the first underscore is a number</li>
<ul/>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
