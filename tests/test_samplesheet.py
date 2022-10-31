import pytest
from seglh_naming.samplesheet import Samplesheet

####################
# FIXTURES #########
####################

@pytest.fixture
def valid_samplesheets():
    return [
        '211008_A01229_0040_AHKGTFDRXY_SampleSheet.csv',
        '211015_M02353_0632_000000000-K242J_SampleSheet.csv',
        '210827_M02353_0614_000000000-JRLLW_SampleSheet.csv',
        '220331_M02631_0249_000000000-K66RM_SampleSheet.csv',
        '220401_M02353_0676_000000000-K4669_SampleSheet.csv',
        '220401_NB551068_0457_AHJYL5AFX3_SampleSheet.csv',
        '220401_NB552085_0188_AHJWL5AFX3_SampleSheet.csv'
    ]

@pytest.fixture
def invalid_samplesheets():
    return [
        '21108_A01229_0040_AHKGTFDRXY_SampleSheet.csv',
        '21aA08_A01229_0040_AHKGTFDRXY_SampleSheet.csv',
        '2110915_M02353_0632_000000000-K242J_SampleSheet.csv',
        '220401_NB55a1068_0457_AHJYL5AFX3_SampleSheet.csv',
        '220401_NB55-1068_0457_AHJYL5AFX3_SampleSheet.csv',
        '211015_M02353_032_000000000-K242J_SampleSheet.csv',
        '211015_M02353_06324_000000000-K242J_SampleSheet.csv',
        '211015_M02353_0a632_000000000-K242J_SampleSheet.csv',
        '211008_A01229_0040_AHKGTaDRXY_SampleSheet.csv',
        '211008_A01229_0040_AHKGT$DRXY_SampleSheet.csv',
        '211015_M02353_0632_000_000000-K242J_SampleSheet.csv',
        '211015_M02353_0632_000000000-K242J_SampleSheet2.csv',
        '211015_M02353_0632_000000000-K242J_Samplesheet.csv',
        '211015_M02353_0632_000000000-K242J_SampleSheet.cv',
    ]


@pytest.fixture
def constituents():
    return [('211008_A01229_0040_AHKGTFDRXY_SampleSheet.csv', 'date', '211008'),
            ('211015_M02353_0632_000000000-K242J_SampleSheet.csv', 'sequencerid', 'M02353'),
            ('210827_M02353_0614_000000000-JRLLW_SampleSheet.csv', 'autoincrno', '0614'),
            ('220331_M02631_0249_000000000-K66RM_SampleSheet.csv', 'flowcellid', '000000000-K66RM'),
            ('220401_NB552085_0188_AHJWL5AFX3_SampleSheet.csv', 'flowcellid', 'AHJWL5AFX3'),
            ('220401_M02353_0676_000000000-K4669_SampleSheet.csv', 'samplesheetstr', 'SampleSheet'),
            ('220401_NB551068_0457_AHJYL5AFX3_SampleSheet.csv', 'fileext', '.csv'),
    ]


@pytest.fixture
def file_paths():
    '''
    samplesheet, is_file, path
    '''
    return [
        ('211008_A01229_0040_AHKGTFDRXY_SampleSheet.csv', ''),
        ('/some/path/211015_M02353_0632_000000000-K242J_SampleSheet.csv', '/some/path'),
        ('/some/path/220401_NB552085_0188_AHJWL5AFX3_SampleSheet.csv', '/some/path')
    ]


@pytest.fixture
def field_validation():
    return [(None, 'date', '211008'),
            ('Date invalid', 'date', '21008'),
            ('Date invalid', 'date', '21aA08'),
            (None, 'sequencerid', 'M02353'),
            ('Sequencer ID invalid', 'sequencerid', 'NB55a1068'),
            ('Sequencer ID invalid', 'sequencerid', 'NB55-1068'),
            (None, 'autoincrno', '0614'),
            ('Autoincrementing number invalid', 'autoincrno', '032'),
            ('Autoincrementing number invalid', 'autoincrno', 'abC'),
            ('Autoincrementing number invalid', 'autoincrno', '06324'),
            (None, 'flowcellid', '000000000-K66RM'),
            (None, 'flowcellid', 'AHJWL5AFX3'),
            ('Flowcell ID invalid', 'flowcellid', 'AHKGTaDRXY'),
            ('Flowcell ID invalid', 'flowcellid', 'AHKGT$DRXY'),
            ('Flowcell ID invalid', 'flowcellid', '000_000000-K242J'),
            (None, 'samplesheetstr', 'SampleSheet'),
            ('SampleSheet string invalid', 'samplesheetstr', 'SampleSheet2'),
            ('SampleSheet string invalid', 'samplesheetstr', 'Samplesheet'),
            (None, 'fileext', '.csv'),
            ('File extension invalid', 'fileext', '.cv'),
    ]


@pytest.fixture
def multiple_errors():
    return [
        ("21108_A01229_00_AHKGTFDRXY_SampleSheet.csv",
         ['Date invalid', 'Autoincrementing number invalid']),
        ("220401_NB55-1068_0457_AHJYL5AFX3_SampleSheet2.cv",
         ['Sequencer ID invalid', 'SampleSheet string invalid', 'File extension invalid']),
    ]

####################
# TESTS ############
####################


def test_valid_samplesheets(valid_samplesheets):
    assert all([Samplesheet.from_string(s) for s in valid_samplesheets])


def test_invalid_samplesheet(invalid_samplesheets):
    for samplesheet in invalid_samplesheets:
        with pytest.raises(ValueError):
            Samplesheet.from_string(samplesheet)


def test_field_validation(field_validation):
    s = '211008_A01229_0040_AHKGTFDRXY_SampleSheet.csv'
    for match_exception, field, value in field_validation:
        samplesheet = Samplesheet.from_string(s)
        if match_exception:
            with pytest.raises(ValueError, match=match_exception):
                setattr(samplesheet, field, value)
        else:
            setattr(samplesheet, field, value)
            assert getattr(samplesheet,field) == value


def test_multiple_errors(multiple_errors):
    for s, match_exceptions in multiple_errors:
        for item in match_exceptions:
            with pytest.raises(ValueError, match=item):
                Samplesheet.from_string(s)


def test_constituents(constituents):
    for fi, c, result in constituents:
        assert getattr(Samplesheet.from_string(fi), c) == result


def test_samplesheet_reconstruction(valid_samplesheets):
    for s in valid_samplesheets:
        if isinstance(s, str):
            assert s.startswith(str(Samplesheet.from_string(s)))


def test_full_reconstruction(valid_samplesheets):
    for s in valid_samplesheets:
        if isinstance(s, str):
            assert s == repr(Samplesheet.from_string(s))


def test_hashed(valid_samplesheets):
    for s in valid_samplesheets:
        assert Samplesheet.from_string(s).hash() != str(Samplesheet.from_string(s))


def test_modified(valid_samplesheets):
    for s in valid_samplesheets:
        samplesheet = Samplesheet.from_string(s)
        assert not samplesheet._is_modified
        samplesheet.date = '221008'
        assert samplesheet._is_modified


def test_file_paths(file_paths):
    for s, path in file_paths:
        samplesheet = Samplesheet.from_string(s)
        assert samplesheet.path == path
        if isinstance(s, str):
            assert s == repr(samplesheet)