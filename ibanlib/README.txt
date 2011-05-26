=========================================================
International Bank Account Number (IBAN) library
=========================================================

The international bank account number (IBAN) consists basically of the
following items:

1) two-letter Country ISO-Code (e.g. 'US', 'DE')
2) two-digit IBAN-Checksum (basically a mod(97))
3) Bank Code (The domestic bank code)
4) Branch Code (For national branches of a bank)
5) Account Number (Bank specific)
6) Bank specific check sum (often part of the account number)

The international bank code (BIC) is NOT part of the IBAN.

The above items are simply concatenated and form the IBAN. However, every
country has its own format of the above items, e.g. in Austria account numbers
are digits only and are between 6 and 11 digits long, which is different in
other countries.

The iban.py module offers an international account object Int_Account, which
stores the above items, checks for validity during creation and provides the
IBAN.

 >>> from ibanlib.iban import IntAccount, valid
 >>> a = IntAccount()
 Traceback (most recent call last):
 AttributeError: Country or IBAN is mandatory
 
The country or IBAN has to be specified during creation, otherwise, the class
does not know the country for which the IBAN specs should be applied.
 
 >>> a=IntAccount('AT')
 >>> a.account = '123456789'
 >>> a.bank = '12345'
 >>> a.bank
 '12345'
 >>> a.bank = '33333'
 >>> a.bank
 '33333'

These attributes are automatically checked, wrong values lead to an IBANError

 >>> a.account = '123ABC'                     # Only digits allowed
 Traceback (most recent call last):
 IBANError: Invalid value "123ABC" for account
 >>> a.account = '12234234234234324234'       # Too long
 Traceback (most recent call last):
 IBANError: Invalid value "12234234234234324234" for account

These object attributes can also be set at object creation time:
 >>> a = IntAccount('AT', bank='12345', account='123456789')
 
If all required attributes of a country are set, the iban may be retrieved

 >>> a.iban
 'AT141234500123456789'

If attributes are missing, no IBAN can be retrieved

 >>> IntAccount('AT').iban
 Traceback (most recent call last):
 IBANError: Attribute bank is missing, no IBAN can be created
 
An international account can also be initialized with the IBAN, whereas the
other given initialization options (country, account etc.) are ignored:

 >>> b=IntAccount(iban='AT141234500123456789')
 >>> b.account
 '123456789'
 >>> b == a
 True

If the given IBAN is invalid, an error is raised:

 >>> b=IntAccount(iban='AT141234500123456781')
 Traceback (most recent call last):
 IBANError: IBAN has an invalid checksum
 
If the specified country for an IBAN is not known, an error is raised:

 >>> b=IntAccount(iban='XY141234500123456789')
 Traceback (most recent call last):
 IBANError: Country XY not implemented
 >>> IntAccount('ZX')
 Traceback (most recent call last):
 IBANError: Country ZX not implemented

Moreover, it can be requested, if the international account, or, more specific,
the according country, is member of the SEPA contract:

 >>> b.is_sepa
 True

IBANs can also be easily checked for validity:

 >>> valid('AT141234500123456789')
 True
 >>> valid('AT14123450012345678')
 False
 >>> valid('AT341234500123456789')
 False
 >>> valid('AT14123450012345a78')
 False

The country specifics are stored in a configuration file called
"countries.cfg", the syntax of this file is given there. The function
get_country_specs() can be used to read in the specifications for the needed
country

 >>> from ibanlib.iban import get_country_specs
 >>> d=get_country_specs('AT')

All configurations is now read into d. Bank/Account can now be checked for
validity
 
 >>> d['account'].valid('123')   # too short
 False
 >>> d['account'].valid('1231234')  # valid
 True
 >>> d['account'].valid('12312312321312321321313') # too long
 False
 >>> d['account'].valid('123ABC234')  # only digits allowed
 False

Short data can be filled to its maximum length

 >>> d['account'].fill('1234567')
 '00001234567'
 
Of course, IBANs can be generated for various countries, here are some
examples:

Andorra

 >>> IntAccount(iban='AD1200012030200359100100')
 IntAccount(country='AD', bank='0001', branche='2030', account='200359100100', check1='None', check2='None', check3='None')

