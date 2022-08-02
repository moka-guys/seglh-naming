# seglh-naming

This repository contains libraries that build, read and validate SEGLH sample/analysis naming conventions.

## Installation

The repository provides a python package which can be installed with:

`python setup.py install`

## Naming schemes

After installation the package can be used to validate the folling naming schemes.

### Sample

#### Validation
Validate a sample name or file name for conformity (formatting, required identifiers).
If validation fails, a _ValueError_ exception is raised.

```python
from seglh_naming.sample import Sample

sample = Sample('NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001')

sample = Sample('NGS123_12_382398_JD_C_VCP0R33_Pan0000_S12_R1_001')
# ValueError: Sex invalid (C)
```

#### Simplify 
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

#### Constituents

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

