# seglh-naming

This repository contains libraries that build, read and validate SEGLH sample/analysis naming conventions.

## Installation

The repository provides a python package which can be installed with:

`python setup.py install`

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

sample = Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001')

sample = Sample('NGS123_12_382398_JD_C_VCP0R33_Pan0000_S12_R1_001')
# ValueError: Sex invalid (C)
```

#### Sample ID and constituent parts
Get the minimal required Sample ID from filename.

```python
from seglh_naming.sample import Sample

sample = Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.bam')

print(sample)
# NGS123_12_382398_JD_M_VCP0R33_Pan0000

print(sample)
# NGS123_12_382398_JD_M_VCP0R33_Pan0000

print(repr(sample))
# NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001
```

Get or edit constituents of sample ID

```python
from seglh_naming.sample import Sample

sample = Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001')

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

print(Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001').hash)
# 998121029e4cd9b64ec7f9218f776255dd16642db498c50e3f2f378153272d84
print(Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000').hash)
# 998121029e4cd9b64ec7f9218f776255dd16642db498c50e3f2f378153272d84
print(Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0001').hash)
# 9b37c0d8271ca42e5e1067feb22ff3ff2163e549a6094cc2c11ac912d463f07b
```

#### File extensions or types

```python
from seglh_naming.sample import Sample

sample = Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.vcf.gz')

print(sample.file_extension())
# vcf.gz

print(sample.file_extension(include_compression=False))
# vcf
```

