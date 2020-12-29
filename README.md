# TR-PDF-Parser

Parses PDF invoices from the brokerage Trade Republic.

## The problem

To keep track of my investing activities, I had to manually extract properties of my trades. After a while, I made some mistakes and archived the files with a wrong naming convention. That's when I decided to write a script.

## What does it?

This python script checks a specified folder for invoices, parses them and moves them to a specified folder.
While the script is parsing the invoices, it returns all needed properties from that invoice, such as underlying security, amount of shares, market price, etc.


## Requirements
- Python 3.7 or larger
- pipenv

## Installation

Clone this repository

```bash
git clone git@github.com:MarcBuch/TR-PDF-Parser.git
```

Edit the source and destination folder inside main.py

```Python
sourceFolder = '/downloads'
destinationFolder = '/Wertpapierabrechnungen'
```

Install the dependencies

```Bash
pipenv install
```

Start the script

```Bash
./start.sh
```

There are no screenshots due to privacy concerns.
