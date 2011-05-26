''' IBAN functions and International Accounts '''
import os.path
import string
import ConfigParser
import ibanlib

cfg_filename = 'iban_countries.cfg'
cfg_file = os.path.join(
    os.path.split(ibanlib.__file__)[0],
    cfg_filename)

cfg_countries = ConfigParser.ConfigParser()
cfg_countries.read(cfg_file)


class IBANError(Exception):
    pass


def containsOnly(seq, aset):
    """ Check if sequence "seq" contains ONLY letters in set "aset" """
    for c in seq:
        if c not in aset: 
            return False
    return True


class FormatSpec(object):
    """ Describes format of iban items """
    min = None
    max = None
    type = None
    fillchar = None
    fill_left = True
    
    def __init__(self, config):
        """ Initialize object according to config string """

        allchars = string.maketrans('','')
        #account = 4/11, n, 0
        config = config.strip().translate(allchars, ' ')
        # Split the configuration
        config = config.split(',')
        # Read min/max
        l = config[0].split('/')
        if len(l) == 1:
            self.min = self.max = int(l[0])
        elif len(l) == 2:
            self.min = int(l[0])
            self.max = int(l[1])
        else:
            raise IBANError('Error in configuration file')
        # Read encoding
        if config[1] == 'n':
            self.type = string.digits
        elif config[1] == 'a':
            self.type = string.ascii_letters
        elif config[1] == 'an':
            self.type = string.digits + string.ascii_letters
        else:
            raise IBANError('Error in configuration file')
        # Read Fill chars, if available
        if len(config) > 2:
            self.fillchar = config[2]

    def valid(self, buf):
        """ Check if given string applies to the format """
        # Length
        if len(buf) < self.min or len(buf) > self.max:
            return False
        elif not containsOnly(buf, self.type):
            return False
        else:
            return True

    def _fill(self, buf, fillno):
        """ Fill string with fill characters """
        if self.fillchar is None:
            # If no fillchars are defined, there's no filling
            return buf
        if self.fill_left:
            return buf.rjust(fillno, self.fillchar)
        else:
            return buf.ljust(fillno, self.fillchar)

    def fill(self, buf):
        """ Fill string with fill characters up to maximum length """
        return self._fill(buf, self.max)
    
    def minfill(self, buf):
        """ Fill string with fill characters up to minimum length """
        return self._fill(buf, self.min)

    def strip(self, buf):
        """Strip all fill characters from buf"""
        if not self.fillchar:
            # If no fillchars are defined, there's no stripping
            return buf
        if self.fill_left:
            buf = buf.lstrip(self.fillchar)
        else:
            buf = buf.rstrip(self.fillchar)
        return buf
        

def checksum(iban):
    """
    Calculate Checksum of a *wellformed* IBAN
    Basically this is just a 'IBAN mod 97' but this is not so easy
    as older python versions/systems cannot handle very long integers
    """
    lbuf = []

    # first 4 chars to the end
    buf = iban[4:] + iban[:2] + iban[2:4]

    # Convert letters into digits
    # 'A' -> 10, 'B' -> 11, ... 'Z' -> 35

    for i in buf:
        if i in string.digits:
            lbuf.append(i)
        else:
            lbuf.append(str(10 + ord(i) - ord('A')))

    # transform list to string
    ibannum = long(''.join(lbuf))

    return ibannum % 97

def get_country_specs(country):
    """ Read country specifics, check and return them as a dictionary """
    
    try:
        country_specs = dict(cfg_countries.items(country))
    except ConfigParser.NoSectionError:
        # No configuration for this country
        raise IBANError('Country %s not implemented' % country)
    # Check bank, branche, account, check
    for k in ['bank', 'branche', 'account', 'check1', 'check2', 'check3']:
        try:
            f = country_specs[k]
        except KeyError:
            raise IBANError(
                'Missing parameter "%s" in configuration, '
                'section %s' % (k, country))
        if f:
            try:
                country_specs[k] = FormatSpec(f)
            except IBANError:
                raise IBANError(
                    'Wrong format specifier for %s in configuration, '
                    'section %s' % (k,country))
        else:
            # Empty specifier
            country_specs[k] = None

    # IBAN length
    try:
        f = country_specs['iban_length']
    except KeyError:
        raise IBANError('Missing parameter "iban_length" in configuration, '
                        'section %s' % country)
    country_specs['iban_length'] = int(f)

    # IBAN order
    try:
        f = country_specs['iban_order']
    except KeyError:
        raise IBANError('Missing parameter "iban_order" in configuration, '
                        'section %s' % country)
    l = []
    for i in f.split(','):
        l.append(i.strip())
    country_specs['iban_order'] = l

    # Is country part of SEPA contract?
    f = country_specs.get('sepa', False)
    if isinstance(f, basestring):
        if f.lower() in ['y','yes']:
            f = True
        else:
            f = False
    country_specs['sepa'] = f

    return country_specs

