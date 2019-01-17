"""
Base model for creating certificate.
"""


class CreateCertificateDto:

    def __init__(self, common_name, email=None, name=None, surname=None, country_name=None, serial=None, validity=None,
                 locality_name=None, postal_address=None, postal_code=None, street_address=None, state_name=None,
                 pseudonym=None, generation_qualifier=None, title=None, business_category=None, valid_after=None):
        self.common_name = common_name
        self.email = email
        self.country_name = country_name
        self.locality_name = locality_name
        self.postal_address = postal_address
        self.postal_code = postal_code
        self.street_address = street_address
        self.state_name = state_name
        self.name = name
        self.surname = surname
        self.pseudonym = pseudonym
        self.generation_qualifier = generation_qualifier
        self.title = title
        self.serial = serial
        self.business_category = business_category
        self.validity = validity
        self.valid_after = valid_after
