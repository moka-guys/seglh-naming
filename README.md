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

After installation the package can be used to validate the folling naming schemes.

### Sample

The sample names are structured as follows and can be accessed by the correponding class property.

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

#### Validation
Validate a sample name or file name for conformity (formatting, required identifiers).
If validation fails, a _ValueError_ exception is raised.

```python
from seglh_naming.sample import Sample

# validate sample name
sample = Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001')

# build and validate from the constituent parts
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

#### Sample ID and constituent parts
Get the minimal required Sample ID from filename.

```python
from seglh_naming.sample import Sample

sample = Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.bam')

print(sample)
# NGS123_12_382398_JD_M_VCP0R33_Pan0000

print(repr(sample))
# NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001
```

Get or edit constituents of sample ID

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

#### Deidentify
Returns a stable identifier for a given sample ID as a salted, cryptographic hash (SHA256).

```python
from seglh_naming.sample import Sample

print(Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001').hash())
# 998121029e4cd9b64ec7f9218f776255dd16642db498c50e3f2f378153272d84
print(Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0000').hash())
# 998121029e4cd9b64ec7f9218f776255dd16642db498c50e3f2f378153272d84
print(Sample.from_string('NGS123_12_382398_JD_M_VCP0R33_Pan0001').hash())
# 9b37c0d8271ca42e5e1067feb22ff3ff2163e549a6094cc2c11ac912d463f07b
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

### Samplesheet
The samplesheet names are structured as follows and can be accessed by the correponding class property.
```
211008_A01229_0040_AHKGTFDRXY_SampleSheet.csv
+====== +== +== += +==+=============
|       |   |   |  |  |
|       |   |   |  |  +- fileext (.csv, required)
|       |   |   |  +---- samplesheetstr (required (exact))
|       |   |   +------- flowcellid (alphanumeric)
|       |   +----------- autoincrno (4 digits)
|       +--------------- sequencerid
+----------------------- date (6 digits)
```

#### Validation
Validate a samplesheet name / file path for conformity (formatting, required identifiers).
If validation fails, a _ValueError_ exception is raised.

```python
from seglh_naming.samplesheet import Samplesheet

# validate sample name
samplesheet = Samplesheet.from_string('211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv')

samplesheet = Samplesheet.from_string('21110_A01229_0040_AHKGTFDRXY_SampleSheet.csv')
# ValueError: Date invalid (21110)
```

#### Samplesheet name and constituent parts
Get the minimal required samplesheet name from filename.

```python
from seglh_naming.samplesheet import Samplesheet

samplesheet = Samplesheet.from_string('211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv')

print(samplesheet)
# 211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv

print(repr(sample))
# 211108_A01229_0040_AHKGTFDRXY_SampleSheet.csv
```

Get or edit constituents of samplesheet name

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