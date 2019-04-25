# pyedi
 - [Usage](#usage)
 - [Examples](#examples)
 - [Project details](#project-details)
    - [Structure of X12 Envelopes](#structure-of-x12-envelopes)
    - [Project Structure](#project-structure)
    - [How it works](#how-it-works)
## Usage
```
from pyedi.edireader import EDIReader
edi_reader = EDIReader(file_name, transaction, version)
edi_reader.validate()
```

Parameter Description:
 - `file_name`: path to the EDI document
 - `transaction`: EDI transtion set eg, 856, 841
 - `version`: EDI document version eg, 5010, 4010
 > Currently we support only 856 transaction and 5010 version

Validation check we support:
 - `start&end segment`: Check if document `start`-`end` pair. Segment might have `end` segment, for instance `ISA` should be followed by `IEA`
 - `mandatory segment missing`: Return mandatory segment if the current segment check is failed
 - `incorrect segment`: Return possible segments if the current segment check is failed
 - `element length`: Check if segment elements have valid length
 - `element value`: Check if segment elements have valid value
 - `element type`: Check if segment elements have valid data type

## Examples
```
python pyedi2xml.py --file documents/856/sample_01.txt --transaction 856 --version 5010
```
## Project details
### Structure of X12 Envelopes
 - Interchange Envelope(ISA/IEA)
 - Functional Group(GS/GE)
 - Transaction Set
 > For more informations, please take a look at [here](https://docs.oracle.com/cd/E19398-01/820-1275/agdaw/index.html)

### Project Structure
### How it works