class IntAccount(object):
    """International Bank Account. This class stores all relevant information
    in specific attributes, e.g. account number, domestic bank number, etc.
    The IBAN is built on the fly and is not stored in the object."""

    def __init__(self, country=None, bank=None, branche=None,
                 account=None, check1=None, check2=None, check3=None, 
                 iban=None):
        """ Import country specific configuration """
        # Get country specific formatting
        if not country and not iban:
            raise AttributeError('Country or IBAN is mandatory')
        if iban:
            # If IBAN is specified, use the country from there
            # and ignore the country attribute
            country = iban[:2]
        
        self.country_specs = get_country_specs(country)

        if iban:
            # If there is an IBAN, use that for initializing
            self.country = country
            self.iban = iban  # iban is a property!!!
        else:
            self.country = country
            self.bank = bank
            self.branche = branche
            self.account = account
            self.check1 = check1
            self.check2 = check2
            self.check3 = check3

    def __cmp__(self, other):
        """IntAccounts are equal if country/bank/branche/
        account/checksum are equal"""
        if self.country != other.country:
            return -1
        for i in ['bank', 'branche', 'account', 'check1', 'check2', 'check3']:
            cs = self.country_specs[i]
            os = other.country_specs[i]
            if cs or os:
                if cs.fill(getattr(self,i)) != os.fill(getattr(other,i)):
                    return -1
        # Everything seems to be the same
        return 0

    def __repr__(self):
        return ("IntAccount(country='%s', bank='%s', branche='%s', "
                "account='%s', check1='%s', check2='%s', check3='%s')" % (
                    self.country,
                    self.bank,
                    self.branche,
                    self.account,
                    self.check1,
                    self.check2,
                    self.check3))
    @property
    def is_sepa(self):
        return self.country_specs['sepa']

    def set_iban(self, iban):
        """Set all needed attributes from IBAN"""
        # Check length of IBAN
        if len(iban) != self.country_specs['iban_length']:
            raise IBANError('IBAN has an invalid length')
        # Validate IBAN checksum
        if checksum(iban) != 1:
            raise IBANError('IBAN has an invalid checksum')
        # Now try to write attributes
        pos = 4 # Initial position from where attributes are read
        for attrname in self.country_specs['iban_order']:
            attr_len = self.country_specs[attrname].max
            # Get attribute from iban
            attrstr = iban[pos:pos+attr_len]
            # Strip eventual fill characters
            attrstr = self.country_specs[attrname].strip(attrstr)
            setattr(self, attrname, attrstr)
            pos += attr_len # set new position
        
    def get_iban(self):
        """ Create IBAN out of object attributes """
        # All attributes are valid, nothing has to be checked,
        # just assemble the IBAN
        iban = []
        iban.append(self.country)
        iban.append('00') # Empty Checksum
        # Now append all specified attributes
        for attrname in self.country_specs['iban_order']:
            a = getattr(self, attrname)
            if a == None:
                # Ooops, attribute is None!
                raise IBANError('Attribute %s is missing, no IBAN '
                                'can be created' % attrname)
            else:
                # Fill attribute (e.g. precede account number
                # with zeros) and append it
                iban.append(self.country_specs[attrname].fill(a))
        # Calculate checksum
        c = checksum (''.join(iban))
        # Add Checksum
        iban[1]=str(98 - c).zfill(2)
        return ''.join(iban)
        
    iban = property(get_iban, set_iban)

# Modify class, so that it contains property objects
# that validate certain attributes

def valid_get(attr):
    """ Factory for getters for constrained attributes """
    def getx(self):
        return getattr(self, '_'+attr, None)
    return getx

def valid_set(attr):
    """ Factory for setters for constrained attributes which check validity """
    def setx(self, value):
        # Check all constraints
        if value == None:
            # Allow setting attribute to None
            setattr(self, '_'+attr, value)
        else:
            # Fill up to minimum length
            value = self.country_specs[attr].minfill(value)
            if self.country_specs[attr].valid(value):
                setattr(self, '_'+attr, value)
            else:
                raise IBANError('Invalid value "%s" for %s' % (value, attr))
    return setx


for i in ['bank', 'branche', 'account', 'check1', 'check2', 'check3']:
    setattr(IntAccount, i, property(valid_get(i), valid_set(i)))

def valid(iban):
    """ Check validity of IBAN """
    try:
        i = IntAccount(iban=iban)
    except IBANError:
        return False
    else:
        return True

def valid_BIC(bic):
    """Check validity of BIC"""
    bic = bic.strip()
    if len(bic) != 8 and len(bic) != 11:
        # length must be 8 or 11 characters
        return False
    if not bic[:6].isalpha():
        # Characters 0-6 must be letters
        return False
    if not bic[6:8].isalnum():
        # Characters 7,8 must me alphanumeric
        return False
    # All seems o.k. so far...
    return True
