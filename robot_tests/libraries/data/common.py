"""
The small pieces every procedure payload is made of: addresses, identifiers,
organizations, classifications, items, values and milestones.

They are the bottom layer of the data modules; ``tender``, ``bid``, ``award``
and ``contract`` compose them, and a test can compose them too when it wants
something the defaults do not give::

    ${item}=      Item Data    quantity=5    related_lot=${lot}[id]
    ${tender}=    Tender Data  items=${{[$item]}}
"""

from __future__ import annotations

from typing import Any

from data.utils import build, fake, fake_en, new_id

DEFAULT_CURRENCY = "UAH"
DEFAULT_SCHEME = "UA-EDR"

# The classification pair the bundled procedures use: industrial machinery.
DEFAULT_CLASSIFICATION = {
    "description": "Промислова техніка",
    "id": "42000000-6",
    "scheme": "ДК021",
}
DEFAULT_ADDITIONAL_CLASSIFICATION = {
    "description": "Техніка конторська/офісна, інша",
    "id": "28.23.23",
    "scheme": "ДКПП",
}
DEFAULT_UNIT = {"code": "KGM", "name": "кг"}


def address_data(**kwargs: Any) -> dict[str, Any]:
    """A Kyiv postal address."""
    return build(
        {
            "countryName": "Україна",
            "locality": "м. Київ",
            "postalCode": "01220",
            "region": "м. Київ",
            "streetAddress": fake.street_address(),
        },
        **kwargs,
    )


def identifier_data(identifier_id: str = "21725150", **kwargs: Any) -> dict[str, Any]:
    """An EDR identifier of a Ukrainian legal entity."""
    return build(
        {
            "id": identifier_id,
            "legalName": fake.company(),
            "scheme": DEFAULT_SCHEME,
        },
        **kwargs,
    )


def contact_point_data(with_email: bool = True, **kwargs: Any) -> dict[str, Any]:
    contact: dict[str, Any] = {
        "name": fake.name(),
        "telephone": fake.prozorro_phone_number(),
    }
    if with_email:
        contact["email"] = fake.email()
    else:
        contact["url"] = fake.url()
    return build(contact, **kwargs)


