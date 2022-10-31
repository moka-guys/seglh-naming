'''
Builds, reads and validates SEGLH sample/analysis naming conventions
'''

import os
import sys
import re
import hashlib

# salt used to generate anonymised function'
SALT = 'jdhFeducf2gkFb2jj7hjs345klosboiydbo73u7g390yubfkd'

# sample_name regular expression
SAMPLE_REGEX = (
    r'([^_]+)_(\d+)_(\d[^_]+)'  # Library_number_DNA
    r'(?:_(\d[^_]+))?(?:_([^_]{2}))?(?:_([A-Za-z]))?'  # secondary identifiers
    r'(?:_([^_]+))?'  # Human readable panel name
    r'_(Pan[^_\.]*)'  # pan number
    r'(?:_(R[A-Z0-9]{2}))?'  # ODS code
    r'(?:_(S\d+)_(R\d))?'  # samplesheet number and read number
    r'(?:_([0-9]{3}))?'  # demultiplex stable number
    r'(.*)$'  # can be followed by more (eg from a filename)
)

# sample name constituent field order
SAMPLE_FIELDS = [
    'libraryprep',
    'samplecount',
    'id1',
    'id2',
    'initials',
    'sex',
    'panelname',
    'panelnumber',
    'ods',
    'samplesheetindex',
    'readnumber',
    'stable',
    'rest'
]


