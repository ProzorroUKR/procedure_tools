from faker import Faker
from faker.providers.phone_number import Provider as PhoneNumberProvider

fake = Faker("uk_UA")
fake_en = Faker("en_US")


class ProzorroPhoneNumberProvider(PhoneNumberProvider):
    def prozorro_phone_number(self):
        return f"+{self.msisdn()[1:]}"


fake.add_provider(ProzorroPhoneNumberProvider)
fake_en.add_provider(ProzorroPhoneNumberProvider)
