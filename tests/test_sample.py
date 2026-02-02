import pytest

from seglh_naming.sample import Sample

####################
# FIXTURES #########
####################

@pytest.fixture
def valid_samples():
    return [
        "ONC22070-05-222662-2232170-SWIFT57-Pan4082",  # ONC sample
        "SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009",  # SNP sample
        "ADX22051-04-222656-2231985-NSCLC-Pan4396",  # ADX sample
        "NGS514B-29-287637-LE-M-VCP1R134StG-Pan4821",  # Custom panels sample
        "NGS514ARpt-06-286962-HS-M-WES87SKIN-Pan4940",  # WES skin sample
        "TSO22039-04-222480-2230347-Pan5085",  # Recent TSO sample
        "SNP70-110-265254-4031238805-DM-M-SNPIDv2-Pan4009",
        "ADX22050-20-222643-2231675-CRC-Pan4396",
        "NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1",
        "NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001",
        "NGS123-12-382398-JD-M-VCP0R33-Pan0000-RJZ_S12_R1",
        "NGS123-12-382398-JD-M-VCP0R33-Pan0000.fasta",
        "NGS123-12-382398-265254-VCP0R33-Pan0000_S12_R1",
        "NGS123-12-382398-265ER254-VCP0R33-Pan0000_S12_R1",
        "TSO123-00-234234-9872349-UP01-Pan4969_CopyNumberVariants.vcf",
        "NGS123-00-234234-123456789123456-UP01-Pan4969",  # Non-tso longer than tso requirements
        "ONC123-00-234234-123243-Pan0000.realign.bam",
        "DMLPA001-00-000000-00000-XX-U-dmlpa-Pan5098",  # Proposed digital MPLA fastq name
        "TSO22039-01-220246-HD200-Pan5085",
        "NGS514ARpt-08-136819-NA12878-U-WES87SKIN-Pan4940",
        "ONC22067-02-000000-NTC000-SWIFT57-Pan4082",
        "TSO22040-12-222704-NA000-Pan5085",
        "TSO22040-48-228291-4232-Pan5085",
        "ONC22070-05-222662-2232170-SWIFT57-Pan4082",
        "ADX22050-01-221975-SC07100496-MpxFFPEControl-Pan4396",
        "ADX22050-01-221975-SC07100496-FFPEControl-Pan4396",
        "NGS463-39-88997-RM-F-VCP2R208ViaGP02-Pan4149",
        "NGS372-22-6113-NF-F-VCP2R208Via-Pan4011",
    ]

@pytest.fixture
def valid_dict_samples():
    return [
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
        "NG123-12-382398-265254-VCP0R33-Pan0000_S12",  # Incorrect library prep id format (needs 3 letters)
        "NGS123-382398-265254-VCP0R33-Pan0000_S12",  # Missing sample count
        "NGS123--382398-265254-VCP0R33-Pan0000_S12",  # Missing sample count (/2 underscores)
        "SNP70-1100-265254-4031238805-DM-M-SNPIDv2-Pan4009",  # Sample count too high
        "NGS123-12--382398-265254-VCP0R33-Pan0000_S12",  # Double underscore
        "NGS123-12-388-265254-VCP0R33-Pan0000_S12",  # Invalid specimen number
        "ONC22070-05-EK222662-2232170-SWIFT57-Pan4082",  # Invalid specimen number (not numeric)
        "NGS123-12-382398-PT3-VCP0R33-Pan0000_S12",  # Invalid secondary identifier
        "NGS123-12-382398-J-M-VCP0R33-Pan0000_S12_R1",  # Invalid initials
        "NGS123-12-382398-J3-M-VCP0R33-Pan0000_S12_R1",  # Invalid initials
        "NGS123-12-382398-J-M-VCP0R33-Pan0000_S12_R1",  # Invalid sex
        "NGS123-12-382398-J-M-A1-Pan0000_S12_R1",  # Invalid panel name
        "NGS123-12-382398-JD-M-VCP0R33-Pan000a_S12_R1",  # Invalid pan no
        "NGS123-12-382398-JD-M-VCP0R33-Pan_S12_R1",  # Invalid pan no
        "NGS123-12-382398-JD-M-VCP0R33-Pan1_S12_R1",  # Invalid pan no
        "NGS123-12-382398-265254-Pn0000_S12_R1",  # Invalid pan no
        "NGS123-12-382398-JD-M-VCP0R33-Pan12_S12_R1.v$f",  # Invalid characters in remainder of parsed string
        "NGS514B-29-LE-VCP1R134StG-Pan4821",  # Not enough identifiers
        "ONC22070-05-2232170-Pan4082",  # Not enough identifiers
        "NGS123-12-382398-Pan0000_S12_R1",  # Not enough identifiers
        "NGS514B-29-287637-M-VCP1R134StG-Pan4821",  # Not enough identifiers
        "TSO123-00-234234-TOOLONGNAMEFORTSO-UP01-Pan4969",  # Name too long for tso requirements
        "TSO22040-12-222704-NA-Pan5085",  # Disallowed id2
        "ONC22067-01-NTCcon-57G-SWIFT57-Pan4082",  # Disallowed id1 and id2
        "ONC22070-05-EK222662-2232170-SWIFT57-Pan4082",  # Disallowed id1
        "TSO22040-48-T228291-HO4232-Pan5085",  # Disallowed id1 and id2
        "ADX22050-01-221975-Mpx-FFPEControl-Pan4396",  # Disallowed id2
        "SNP70-11-265254-4031238_805-DM-M-SNPIDv2-Pan4009",  # Disallowed id2
        "ONC22067-02-000000-NT000-SWIFT57-Pan4082",  # Disallowed id2
        "NGS372-22-611-NF-F-VCP2R208Via-Pan4011",  # ID1 too short
    ]


