# TR-PDF-Parser

Parses PDF invoices from the brokerage Trade Republic (for PDF documents in German).

## The problem

To keep track of my investing activities, I had to manually extract properties of my trades. After a while, I made some mistakes and archived the files with a wrong naming convention. That's when I decided to write a script. Furthermore, the popular Software Portfolio Performance can't parse trade documents (PDFs) provided by Trade Republic automatically. As a workaround a .csv import can be done, however.

## What does it?

This python script checks a specified folder for trade documents (e.g., invoices or dividend payments), parses them, renames and moves them to a specified folder and saves a .csv table of all parsed files for easy import into Portfolio Performance.
While the script is parsing the invoices, it prints all properties from that invoice to the terminal as well, such as underlying security, amount of shares, market price, etc., in case a manual import is desired.


## Requirements
- Python 3.7 or larger
- pipenv

## Installation

Clone this repository

```bash
git clone git@github.com:MarcBuch/TR-PDF-Parser.git
```

Install required python modules
```Bash
pip3 install pdfminer.six # not to be confused with pdfminer
```

Edit the source and destination folder inside main.py

```Python
sourceFolder = '/downloads/'
destinationFolder = '/Wertpapierabrechnungen/'
```

Install the dependencies

```Bash
pipenv install
```

Start the script...

```Bash
./start.sh
```

... or run in python directly
```Python
python3 main.py
```

There are no screenshots due to privacy concerns.