Austria
 >>> IntAccount('AT',bank='19043',account='234573201').iban
 'AT611904300234573201'

Belgium
 >>> IntAccount (iban='BE68539007547034')
 IntAccount(country='BE', bank='539', branche='None', account='0075470', check1='None', check2='None', check3='34')

Bosnia and Herzegovina
 >>> IntAccount (iban='BA391290079401028494')
 IntAccount(country='BA', bank='129', branche='007', account='94010284', check1='None', check2='None', check3='94')

Bulgaria
 >>> IntAccount (iban='BG80BNBG96611020345678')
 IntAccount(country='BG', bank='BNBG', branche='9661', account='1020345678', check1='None', check2='None', check3='None')

Croatia
 >>> IntAccount (iban='HR1210010051863000160')
 IntAccount(country='HR', bank='1001005', branche='None', account='1863000160', check1='None', check2='None', check3='None')

Cyprus
 >>> IntAccount (iban='CY17002001280000001200527600')
 IntAccount(country='CY', bank='2', branche='128', account='1200527600', check1='None', check2='None', check3='None')

Czech Republik
 >>> IntAccount (iban='CZ6508000000192000145399')
 IntAccount(country='CZ', bank='0800', branche='None', account='192000145399', check1='None', check2='None', check3='None')

Denmark
 >>> IntAccount (iban='DK5000400440116243')
 IntAccount(country='DK', bank='40', branche='None', account='44011624', check1='None', check2='None', check3='3')

Estonia
 >>> IntAccount (iban='EE382200221020145685')
 IntAccount(country='EE', bank='22', branche='None', account='221020145685', check1='None', check2='None', check3='None')

Finland
 >>> IntAccount (iban='FI2112345600000785')
 IntAccount(country='FI', bank='123456', branche='None', account='78', check1='None', check2='None', check3='5')

France
 >>> IntAccount (iban='FR1420041010050500013M02606')
 IntAccount(country='FR', bank='20041', branche='01005', account='0500013M026', check1='None', check2='None', check3='06')

Germany
 >>> IntAccount(iban='DE89370400440532013000')
 IntAccount(country='DE', bank='37040044', branche='None', account='532013000', check1='None', check2='None', check3='None')
 >>> IntAccount('DE',bank='37040044', account='532013000').iban
 'DE89370400440532013000'

Gibraltar
 >>> IntAccount (iban='GI75NWBK000000007099453')
 IntAccount(country='GI', bank='NWBK', branche='None', account='000000007099453', check1='None', check2='None', check3='None')

Greece
 >>> IntAccount (iban='GR1601101250000000012300695')
 IntAccount(country='GR', bank='11', branche='125', account='12300695', check1='None', check2='None', check3='None')

Hungary
 >>> IntAccount (iban='HU42117730161111101800000000')
 IntAccount(country='HU', bank='117', branche='7301', account='111110180000000', check1='None', check2='6', check3='0')

Iceland
 >>> IntAccount (iban='IS140159260076545510730339')
 IntAccount(country='IS', bank='0159', branche='None', account='260076545510730339', check1='None', check2='None', check3='None')

Ireland
 >>> IntAccount (iban='IE29AIBK93115212345678')
 IntAccount(country='IE', bank='AIBK', branche='931152', account='12345678', check1='None', check2='None', check3='None')

Italy 
 
 >>> IntAccount('IT', bank='05428', branche='11101', 
 ...            account='123456', check1='X').iban
 'IT60X0542811101000000123456'
 >>> valid(iban='IT21Q054280160000ABCD12ZE34')
 True
 >>> valid('IT30C0800001000123VALE456NA')
 True
 >>> valid('IT11V0600003200000011556BFE')
 True
 >>> valid('IT21J0100516052120050012345')
 True
 
Latvia
 >>> IntAccount (iban='LV80BANK0000435195001')
 IntAccount(country='LV', bank='BANK', branche='None', account='0000435195001', check1='None', check2='None', check3='None')

