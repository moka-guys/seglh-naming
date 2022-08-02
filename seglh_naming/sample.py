import re
import hashlib


SALT = 'jdhFeducf2gkFb2jj7hjs345klosboiydbo73u7g390yubfkd'

SAMPLE_REGEX = (
    r'([^_]+)_(\d+)_([^_]+)'  # Library_number_DNA
    r'(?:_([^_]{4,}))?(?:_([^_]{2}))?(?:_([MFU]{1}))?'  # secondary identifiers
    r'_([^_]+)'  # Human readable panel name
    r'_(Pan[^_]+)'  # pan number
    r'(?:_(R[A-Z0-9]{2}))?'  # ODS code
    r'(?:_(S\d+)_(R\d))?'  # samplesheet number and read number
    r'(?:_(001))?'  # demultiplex lane
    r'(.*)$'  # can be followed by more (eg from a filename)
)


class Sample:
    def __init__(self, name):
        self._name = name
        self.parse_name(name)

    def parse_name(self, name):
        m = re.match(SAMPLE_REGEX, name)
        try:
            assert m
        except AssertionError:
            raise ValueError('Wrong naming format')
        else:
            self.libraryprep = m.group(1)
            self.samplecount = m.group(2)
            self.id1 = m.group(3)
            # seconday identifiers
            self.id2 = m.group(4)
            self.initials = m.group(5)
            self.sex = m.group(6)
            # panel
            self.panelname = m.group(7)
            self.panelnumber = m.group(8)
            # optional
            self.ods = m.group(9)
            self.samplesheetindex = m.group(10)
            self.readnumber = m.group(11)
            self.lane = m.group(12)
            self.rest = m.group(13)

        # validate completeness (at least one secondary identifier)
        try:
            assert self.satisfies_requirements()
        except AssertionError:
            raise ValueError('Nomenclature requirements not satisfied')

    def satisfies_requirements(self):
        '''checks if sample name contains at least 2 patient identifiers'''
        # min 2 identifiers
        return self.id1 and (self.id2 or self.initials or self.sex)

    def __str__(self):
        '''Returns the sample name excluding any demultiplex additions'''
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
        '''returns the pull parsed string'''

    def hash(self):
        s = str(self)+SALT
        s_encoded = s.encode('utf-8)')
        h = hashlib.new('sha256')
        h.update(s_encoded)
        return h.hexdigest()

    # check if any elment has been modified
    @property
    def is_modified(self):
        return not self._name.startswith(str(self))

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
        if not re.match(r'[A-Z]{3,}\d+\w*', value):
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
        if not re.match(r'\d{2}$', value):
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
        if not re.match(r'\w{4,}', value):
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
        if value and not re.match(r'\w{4,}$', value):
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
        if value and not re.match(r'[A-Z]{2}$', value):
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
        if value and not re.match(r'[MFU]$', value):
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
        if not re.match(r'\w{4,}$', value):
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
        if not re.match(r'Pan\d{2,}$', value):
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
        if value and not re.match(r'R\w{2}$', value):
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
        if value and not re.match(r'S\d+$', value):
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
        if value and not re.match(r'[RI]\d$', value):
            raise ValueError("Readnumber invalid ({})".format(value))
        self._readnumber = value

    @property
    def lane(self):
        '''
        Lane Number from demultiplexing
            three digit number
        '''
        return self._lane

    @lane.setter
    def lane(self, value):
        if value and not re.match(r'\d{3}$', value):
            raise ValueError("Lane number invalid ({})".format(value))
        self._lane = value

    @property
    def rest(self):
        '''
        Remainder of the parsed string (e.g. rest of filename)
            a string of any length
        '''
        return self._rest

    @rest.setter
    def rest(self, value):
        if value and not re.match(r'[\w\._]*$', value):
            raise ValueError("Unrecognised characters in parsed name ({})".format(value))
        self._rest = value
