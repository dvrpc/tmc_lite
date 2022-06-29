# tmc_lite

A web app wrapper around <https://github.com/dvrpc/tmc-summarizer> to process turning movement counts for use in Synchro.

## Production

This is configured to run at <https://tmc.cloud.dvrpc.org/app/tmc-lite/> via Ansible. The repo for the Ansible project is here: <https://github.com/dvrpc/tmc-ansible>.

## Development

### Dependencies and Virtual Environment with Conda

```
conda env create --file environment.yml
conda activate tmc_fastapi
```

### Dependencies and Virtual Environment with venv

```
python3 -m venv ve
. ve/bin/activate
pip install -r requirements_dev.txt
```

### Development Server

Launch Uvicorn server with: `uvicorn app.main:app --reload`.

Upload TMC files, wait 5-10 seconds, then summary of files is returned to your browser. 🤖
