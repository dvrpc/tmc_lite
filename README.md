# tmc_lite

A minimal fastAPI implementation of the TMC_app. Processes turning movement counts for use in Synchro. 

## Dependencies

Create environment using: 

```
conda env create --file environment.yml
```
then:
```conda activate tmc_fastapi```

## Development Server
CD into "app" folder, then launch Uvicorn server with:

```
uvicorn main:app --reload
```

Upload TMC files, wait 5-10 seconds, then summary of files is returned to your browser. 🤖 
