import threading

from faker import Faker
from faker.providers.phone_number import Provider as PhoneNumberProvider


class ProzorroPhoneNumberProvider(PhoneNumberProvider):
    def prozorro_phone_number(self):
        return f"+380{self.random_number(digits=9, fix_len=True)}"


def _create_faker(locale):
    instance = Faker(locale)
    instance.add_provider(ProzorroPhoneNumberProvider)
    return instance


class _ThreadLocalFaker:
    def __init__(self, locale):
        self._locale = locale
        self._local = threading.local()

    def _get(self):
        instance = getattr(self._local, "instance", None)
        if instance is None:
            instance = _create_faker(self._locale)
            seed = getattr(self._local, "seed", None)
            if seed is not None:
                instance.seed_instance(seed)
            self._local.instance = instance
        return instance

    def seed_instance(self, seed):
        self._local.seed = seed
        instance = getattr(self._local, "instance", None)
        if instance is not None:
            instance.seed_instance(seed)

    def __getattr__(self, name):
        return getattr(self._get(), name)

    def __call__(self, *args, **kwargs):
        return self._get()(*args, **kwargs)


fake = _ThreadLocalFaker("uk_UA")
fake_en = _ThreadLocalFaker("en_US")
