import logging
import threading
from typing import Any

from faker import Faker
from faker.providers.phone_number import Provider as PhoneNumberProvider

logging.getLogger("faker").setLevel(logging.INFO)


class ProzorroPhoneNumberProvider(PhoneNumberProvider):
    def prozorro_phone_number(self) -> str:
        return f"+380{self.random_number(digits=9, fix_len=True)}"


def _create_faker(locale: str) -> Faker:
    instance = Faker(locale)
    instance.add_provider(ProzorroPhoneNumberProvider)
    return instance


class _ThreadLocalFaker:
    def __init__(self, locale: str) -> None:
        self._locale = locale
        self._local = threading.local()

    def _get(self) -> Faker:
        instance: Faker | None = getattr(self._local, "instance", None)
        if instance is None:
            instance = _create_faker(self._locale)
            seed = getattr(self._local, "seed", None)
            if seed is not None:
                instance.seed_instance(seed)
            self._local.instance = instance
        return instance

    def seed_instance(self, seed: int) -> None:
        self._local.seed = seed
        instance: Faker | None = getattr(self._local, "instance", None)
        if instance is not None:
            instance.seed_instance(seed)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get(), name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        instance: Any = self._get()
        return instance(*args, **kwargs)  # pylint: disable=not-callable


fake = _ThreadLocalFaker("uk_UA")
fake_en = _ThreadLocalFaker("en_US")
