import pytest

from seglh_naming.sample import Sample

####################
# FIXTURES #########
####################

@pytest.fixture
def valid_samples():
    return [
        "ONC22070_05_222662_2232170_SWIFT57_Pan4082", # ONC sample
        "SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009", # SNP sample
        "ADX22051_04_222656_2231985_NSCLC_Pan4396", # ADX sample
        "NGS514B_29_287637_LE_M_VCP1R134StG_Pan4821", # custom panels sample
        "NGS514ARpt_06_286962_HS_M_WES87SKIN_Pan4940", # WES skin sample
        "TSO22039_04_222480_2230347_Pan5085", # recent TSO sample
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_RJZ_S12_R1",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000.fasta",
        "NGS123_12_382398_265254_VCP0R33_Pan0000_S12_R1",
        "NGS123_12_382398_265ER254_VCP0R33_Pan0000_S12_R1",
        "TSO123_00_234234_9872349_UP01_Pan4969_CopyNumberVariants.vcf",
        "NGS123_00_234234_123456789123456_UP01_Pan4969", # non-tso longer than tso requirements
        "ONC123_00_234234_123243_Pan0000.realign.bam",
        {
            "libraryprep": "ONC123",
            "samplecount": 12,
            "id1": "123456",
            "id2": "123456",
            "initials": "XX",
            "sex": "U",
            "panelname": "PANEL",
            "panelnumber": "Pan0000"
        }
    ]

@pytest.fixture
def invalid_samples():
    return [
        "NG123_12_382398_265254_VCP0R33_Pan0000_S12", # incorrect library prep id format (needs 3 letters)
        "NGS123_382398_265254_VCP0R33_Pan0000_S12", # missing sample count
        "NGS123__382398_265254_VCP0R33_Pan0000_S12", # missing sample count (/2 underscores)
        "NGS123_12__382398_265254_VCP0R33_Pan0000_S12", # double underscore
        "NGS123_12_388_265254_VCP0R33_Pan0000_S12", # invalid specimen number
        "ONC22070_05_EK222662_2232170_SWIFT57_Pan4082",  # Invalid specimen number (not numeric)
        "NGS123_12_382398_PT3_VCP0R33_Pan0000_S12", # invalid secondary identifier
        "NGS123_12_382398_J_M_VCP0R33_Pan0000_S12_R1",  # invalid initials
        "NGS123_12_382398_J3_M_VCP0R33_Pan0000_S12_R1", # invalid initials
        "NGS123_12_382398_J_M_VCP0R33_Pan0000_S12_R1", # invalid sex
        "NGS123_12_382398_J_M_A1_Pan0000_S12_R1", # invalid panel name
        "NGS123_12_382398_JD_M_VCP0R33_Pan000a_S12_R1",  # invalid pan no
        "NGS123_12_382398_JD_M_VCP0R33_Pan_S12_R1",  # invalid pan no
        "NGS123_12_382398_JD_M_VCP0R33_Pan1_S12_R1",  # invalid pan no
        "NGS123_12_382398_265254_Pn0000_S12_R1",  # invalid pan no
        "NGS123_12_382398_JD_M_VCP0R33_Pan12_S12_R1.v$f",  # invalid characters in remainder of parsed string
        "NGS514B_29_LE_VCP1R134StG_Pan4821", # not enough identifiers
        "ONC22070_05_2232170_Pan4082", # not enough identifiers
        "NGS123_12_382398_Pan0000_S12_R1", # not enough identifiers
        "NGS514B_29_287637_M_VCP1R134StG_Pan4821",  # not enough identifiers
        "TSO123_00_234234_TOOLONGNAMEFORTSO_UP01_Pan4969", # name too long for tso requirements
        {
            "libraryprep": "ONC123",
            "samplecount": 12,
            "id1": "123456",
            "sex": "U",
            "panelname": "PANEL",
            "panelnumber": "Pan0000"
        }
    ]