@pytest.fixture
def invalid_dict_samples():
    return [
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
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'libraryprep', 'SNP70'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'samplecount', '11'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'id1', '265254'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'id2', '4031238805'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'initials', 'DM'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'sex', 'M'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'panelname', 'SNPIDv2'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'panelnumber', 'Pan4009'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'ods', 'RJZ'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'samplesheetindex', 'S12'),
        ("SNP70-11-265254-4031238805-DM-M-SNPIDv2-Pan4009-RJZ_S12_R1", 'readnumber', 'R1'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000.fasta", 'initials', 'JD'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000.fasta", 'sex', 'M'),
        ("NGS123-12-382398-265254-VCP0R33-Pan0000_S12_R1", 'sex', None)
    ]

@pytest.fixture
def file_names():
    return [
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.realigned.bam",
         True, 'bam'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.realigned.bam",
         False, 'bam'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.re.xxx.vcf.gz",
         True, 'vcf.gz'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.re.xxx.vcf.gz",
         False, 'vcf'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R2_001.fastq.gz",
         True, 'fastq.gz'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R2_001.fastq.gz",
         False, 'fastq'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.haplotyper.vcf",
         True, 'vcf'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.haplotyper.vcf",
         False, 'vcf'),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000.haplotyper.vcf",
         False, 'vcf'),
    ]

@pytest.fixture
def file_paths():
    return [
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001.haplotyper.vcf",
         True, ''),
        ("/some/path/NGS123-12-382398-JD-M-VCP0R33-Pan0000.haplotyper.vcf",
         True, "/some/path"),
        ("/some/path/NGS123-12-382398-JD-M-VCP0R33-Pan0000",
         True, "/some/path"),
        ("NGS123-12-382398-JD-M-VCP0R33-Pan0000_S12_R1_001",
         False, ''),
    ]


@pytest.fixture
def file_dict_paths():
    return [
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
        ("NG123-12-324-265254-VCP0R33-Pan0000_S12", ['LibraryPrep name invalid', 'Specimen/DNA number invalid']),
        ("NG3-12-388-252-CRC-Pan_S12", ['LibraryPrep name invalid',
                                        'Specimen/DNA number invalid', 'Pan Number invalid']),
    ]

####################
# TESTS ############
####################

def test_invalid_samples(invalid_samples):
    for samplename in invalid_samples:
        with pytest.raises(ValueError):
            Sample.from_string(samplename)


def test_invalid_dict_samples(invalid_dict_samples):
    for samplename in invalid_dict_samples:
        with pytest.raises(ValueError):
            Sample.from_dict(samplename)


def test_field_validation(field_validation):
    s = "NGS123-12-382398-003245-VCP0R33-Pan0000_S12_R1"
    for match_exception, field, value in field_validation:
        sample = Sample.from_string(s)
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
                Sample.from_string(samplename)


def test_valid_samples(valid_samples):
    assert all([Sample.from_string(s) for s in valid_samples])


def test_valid_dict_samples(valid_dict_samples):
    assert all([Sample.from_dict(s) for s in valid_dict_samples])


def test_constituents(constituents):
    for fi, c, result in constituents:
        assert getattr(Sample.from_string(fi), c) == result


def test_sample_reconstruction(valid_samples):
    for s in valid_samples:
        if isinstance(s, str):
            assert s.startswith(str(Sample.from_string(s)))


def test_full_reconstruction(valid_samples):
    for s in valid_samples:
        if isinstance(s, str):
            assert s == repr(Sample.from_string(s))


def test_file_extension(file_names):
    for fi, z, ext in file_names:
        assert Sample.from_string(fi).file_extension(z) == ext


def test_hashed(valid_samples):
    for s in valid_samples:
        assert Sample.from_string(s).hash() != str(Sample.from_string(s))


def test_modified(valid_samples):
    for s in valid_samples:
        sample = Sample.from_string(s)
        assert not sample._is_modified
        sample.id1 = '0101010101'
        assert sample._is_modified


def test_file_paths(file_paths):
    for s, is_file, path in file_paths:
        sample = Sample.from_string(s)
        assert sample.is_file == is_file
        assert sample.path == path
        if isinstance(s, str):
            assert s == repr(sample)


def test_file_dict_paths(file_dict_paths):
    for s, is_file, path in file_dict_paths:
        sample = Sample.from_dict(s)
        assert sample.is_file == is_file
        assert sample.path == path
        if isinstance(s, str):
            assert s == repr(sample)