def organization_data(
    kind: str | None = "general",
    identifier_id: str = "21725150",
    with_email: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """A buyer, procuring entity or tenderer; ``kind`` is left out for a tenderer."""
    organization: dict[str, Any] = {
        "address": address_data(),
        "contactPoint": contact_point_data(with_email=with_email),
        "identifier": identifier_data(identifier_id),
        "name": fake.company(),
    }
    if kind:
        organization["kind"] = kind
    return build(organization, **kwargs)


def procuring_entity_data(kind: str = "special", **kwargs: Any) -> dict[str, Any]:
    return organization_data(kind=kind, with_email=False, **kwargs)


def tenderer_data(identifier_id: str = "00137256", scale: str = "micro", **kwargs: Any) -> dict[str, Any]:
    tenderer = organization_data(kind=None, identifier_id=identifier_id)
    tenderer["identifier"]["uri"] = fake.url()
    tenderer["identifier"].pop("legalName", None)
    tenderer["scale"] = scale
    return build(tenderer, **kwargs)


def supplier_data(identifier_id: str = "13313462", scale: str = "micro", **kwargs: Any) -> dict[str, Any]:
    supplier = organization_data(kind=None, identifier_id=identifier_id)
    supplier["identifier"]["uri"] = "https://example.com"
    supplier["scale"] = scale
    return build(supplier, **kwargs)


def classification_data(**kwargs: Any) -> dict[str, Any]:
    return build(DEFAULT_CLASSIFICATION, **kwargs)


def unit_data(**kwargs: Any) -> dict[str, Any]:
    return build(DEFAULT_UNIT, **kwargs)


def value_data(
    amount: float = 1000,
    currency: str = DEFAULT_CURRENCY,
    value_added_tax_included: bool | None = False,
    **kwargs: Any,
) -> dict[str, Any]:
    value: dict[str, Any] = {"amount": amount, "currency": currency}
    if value_added_tax_included is not None:
        value["valueAddedTaxIncluded"] = value_added_tax_included
    return build(value, **kwargs)


def guarantee_data(amount: float = 100, currency: str = DEFAULT_CURRENCY, **kwargs: Any) -> dict[str, Any]:
    return build({"amount": amount, "currency": currency}, **kwargs)


def period_data(start_date: str, end_date: str, **kwargs: Any) -> dict[str, Any]:
    return build({"startDate": start_date, "endDate": end_date}, **kwargs)


def item_data(
    quantity: float = 1,
    related_lot: str | None = None,
    delivery_start_date: str = "2017-07-11T16:02:36.221241+03:00",
    delivery_end_date: str = "2017-08-10T16:02:36.221295+03:00",
    with_id: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """One tender item; pass ``related_lot`` to bind it to a lot."""
    item: dict[str, Any] = {
        "additionalClassifications": [dict(DEFAULT_ADDITIONAL_CLASSIFICATION)],
        "classification": classification_data(),
        "deliveryAddress": address_data(postalCode="79000"),
        "deliveryDate": {"startDate": delivery_start_date, "endDate": delivery_end_date},
        "description": fake.sentence(nb_words=8),
        "description_en": fake_en.sentence(nb_words=8),
        "quantity": quantity,
        "unit": unit_data(),
    }
    if with_id:
        item["id"] = new_id()
    if related_lot:
        item["relatedLot"] = related_lot
    return build(item, **kwargs)


# A product from the localisation catalogue, and the category it sits in. A
# localisation criterion can only be attached to an item that names both.
LOCALISED_CATEGORY = "31120000-730722-40996564"
LOCALISED_PRODUCT = "1270c96a250e474ba0dd7bc782705411"
LOCALISED_CLASSIFICATION = {
    "description": "Генератори",
    "id": "31120000-3",
    "scheme": "ДК021",
}


def localised_item_data(quantity: float = 1, **kwargs: Any) -> dict[str, Any]:
    """
    An item that can carry a localisation criterion.

    The criterion is about how much of the product is made locally, so the item
    has to say which catalogue product it is; without ``category`` the API
    refuses the criterion rather than the item.
    """
    item = item_data(quantity=quantity, with_id=True)
    item["classification"] = dict(LOCALISED_CLASSIFICATION)
    item["category"] = LOCALISED_CATEGORY
    item["product"] = LOCALISED_PRODUCT
    return build(item, **kwargs)


def lot_data(
    title: str | None = None,
    amount: float = 2500,
    minimal_step_amount: float = 25,
    guarantee_amount: float = 100,
    lot_id: str | None = None,
    with_minimal_step: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    One lot, with the id a test needs to bind items, milestones and criteria to it.

    ``minimalStep`` is how much a bid has to improve on the last one during the
    auction, so a tender that holds no auction must not carry it - the API
    calls it a rogue field.
    """
    lot: dict[str, Any] = {
        "id": lot_id or new_id(),
        "title": title or f"Лот: {fake.word()}",
        "description": fake.sentence(nb_words=6),
        "value": value_data(amount=amount),
        "guarantee": guarantee_data(amount=guarantee_amount),
    }
    if with_minimal_step:
        lot["minimalStep"] = value_data(amount=minimal_step_amount)
    return build(lot, **kwargs)


def milestone_data(
    code: str = "prepayment",
    title: str = "executionOfWorks",
    milestone_type: str = "financing",
    percentage: float = 100,
    sequence_number: int = 1,
    duration_days: int = 2,
    duration_type: str = "working",
    related_lot: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    milestone: dict[str, Any] = {
        "code": code,
        "duration": {"days": duration_days, "type": duration_type},
        "percentage": percentage,
        "sequenceNumber": sequence_number,
        "title": title,
        "type": milestone_type,
    }
    if related_lot:
        milestone["relatedLot"] = related_lot
    return build(milestone, **kwargs)


def payment_milestones_data(related_lot: str | None = None) -> list[dict[str, Any]]:
    """The financing and delivery pair every tender (or lot) needs."""
    return [
        milestone_data(
            code="prepayment",
            title="executionOfWorks",
            milestone_type="financing",
            sequence_number=1,
            related_lot=related_lot,
        ),
        milestone_data(
            code="standard",
            title="signingTheContract",
            milestone_type="delivery",
            sequence_number=2,
            related_lot=related_lot,
        ),
    ]


def signer_info_data(**kwargs: Any) -> dict[str, Any]:
    """Signer info of a contract party (buyer or supplier)."""
    return build(
        {
            "authorizedBy": "Статут компанії",
            "email": fake.email(),
            "iban": "111111111111111",
            "name": fake_en.name(),
            "position": "Генеральний директор",
            "telephone": fake.prozorro_phone_number(),
        },
        **kwargs,
    )