@pytest.fixture
def constituents():
    return [
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'libraryprep', 'SNP70'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'samplecount', '11'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'id1', '265254'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'id2', '4031238805'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'initials', 'DM'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'sex', 'M'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'panelname', 'SNPIDv2'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'panelnumber', 'Pan4009'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'ods', 'RJZ'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'samplesheetindex', 'S12'),
        ("SNP70_11_265254_4031238805_DM_M_SNPIDv2_Pan4009_RJZ_S12_R1", 'readnumber', 'R1'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000.fasta", 'initials', 'JD'),
        ("NGS123_12_382398_JD_M_VCP0R33_Pan0000.fasta", 'sex', 'M'),
        ("NGS123_12_382398_265254_VCP0R33_Pan0000_S12_R1", 'sex', None)
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
            "id1": "123456",
            "id2": "123456",
            "initials": "XX",
            "sex": "U",
            "panelname": "PANEL",
            "panelnumber": "Pan0000"
        }, False, '')
    ]

@pytest.fixture
def field_validation():
    return [
        (None, 'libraryprep', 'NGS232b'),
        ('LibraryPrep name invalid', 'libraryprep', 'NGS234_'),
        ('LibraryPrep name invalid', 'libraryprep', 'NS232'),
        (None, 'samplecount', '12'),
        ('SampleCount invalid', 'samplecount', '1_2'),
        ('SampleCount invalid', 'samplecount', '12_'),
        (None, 'id1', '123456'),
        ('Specimen/DNA number invalid', 'id1', 'AM1'),
        ('Specimen/DNA number invalid', 'id1', 'a3'),
        ('Specimen/DNA number invalid', 'id1', '3_4'),
        (None, 'id2', '289567'),
        ('Secondary identifier invalid', 'id2', '287'),
        ('Secondary identifier invalid', 'id2', '_287'),
        (None, 'initials', 'RD'),
        ('Initials invalid', 'initials', 'R'),
        ('Initials invalid', 'initials', '2'),
        (None, 'sex', 'M'),
        ('Sex invalid', 'sex', 'B'),
        ('Sex invalid', 'sex', '_'),
        (None, 'panelname', '289567'),
        (None, 'panelname', 'VCP1R33'),
        ('Panel Name invalid', 'panelname', 'VCP1_R33'),
        (None, 'panelnumber', 'Pan1111'),
        ('Pan Number invalid', 'panelnumber', 'Pan1'),
        ('Pan Number invalid', 'panelnumber', 'Pan111_'),
        (None, 'ods', 'R35'),
        ('Unknown or invalid ODS code', 'ods', 'VCP1_R33'),
        ('Unknown or invalid ODS code', 'ods', 'B35'),
        (None, 'samplesheetindex', 'S12'),
        ('Samplesheet index invalid', 'samplesheetindex', '12'),
        (None, 'readnumber', 'R2'),
        (None, 'readnumber', 'I2'),
        ('Readnumber invalid', 'readnumber', 'I29'),
        (None, 'stable', '001'),
        ('Number invalid', 'stable', '2'),
        ('Number invalid', 'stable', 'er'),
        (None, 'rest', '.fastq.gz'),
        (None, 'rest', '_corrupted.fastq.gz'),
        ('Unrecognised characters in parsed name', 'rest', '0-01'),
    ]


@pytest.fixture
def multiple_errors():
    return [
        ("NG123_12_324_265254_VCP0R33_Pan0000_S12", ['LibraryPrep name invalid', 'Specimen/DNA number invalid']),
        ("NG3_12_388_252_VC3_Pan_S12", ['LibraryPrep name invalid', 'Specimen/DNA number invalid',
                                    'Secondary identifier invalid', 'Panel Name invalid', 'Pan Number invalid']),
    ]

####################
# TESTS ############
####################

def test_invalid_samples(invalid_samples):
    for samplename in invalid_samples:
        with pytest.raises(ValueError):
            Sample(samplename)


def test_field_validation(field_validation):
    s = "NGS123_12_382398_003245_VCP0R33_Pan0000_S12_R1"
    for match_exception, field, value in field_validation:
        sample = Sample(s)
        if match_exception:
            with pytest.raises(ValueError, match=match_exception):
                setattr(sample, field, value)
        else:
            setattr(sample, field, value)
            assert getattr(sample,field) == value


def test_multiple_errors(multiple_errors):
    for samplename, match_exceptions in multiple_errors:
        for item in match_exceptions:
            with pytest.raises(ValueError, match=item):
                Sample(samplename)
                

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