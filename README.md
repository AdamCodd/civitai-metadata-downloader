## Overview
This script was developed after some unsuccessful attempts to build a dataset using Civitai's (limited) API. It's designed to scrape metadata from images directly from the Civitai website. Currently, Civitai's images are numbered consecutively from 1 to ~10 million, and this script is capable of extracting metadata starting from any specified range within this sequence.

## Description
The script uses Selenium WebDriver for Python to navigate Civitai's website and extract metadata for each image within a specified range. A headless Chrome browser is used to streamline the process and avoid anti-bot measures. The metadata for each image is then saved in JSON format to a designated output file.

**Configuration**: You can configure the script to specify the range of image IDs you want to scrape and the output file for the metadata.

## Installation
Clone the Repository
```
git clone https://github.com/AdamCodd/civitai-metadata-downloader.git
cd civitai-metadata-downloader
```
Ensure you have Python 3.6+ installed, then run:
```
pip install -r requirements.txt
```
