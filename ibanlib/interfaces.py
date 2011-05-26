from zope.interface import Interface
from zope.schema import TextLine

class IIntAccount(Interface):
    """ Schema for International Account IntAccount class """
    country = TextLine(
        title=u"Country", 
        description=u"Two-letter country ISO-code",
        min_length=2,
        max_length=2,
        required=True)

    bank = TextLine(
        title=u"Bank", 
        description=u"Bank code")

    branche = TextLine(
        title=u"Branche",
        description=u"Branche code")

    account = TextLine(
        title = u"Account number",
        description = u"Account number")

    checksum = TextLine(
        title = u"Checksum",
        description = u"Checksum of account number")

    iban = TextLine(
        title = u"IBAN",
        description = u"International Bank Account Number")
    
