# seglh-naming

This repository contains libraries that build, read and validate SEGLH sample/analysis naming conventions.

## Installation

The repository provides a python package which can be installed with:

`python setup.py install`

NB: Use the `--user` flag or install into an virtualenv/pipenv if not installing globally.

## Contributions
Any contributions _must_ follow GIT-Flow. Code reviews are mandatory and _must_ be done by a representative of each site implementing the naming scheme.

A full test suite is provided and can be run with `pytest -v`. Code formatting _must_ follow recommendations of PEP8. Both requirements are checked automatically via GitHub Actions on pushes to `develop` and `main` branches


## Naming schemes

After installation the package can be used to validate the folling naming schemes:
* Sample name
* Samplesheet name

The libraries validate samplesheet name/path, sample name or file name/path for conformity (formatting, required 
identifiers). This is performed by accessing the corresponding class property. If validation fails, a _ValueError_ 
exception is raised.

The naming schemes are structured as follows:

### Sample name
```
NGS123_12_382398_P9392B_JD_M_VCP0R33_Pan0000_RJZ_S12_R1_001.realigned.bam
+===== += +===== +===== += + +====== +====== +== +== += +==+=============
|      |  |      |      |  | |       |       |   |   |  |  |
|      |  |      |      |  | |       |       |   |   |  |  +- rest (trailing string, optional)
|      |  |      |      |  | |       |       |   |   |  +---- stable (not informative, optional)
|      |  |      |      |  | |       |       |   |   +------- readnumber (optional)
|      |  |      |      |  | |       |       |   +----------- samplesheetindex (optional)
|      |  |      |      |  | |       |       +--------------- ods (ODS code, optional)
|      |  |      |      |  | |       +----------------------- panelnumber (Pan Number)
|      |  |      |      |  | +------------------------------- panelname (Human readable Pan number)
|      |  |      |      |  +--------------------------------- sex (optional)
|      |  |      |      +------------------------------------ initials (secondary identifier, optional)
|      |  |      +------------------------------------------- id2 (secondary identifier, optional)
|      |  +-------------------------------------------------- id1 (DNA number)
|      +----------------------------------------------------- samplecount (number in batch/library)
+------------------------------------------------------------ libraryprep (library name)
```
#### Requirements

When creating the sample name (e.g. in the sample sheet) the sample name should adhere to the following conventions. 
Examples are provided.

Special characters (e.g. -, $, _) are _not_ allowed within the identifiers, and identifiers _must_ be 
spaced using a single underscore only. 

| Element           | Requirements                                                                                                                            | Examples                                                |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| libraryprep       | ≥3 uppercase letters followed by ≥1 digit and ≥0 digits/letters/combination (upper and/or lower case)                                   | NGS431, NGS431rpt, ADX346, TSO239, SNP123, WES894       |
| samplecount       | 2-3 digits                                                                                                                              | 00, 15, 120                                             |
| id1               | ≥6 digits                                                                                                                               | 123456, 000000                                          |
| id2               | Starts with either 1 digit, 'HD', 'NA', 'NTC', 'NC' or 'SC'. Followed by at least 3 digits/letters/combination (upper and/or lower case) | 223785, 2345, NA12878, HD200, NTC000, NC000, SC07100496 |
| initials          | 2 uppercase letters                                                                                                                  | AW, RD                                                  |
| sex               | 'M', 'F', or 'U'                                                                                                                  | M, F, U                                                 |
| panelname         | 3+ digits/letters/combination (upper and/or lower case)                                                                                 | FFPEControl, SWIFT57, VCP1R134StG, SNPIDv2, CRC         |
| panelnumber       | 'Pan' followed by 2+ digits                                                                                                             | Pan2345, Pan3456                                        |

The following additional requirements _must_ also be met: 
* TSO500 sample names must not be longer than 40 characters
* The sample name _must_ contain id1
* The sample name _must also_ contain: id2, _or_ both initials and sex

### Samplesheet name

```
211008_A01229_0040_AHKGTFDRXY_SampleSheet.csv
+====== +== +== += +==+=============
|       |   |   |  |  |
|       |   |   |  |  +- fileext
|       |   |   |  +---- samplesheetstr
|       |   |   +------- flowcellid
|       |   +----------- autoincrno
|       +--------------- sequencerid
+----------------------- date
```

#### Requirements

When creating the samplesheet name, it should adhere to the following conventions. Examples are provided.

Special characters (e.g. -, $, _) are _not_ allowed within the identifiers unless explicitly stated, and 
identifiers _must_ be spaced using a single underscore only. There must not be an underscore between 'SampleSheet' and 
'.csv'.

