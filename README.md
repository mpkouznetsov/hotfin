# HotFin

HotFin is a system for downloading and querying
financial data. It is work in progress.

## Running
Start the database:
```commandline
docker run --name HotFinDb -e POSTGRES_PASSWORD=<password> -p 5432:5432 -d postgres
```

Run the downloader:
```commandline
python -m downloader.download
```
This will download ticker mappings
as well as some actual SEC filings.
The goal I am working towards is to
load all 10-K filings for companies
that were included into S&P 500 on a
given date in the past.

Run the loader:
```commandline
python -m loader.loader data/<date-downloader-was-run>
```


## Development
I am following [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

... _In Progress_ ...
