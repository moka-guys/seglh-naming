'''
Builds, reads and validates SEGLH samplesheet naming conventions
'''

import os
import sys
import re
import hashlib

# salt used to generate anonymised function'
SALT = 'jdhFeducf2gkFb2jj7hjs345klosboiydbo73u7g390yubfkd'

# 211008_A01229_0040_AHKGTFDRXY_SampleSheet
# samplesheet name regular expression
SAMPLE_REGEX = (
    r'([\d]+)_' # date_
    r'([^_]+)_' # sequencerid_
    r'([\d]+)_' # autoincrno_
    r'([\w-]+)_' # flowcellid_
    r'([sS][\w]+)' # samplesheet
    r'(.[\w]+)' # fileext
    )

# samplesheet name constituent field order
SAMPLESHEET_FIELDS = [
    'date',
    'sequencerid',
    'autoincrno',
    'flowcellid',
    'samplesheetstr',
    'fileext'
]


class Samplesheet(object):
    def __init__(self, **kwargs):
        '''
        parses the samplesheet name (or file name)
        calls the builder which validates each element
        '''
        self._path = kwargs.get('path')
        self._build_name(kwargs)
        self._is_modified=False

    def __setattr__(self, key, value):
        if key != '_is_modified':
            self._is_modified = True
        super(Samplesheet, self).__setattr__(key, value)

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
            constituents = dict(zip(SAMPLESHEET_FIELDS, m.groups()))
            constituents['name'] = name
            constituents['path'] = path
            return cls(**constituents)

    def _build_name(self, constituents):
        '''
        build samplesheet name string
        validate construct and each constituent element
        aggregates errors for different fields
        '''
        collected_errors = []
        for field in SAMPLESHEET_FIELDS:
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

    def __str__(self):
        '''
        Returns the samplesheet name
        '''
        return "_".join(filter(lambda x: x, [
            self.date,
            self.sequencerid,
            self.autoincrno,
            self.flowcellid,
            self.samplesheetstr
        ])) + self.fileext

    def __repr__(self):
        '''
        returns the full parsed string
        '''
        filename = "_".join(filter(lambda x: x, [
            self.date,
            self.sequencerid,
            self.autoincrno,
            self.flowcellid,
            self.samplesheetstr
        ])) + self.fileext
        return os.path.join(self.path, filename)

    def hash(self):
        '''
        A stable cryptographic hash to obfuscate samplesheet name if required
        '''
        s = str(self) + SALT
        s_encoded = s.encode('utf-8')
        h = hashlib.new('sha256')
        h.update(s_encoded)
        return h.hexdigest()

    # check if any elment has been modified
    @property
    def is_modified(self):
        '''
        returns True if any constituent part of the samplesheet name
        has been modified after the initial parsing
        '''
        return self._is_modified

    # check if is a  file name
    @property
    def is_file(self):
        '''
        indicate if was built from file/path (inferred)
            bool
        '''
        return bool(self.path)

    @property
    def path(self):
        '''
        File path (if initialised from string)
            string
        '''
        return self._path

    # value properties
    @property
    def date(self):
        '''
        Date
        '''
        return self._date

    @date.setter
    def date(self, value):
        if not re.match(r'^[\d]{6}$', value):
            raise ValueError("Date invalid ({})".format(value))
        self._date = value

    @property
    def sequencerid(self):
        '''
        Sequencer identifier
            Alphanumeric string that may contain hyphen
        '''
        return self._sequencerid

    @sequencerid.setter
    def sequencerid(self, value):
        if not re.match(r'^[A-Z0-9]+$', value):
            raise ValueError("Sequencer ID invalid ({})".format(value))
        self._sequencerid = value

    @property
    def autoincrno(self):
        '''
        Auto-incrementing number
            4 digits
        '''
        return self._autoincrno

    @autoincrno.setter
    def autoincrno(self, value):
        if not re.match(r'^\d{4}$', value):
            raise ValueError("Autoincrementing number invalid ({})".format(value))
        self._autoincrno = value

    @property
    def flowcellid(self):
        '''
        Flowcell ID:
            Alpha numeric string
        '''
        return self._flowcellid

    @flowcellid.setter
    def flowcellid(self, value):
        if value and not re.match(r'^[0]{9}-[A-Z0-9]{5}|[A-Z0-9]{10}$', value):
            raise ValueError("Flowcell ID invalid ({})".format(value))
        self._flowcellid = value

    @property
    def samplesheetstr(self):
        '''
        SampleSheet string:
            String matching 'SampleSheet' exactly
        '''
        return self._samplesheetstr

    @samplesheetstr.setter
    def samplesheetstr(self, value):
        if value and not re.match(r'^SampleSheet$', value):
            raise ValueError("SampleSheet string invalid ({})".format(value))
        self._samplesheetstr = value

    @property
    def fileext(self):
        '''
        File extension:
            String matching '.csv' exactly
        '''
        return self._fileext

    @fileext.setter
    def fileext(self, value):
        if value and not re.match(r'^.csv$', value):
            raise ValueError("File extension invalid ({})".format(value))
        self._fileext = value


if __name__ == "__main__":
    Samplesheet(sys.argv[1])