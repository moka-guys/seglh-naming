import pytest

from seglh_naming.sample import Sample

####################
# FIXTURES #########
####################

@pytest.fixture
def valid_samples():
    return [
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_RJZ_S12_R1",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000.fasta",
        "NGS123_12_382398_00324B_VCP0R33_Pan0000_S12_R1",
        "TSO123_00_234234_9872349_UP01_Pan4969_CopyNumberVariants.vcf",
        "NGS123_00_234234_000TOOLONG4TSO_UP01_Pan4969",
        "ONC123_00_EK234234_3243_Pan0000.realign.bam",
        {
            "libraryprep": "ONC123",
            "samplecount": 12,
            "id1": "BAC123",
            "id2": "12345",
            "initials": "XX",
            "sex": "U",
            "panelname": "PANEL",
            "panelnumber": "Pan0000"
        }
    ]

@pytest.fixture
def invalid_samples():
    return [
        "NGS123_12_382398_PT324B_VCP0R33_Pan0000b_S12",
        "NGS123_12_382398_VCP0R33_Pan0000",
        "NGS123_12_382398_JD_M_VCP0R33_Pan000a_S12_R1",
        "NGS123_12_382398_PT324B_Pan0000_S12_R1",
        "NGS123_12_382398_PT324B_Pn0000_S12_R1",
        "NGS123_12_382398_Pan0000_S12_R1",
        "TSO123_00_234234_00TOOLONGFORTSO_UP01_Pan4969",
        {
            "libraryprep": "ONC123",
            "samplecount": 12,
            "id1": "BAC123",
            "sex": "U",
            "panelname": "PANEL",
            "panelnumber": "Pan0000"
        }
    ]

@pytest.fixture
def constituents():
    return [
        ("NGS123_12_382398_02SECONDARY_VC033_Pan0000_S12", 'panelnumber', 'Pan0000'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1", 'readnumber', 'R1'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000", 'panelname', 'VCP0R33'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_RJZ_S12_R1", 'ods', 'RJZ'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_RJZ", 'ods', 'RJZ'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000.fasta", 'initials', 'JD'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000.fasta", 'sex', 'M'),
        ("NGS123_12_382398_0024B_VCP0R33_Pan0000_S12_R1", 'sex', None)
    ]

@pytest.fixture
def file_names():
    return [
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.bam",
         True, 'bam'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.realigned.bam",
         False, 'bam'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.re.xxx.vcf.gz",
         True, 'vcf.gz'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.re.xxx.vcf.gz",
         False, 'vcf'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R2_001.fastq.gz",
         True, 'fastq.gz'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R2_001.fastq.gz",
         False, 'fastq'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.haplotyper.vcf",
         True, 'vcf'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.haplotyper.vcf",
         False, 'vcf'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000.haplotyper.vcf",
         False, 'vcf'),
    ]

@pytest.fixture
def file_paths():
    return [
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001.haplotyper.vcf",
         True, ''),
        ("/some/path/NGS123_12_382398_JD_M_VCP0R33_Pan0000.haplotyper.vcf",
         True, "/some/path"),
        ("/some/path/NGS123_12_382398_JD_M_VCP0R33_Pan0000",
         True, "/some/path"),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001",
         False, ''),
        ({
            "libraryprep": "ONC123",
            "samplecount": 12,
            "id1": "BAC123",
            "id2": "12345",
            "initials": "XX",
            "sex": "U",
            "panelname": "PANEL",
            "panelnumber": "Pan0000"
        }, False, '')
    ]

@pytest.fixture
def field_validation():
    return [
        (None, 'panelnumber', 'Pan1111'),
        ('Pan Number invalid', 'panelnumber', 'Pan0'),
        (None, 'libraryprep', 'NGS232b'),
        ('LibraryPrep name invalid', 'libraryprep', 'NS232'),
        (None, 'id1', 'AM1123'),
        ('Specimen/DNA number invalid', 'id1', 'AM1'),
    ]

####################
# TESTS ############
####################

def test_invalid_samples(invalid_samples):
    for samplename in invalid_samples:
        with pytest.raises(ValueError):
            Sample(samplename)


def test_field_validation(field_validation):
    s = "NGS123_12_382398_00324B_VCP0R33_Pan0000_S12_R1"
    for match_exception, field, value in field_validation:
        sample = Sample(s)
        if match_exception:
            with pytest.raises(ValueError, match=match_exception):
                setattr(sample, field, value)
        else:
            setattr(sample, field, value)
            assert getattr(sample,field) == value


def test_valid_samples(valid_samples):
    assert all([Sample(s) for s in valid_samples])


def test_constituents(constituents):
    for fi, c, result in constituents:
        assert getattr(Sample(fi), c) == result


def test_sample_reconstruction(valid_samples):
    for s in valid_samples:
        if isinstance(s, str):
            assert s.startswith(str(Sample(s)))


def test_full_reconstruction(valid_samples):
    for s in valid_samples:
        if isinstance(s, str):
            assert s == repr(Sample(s))


def test_file_extension(file_names):
    for fi, z, ext in file_names:
        assert Sample(fi).file_extension(z) == ext


def test_hashed(valid_samples):
    for s in valid_samples:
        assert Sample(s).hash() != str(Sample(s))


def test_modified(valid_samples):
    for s in valid_samples:
        sample = Sample(s)
        assert not sample.is_modified
        sample.id1 = '0101010101'
        assert sample.is_modified


def test_file_paths(file_paths):
    for s, is_file, path in file_paths:
        sample = Sample(s)
        assert sample.is_file == is_file
        assert sample.path == path
        if isinstance(s, str):
            assert s == repr(sample)
