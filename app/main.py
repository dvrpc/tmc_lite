import os
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from tmc_summarizer import write_summary_file
import shutil
from fastapi.responses import FileResponse

app = FastAPI()


@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile], background_tasks: BackgroundTasks
):
    # copies the files from the user directory into this repo, runs function from tmc_summarizer, returns summary file, cleans out excel files
    for file in files:
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    cwd = os.getcwd()
    summary = write_summary_file(cwd)
    summary_filepath = os.path.normpath(summary[0])
    summary_filename = str(os.path.basename(os.path.normpath(summary[0])))
    background_tasks.add_task(delete_excel)
    return FileResponse(
        summary_filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=summary_filename,
    )


def delete_excel():
    # deletes the copied excel files and the summary file after returning it to the users downloads
    path = os.getcwd()
    os.chdir(path)
    for file in os.listdir(path):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            os.remove(file)


@app.get("/")
# html and css info
async def main():
    content = """
<head>
<style>
h1 {
  color: Black;
  font-family: monospace;
}
h2 {
  color: Black;
  font-family: monospace;
}
p {
  color: Black;
  font-family: monospace;
  font-size: 15px
}
</head>
</style>
<body>
<h1>
TMC Summarizer Bot
</h1>
<img src="https://www.reshot.com/preview-assets/icons/LH8Z2JXSQ7/robot-LH8Z2JXSQ7.svg" alt="Free robot icon" width ="200" height = "200"/>
<h2>
File names must meet the following criteria:
<h2/>
<ul>
        <li> File ends in `.xls`</li>
        <li> Filename has at least 1 underscore</li>
        <li> Text before the first underscore is a number</li>
<ul/>
<p>
Summary file download takes a few seconds after pressing submit..
<p/>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
