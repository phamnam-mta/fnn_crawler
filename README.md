# FNN Crawler

FNN Crawler is a web crawler to scrape information about movies from online movie websites

## Requirements

* Python 3.5.2+
* Works on Linux, Windows, macOS, BSD

## Installation

1. Clone this repository
```bash
git clone https://github.com/phamnam-mta/fnn_crawler.git
```

2. Install dependencies
First, download file 'Twisted‑20.3.0‑cp39‑cp39‑win_amd64.whl' https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted at this location

After run command:
```bash
pip install Twisted‑20.3.0‑cp39‑cp39‑win_amd64.whl
pip install -r requirements.txt
```

## Example running the spiders

You can run a spider using the scrapy crawl command:


```bash
scrapy crawl voz
```