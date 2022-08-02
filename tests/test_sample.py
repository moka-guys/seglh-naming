import pytest

from seglh_naming.sample import Sample


@pytest.fixture
def valid_samples():
    return [
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_S12_R1_001",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000_RJZ_S12_R1",
        "NGS123_12_382398_JD_M_VCP0R33_Pan0000",
        "NGS123_12_382398_PT324B_VCP0R33_Pan0000_S12_R1"
    ]

@pytest.fixture
def invalid_samples():
    return [
        "NGS123_12_382398_PT324B_VCP0R33_Pan0000b_S12",
        "NGS123_12_382398_VCP0R33_Pan0000",
        "NGS123_12_382398_JD_M_VCP0R33_Pan000a_S12_R1",
        "NGS123_12_382398_PT324B_Pan0000_S12_R1",
        "NGS123_12_382398_PT324B_Pn0000_S12_R1",
        "NGS123_12_382398_Pan0000_S12_R1"
    ]


def test_invalid_samples(invalid_samples):
    for samplename in invalid_samples:
        with pytest.raises(ValueError):
            Sample(samplename)


def test_valid_samples(valid_samples):
    assert all([Sample(s) for s in valid_samples])


def test_reconstruction(valid_samples):
    for s in valid_samples:
        assert s.startswith(str(Sample(s)))


def test_hashed(valid_samples):
    for s in valid_samples:
        assert Sample(s).hash() != str(Sample(s))


def test_modified(valid_samples):
    for s in valid_samples:
        sample = Sample(s)
        assert not sample.is_modified
        sample.id1 = '0101010101'
        assert sample.is_modified
