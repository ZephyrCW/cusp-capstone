# Read Me


## Introduction
This is a repository for CUSP-InCitu Team. It serves as a terminal and use [Github Actions](https://github.com/features/actions) to automatically scrape data from ZAP and Pluto. 

## Repository Structure
The python script that ran by Github Action is included in '.github/workflows/' as part of `.yml` file, there is also a copy of python script alone in the root folder for reference. Scraped data is store as `zap_projects_data.csv` and `consolidated_data.csv`.

Workflow will run on a github server everyday 8AM, scraping all the desired information from ZAP and Pluto, store and push them into this repo. The process should take about 8 minuts in total. 

## Team Mmeber: 
- [Charles Wu](https://github.com/ZephyrCW)
- Hanfie Vandanu
- Zenn Wong
- Ying Lei