Liechtenstein
 >>> IntAccount (iban='LI21088100002324013AA')
 IntAccount(country='LI', bank='8810', branche='None', account='0002324013AA', check1='None', check2='None', check3='None')

Lithuania
 >>> IntAccount (iban='LT121000011101001000')
 IntAccount(country='LT', bank='10000', branche='None', account='11101001000', check1='None', check2='None', check3='None')

Luxemburg
 >>> IntAccount (iban='LU360029152460050000')
 IntAccount(country='LU', bank='002', branche='None', account='9152460050000', check1='None', check2='None', check3='None')

Macedonia, former Yugoslav Republic of
 >>> IntAccount (iban='MK07250120000058984')
 IntAccount(country='MK', bank='250', branche='None', account='1200000589', check1='None', check2='None', check3='84')

Malta
 >>> IntAccount (iban='MT84MALT011000012345MTLCAST001S')
 IntAccount(country='MT', bank='MALT', branche='01100', account='0012345MTLCAST001S', check1='None', check2='None', check3='None')
 
Montenegro
 >>> IntAccount (iban='ME25505000012345678951')
 IntAccount(country='ME', bank='505', branche='None', account='0000123456789', check1='None', check2='None', check3='51')

The Netherlands
 >>> IntAccount (iban='NL91ABNA0417164300')
 IntAccount(country='NL', bank='ABNA', branche='None', account='417164300', check1='None', check2='None', check3='None')

Norway
 >>> IntAccount (iban='NO9386011117947')
 IntAccount(country='NO', bank='8601', branche='None', account='111794', check1='None', check2='None', check3='7')

Poland
 >>> IntAccount (iban='PL27114020040000300201355387')
 IntAccount(country='PL', bank='11402004', branche='None', account='0000300201355387', check1='None', check2='None', check3='None')

Portugal
 >>> IntAccount (iban='PT50000201231234567890154')
 IntAccount(country='PT', bank='0002', branche='0123', account='12345678901', check1='None', check2='None', check3='54')
 
Romania
 >>> IntAccount (iban='RO49AAAA1B31007593840000')
 IntAccount(country='RO', bank='AAAA', branche='None', account='1B31007593840000', check1='None', check2='None', check3='None')

Serbia
 >>> IntAccount (iban='CS73260005601001611379')
 IntAccount(country='CS', bank='260', branche='None', account='0056010016113', check1='None', check2='None', check3='79')
 
Slovak Republic
 >>> IntAccount (iban='SK3112000000198742637541')
 IntAccount(country='SK', bank='1200', branche='None', account='0000198742637541', check1='None', check2='None', check3='None')
 
Slovenia
 >>> IntAccount (iban='SI56191000000123438')
 IntAccount(country='SI', bank='19100', branche='None', account='00001234', check1='None', check2='None', check3='38')
 
Spain
 >>> IntAccount (iban='ES9121000418450200051332')
 IntAccount(country='ES', bank='2100', branche='0418', account='0200051332', check1='None', check2='4', check3='5')

Sweden
 >>> IntAccount (iban='SE3550000000054910000003')
 IntAccount(country='SE', bank='500', branche='None', account='0000005491000000', check1='None', check2='None', check3='3')

Switzerland
 >>> IntAccount (iban='CH9300762011623852957')
 IntAccount(country='CH', bank='00762', branche='None', account='011623852957', check1='None', check2='None', check3='None')

Turkey
 >>> IntAccount (iban='TR330006100519786457841326')
 IntAccount(country='TR', bank='00061', branche='None', account='00519786457841326', check1='None', check2='None', check3='None')

United Kingdom
 >>> IntAccount (iban='GB29NWBK60161331926819')
 IntAccount(country='GB', bank='NWBK', branche='601613', account='31926819', check1='None', check2='None', check3='None')

Mauritius
 >>> IntAccount (iban='MU17BOMM0101101030300200000MUR')
 IntAccount(country='MU', bank='BOMM01', branche='None', account='01101030300200000M', check1='None', check2='None', check3='None')
 
Tunisia
 >>> IntAccount (iban='TN5914207207100707129648')
 IntAccount(country='TN', bank='14', branche='207', account='2071007071296', check1='None', check2='None', check3='48')
 