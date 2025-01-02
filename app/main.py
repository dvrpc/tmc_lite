import os
import shutil

from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from tmc_summarizer import write_summary_file

try:
    from .config import URL_PATH
except ImportError:
    URL_PATH = ""

app = FastAPI()


@app.post(f"{URL_PATH}/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile], background_tasks: BackgroundTasks
):
    # copies the files from the user directory into this repo, runs function from tmc_summarizer, returns summary file, cleans out excel files
    delete_excel()
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


@app.get(f"{URL_PATH}/")
# html and css info
async def main():
    content = (
        """
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
        <li> It is highly recommended that the numbers "e.g., the '3' in 3_DVRPC-TMC....xls" correspond to the node/intersection numbers in Synchro, to keep your intersections organized. 
        <li> Try to only use RAW file straight from OTM, in other words, don't use files that you've edited or added manual calculations to. The tool will often break if you make edits to the file. (renaming the files is fine though)
        <li> Example filenames: 
            <ul>
                <li> 1_DVRPC-TMC-174985 - Erie Ave @ PA 611 Broad St.xls
                <li> 2_DVRPC-TMC-174986 - Erie Ave @ Germantown Ave.xls
                <li> 3_DVRPC-TMC-175011 - Erie Ave @ Kensington Ave.xls
            <ul/>
<ul/>
<p>
Summary file download takes a few seconds after pressing submit..
<p/>
<form action="%s/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<p> report any bugs or requested changes to app <a href="https://forms.gle/nsCDBTv8hi7enu4UA">here.</a></p>
</body>
    """
        % URL_PATH
    )
    return HTMLResponse(content=content)
