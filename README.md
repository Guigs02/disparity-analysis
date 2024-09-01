# disparity-analysis - Sex Analysis of Article Authors on CERN Courier

This Python project scrapes article data from the CERN Courier website, analyses the sex of the authors by their name, and generates a bar plot with the sex distribution.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Licence](#licence)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/cerncourier/disparity-analysis.git
cd disparity-analysis
```
2. **Install the required packages:**
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python3 thread_main.py
```

This will:
- Scrape article links from the CERN Courier website.
- Fetch the title, date, and author of each article.
- Determine the sex of the authors using the gender-guesser library.
- Generate a CSV file with the processed data.
- Create and save a bar chart showing the sex distribution.

## Licence

Distributed under the MIT Licence.