| Element        | Requirements                                                                                                                  | Examples                    |
|----------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| date           | 6 digits                                                                                                                      | 221004                      |
| sequencerid    | ≥1 digits or uppercase letters                                                                                                | M02353, NB551068            |
| autoincrno     | 4 digits                                                                                                                      | 0123                        |
| flowcellid     | EITHER (9 zeros followed by a hyphen then 5 digits/uppercase letters/combination) OR (9 digits/uppercase letters/combination) | 000000000-JRLLW, AHJYL5AFX3 |
| samplesheetstr | 'SampleSheet' _Must be an exact match_                                                                                        | SampleSheet                 |
| fileext        | '.csv' _Must be an exact match_                                                                                               | .csv                        |

## Usage

### Sample

```python
from seglh_naming.sample import Sample

# Validate sample name
sample = Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001')

# Build and validate from the constituent parts
sample = Sample.from_dict({
	"libraryprep": "NGS123",
	"samplecount": 12,
	"id1": "382398",
	"initials":	"JD",
	"sex": "M",
	"panelname": "VCP0R33",
	"panelnumber": "Pan0000"
})

sample = Sample.from_string('NGS123_12_382398_JD_C_VCP0R33_Pan0000_S12_R1_001')
# ValueError: Sex invalid (C)
```

#### Get name and constituent parts

Get the minimal required Sample ID.
```python
from seglh_naming.sample import Sample

sample = Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.bam')

print(sample)
# NGS123_12_382398_JD_M_VCP0R33_Pan0000

print(repr(sample))
# NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001

## Samplesheet
```python
from seglh_naming.samplesheet import Samplesheet

# Validate samplesheet name
samplesheet = Samplesheet.from_string('211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv')

samplesheet = Samplesheet.from_string('21110_A01229_0040_AHKGTFDRXY_SampleSheet.csv')
# ValueError: Date invalid (21110)
```
Get or edit constituents of sample name.
```python
from seglh_naming.sample import Sample

sample = Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001')

sample.id1
# 382398

sample.id1 = '000111'

print(sample)
# NGS123_12_000111_JD_M_VCP0R33_Pan0000

print(sample.is_modified)
# True
```
#### File extensions or types

```python
from seglh_naming.sample import Sample

sample = Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.vcf.gz')

print(sample.file_extension())
# vcf.gz

print(sample.file_extension(include_compression=False))
# vcf
```
#### Deidentify
Return a stable identifier for a given sample ID as a salted, cryptographic hash (SHA256).

```python
from seglh_naming.sample import Sample

print(Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001').hash())
# 998121029e4cd9b64ec7f9218f776255dd16642db498c50e3f2f378153272d84
print(Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000').hash())
# 998121029e4cd9b64ec7f9218f776255dd16642db498c50e3f2f378153272d84
print(Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0001').hash())
# 9b37c0d8271ca42e5e1067feb22ff3ff2163e549a6094cc2c11ac912d463f07b
```

### Samplesheet

#### Get name and constituent parts

Get the minimal required string from the input. 

```python
from seglh_naming.samplesheet import Samplesheet

samplesheet = Samplesheet.from_string('/home/samplesheet/211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv')

print(samplesheet)
# 211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv

print(repr(sample))
# 211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv
```

Get or edit constituents of samplesheet name.

```python
from seglh_naming.samplesheet import Samplesheet

samplesheet = Samplesheet.from_string('211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv')

samplesheet.sequencerid

# 'A01229'

samplesheet.sequencerid = 'NB552085'

print(samplesheet)
# 211108_NB552085_0040_AHKGTFDRXY_SampleSheet.csv

print(samplesheet.is_modified)
# True
```

#### Deidentify
Returns a stable identifier for a given sample ID as a salted, cryptographic hash (SHA256).

```python
from seglh_naming.samplesheet import Samplesheet

print(Samplesheet.from_string('211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv').hash())
# 4b9259df18af72841419d832988d6ffdd58ec16525b6ccdca908b9e410803c62
print(Samplesheet.from_string('220401_M02353_0676_000000000-K4669_SampleSheet.csv').hash())
# 22ed36ee4ec1a858dc46c49d924799f810f055031d4a6a348c6609766a076741
print(Samplesheet.from_string('220401_NB552085_0188_AHJWL5AFX3_SampleSheet.csv').hash())
# 6e996e99483f40c3b9ebd52d0f56c672813907bfe58a08d92f4155f5050c86a3
```