class Sample(object):
    def __init__(self, **kwargs):
        '''
        parses the sample name (or file name)
        calls the builder which validates each element
        '''
        self._path = kwargs.get('path')
        self._build_name(kwargs)
        self._is_modified=False
        # validate completeness (at least one secondary identifier)
        self._check_requirements()

    def __setattr__(self, key, value):
        if key != '_is_modified':
            self._is_modified = True
        super(Sample, self).__setattr__(key, value)

    @classmethod
    def from_string(cls, fullname):
        assert isinstance(fullname, str)
        dirs = fullname.split('/')
        name = dirs[-1]
        path = '/'.join(dirs[:-1])
        m = re.match(SAMPLE_REGEX, name)
        try:
            assert m
        except AssertionError:
            raise ValueError('Wrong naming format ({})'.format(name))
        else:
            constituents = dict(zip(SAMPLE_FIELDS, m.groups()))
            constituents['name'] = name
            constituents['path'] = path
            return cls(**constituents)

    @classmethod
    def from_dict(cls, constituents):
        assert isinstance(constituents, dict)
        if constituents.get('path') is None:
            constituents['path'] = ''
        return cls(**constituents)

    def _build_name(self, constituents):
        '''
        build sample name string
        validate construct and each constituent element
        aggregates errors for different fields
        '''
        collected_errors = []
        for field in SAMPLE_FIELDS:
            try:
                if field in constituents.keys() and \
                        constituents[field] is not None:
                    setattr(self, field, str(constituents[field]))
                else:
                    setattr(self, field, None)
            except Exception as e:
                collected_errors.append(str(e))
        if collected_errors:
            raise ValueError(", ".join(collected_errors))

    def _check_requirements(self):
        '''
        checks if sample name contains at least 2 patient identifiers
        checks total identifier length of TSO samples to be below 40 characters
        '''
        # min 2 identifiers
        enough_identifiers = self.id1 and (self.id2 or (self.initials and self.sex))
        if not enough_identifiers:
            raise ValueError('Not enough identifiers in sample name')
        # TSO max 40 characters
        acceptable_length = not self.libraryprep.startswith('TSO') or len(str(self)) <= 40
        if not acceptable_length:
            raise ValueError('TSO sample name too long')

    def __str__(self):
        '''
        Returns the sample name excluding any demultiplex additions
        '''
        return "_".join(filter(lambda x: x, [
            self.libraryprep,
            self.samplecount,
            self.id1,
            self.id2,
            self.initials,
            self.sex,
            self.panelname,
            self.panelnumber,
            self.ods
        ]))

    def __repr__(self):
        '''
        returns the full parsed string
        '''
        filename = "_".join(filter(lambda x: x, [
            self.libraryprep,
            self.samplecount,
            self.id1,
            self.id2,
            self.initials,
            self.sex,
            self.panelname,
            self.panelnumber,
            self.ods,
            self.samplesheetindex,
            self.readnumber,
            self.stable
        ])) + self.rest
        return os.path.join(self.path, filename)

    def file_extension(self, include_compression=True):
        '''
        extracts the file extension if any
        '''
        if not self.rest:
            raise ValueError("Not a file name ({})".format(self.name))
        constituents = self.rest.split('.')
        # check if compressed
        if constituents[-1] in ('gz', 'zip', 'bz2', 'zx') and \
                constituents[-2] and \
                re.match(r'\w{2,5}$', constituents[-2]):
            if include_compression:
                return '.'.join(constituents[-2:])
            else:
                return constituents[-2]
        return constituents[-1]

    def hash(self):
        '''
        A stable cryptographic hash to obfuscate sample name if required
        '''
        s = str(self) + SALT
        s_encoded = s.encode('utf-8)')
        h = hashlib.new('sha256')
        h.update(s_encoded)
        return h.hexdigest()

    # check if any elment has been modified
    @property
    def is_modified(self):
        '''
        returns True if any constituent part of the sample name
        has been modified after the initial parsing
        '''
        return self.is_modified

    # check if is a  file name
    @property
    def is_file(self):
        '''
        indicate if was built from file/path (inferred)
            bool
        '''
        return bool(self.rest) or bool(self.path)

    @property
    def path(self):
        '''
        File path (if initialised from string)
            string
        '''
        return self._path

    # value properties
    @property
    def libraryprep(self):
        '''
        Library preparation name
        Prefix:
            Three+ letter code
        Main:
            number
        Postfix (optional):
            letters (eg. rep, b)
        '''
        return self._libraryprep

    @libraryprep.setter
    def libraryprep(self, value):
        if not re.match(r'^[A-Z]{3,}\d+[a-zA-Z0-9]*$', value):
            raise ValueError("LibraryPrep name invalid ({})".format(value))
        self._libraryprep = value

    @property
    def samplecount(self):
        '''
        Sample index in library preparation:
            couple of ints (two digit number)
        '''
        return self._samplecount

    @samplecount.setter
    def samplecount(self, value):
        if not re.match(r'^\d{2}$', value):
            raise ValueError("SampleCount invalid ({})".format(value))
        self._samplecount = value

    @property
    def id1(self):
        '''
        Specimen or DNA number:
            Alpha numeric string
        '''
        return self._id1

    @id1.setter
    def id1(self, value):
        if not re.match(r'^\d{6,}', value):
            raise ValueError("Specimen/DNA number invalid ({})".format(value))
        self._id1 = value

    @property
    def id2(self):
        '''
        Secondary Patient, Specimen or DNA identifier:
            Alpha numeric string
        '''
        return self._id2

    @id2.setter
    def id2(self, value):
        if value and not re.match(r'^[a-zA-Z0-9-]{5,}$', value):
            raise ValueError("Secondary identifier invalid ({})".format(value))
        self._id2 = value

    @property
    def initials(self):
        '''
        Patient initials:
            couple of chars
        '''
        return self._initials

    @initials.setter
    def initials(self, value):
        if value and not re.match(r'^[A-Z]{2}$', value):
            raise ValueError("Initials invalid ({})".format(value))
        self._initials = value

    @property
    def sex(self):
        '''
        Patient sex:
            single char
        '''
        return self._sex

    @sex.setter
    def sex(self, value):
        if value and not re.match(r'^[MFU]$', value):
            raise ValueError("Sex invalid ({})".format(value))
        self._sex = value

    @property
    def panelname(self):
        '''
        Human readable panel name
            string
        '''
        return self._panelname

    @panelname.setter
    def panelname(self, value):
        if value and not re.match(r'^[a-zA-Z0-9]{4,}$', value):
            raise ValueError("Panel Name invalid ({})".format(value))
        self._panelname = value

    @property
    def panelnumber(self):
        '''
        Panel/routing number
            digits prefixed by Pan
        '''
        return self._panelnumber

    @panelnumber.setter
    def panelnumber(self, value):
        if not re.match(r'^Pan\d{2,}$', value):
            raise ValueError("Pan Number invalid ({})".format(value))
        self._panelnumber = value

    @property
    def ods(self):
        '''
        ODS code:
            Triplet of alphanumeric character
        '''
        return self._ods

    @ods.setter
    def ods(self, value):
        if value and not re.match(r'^R[A-Z0-9]{2}$', value):
            raise ValueError("Unknown or invalid ODS code ({})".format(value))
        self._ods = value

    @property
    def samplesheetindex(self):
        '''
        Samplesheet index (from dmx):
            digits prefixed with S
        '''
        return self._samplesheetindex

    @samplesheetindex.setter
    def samplesheetindex(self, value):
        if value and not re.match(r'^S\d+$', value):
            raise ValueError("Samplesheet index invalid ({})".format(value))
        self._samplesheetindex = value

    @property
    def readnumber(self):
        '''
        Read number in pair
            single digit prefixed by R or I
        '''
        return self._readnumber

    @readnumber.setter
    def readnumber(self, value):
        if value and not re.match(r'^[RI]\d$', value):
            raise ValueError("Readnumber invalid ({})".format(value))
        self._readnumber = value

    @property
    def stable(self):
        '''
        Stable number from demultiplexing
            001
        '''
        return self._stable

    @stable.setter
    def stable(self, value):
        if value and not re.match(r'^001$', value):
            raise ValueError("Number invalid ({})".format(value))
        self._stable = value

    @property
    def rest(self):
        '''
        Remainder of the parsed string (e.g. rest of filename)
            a string of any length
        '''
        return self._rest or ''

    @rest.setter
    def rest(self, value):
        if value and not re.match(r'^[\w\.]*$', value):
            raise ValueError("Unrecognised characters in parsed name ({})"
                             .format(value))
        self._rest = value


if __name__ == "__main__":
    Sample(sys.argv[1])
