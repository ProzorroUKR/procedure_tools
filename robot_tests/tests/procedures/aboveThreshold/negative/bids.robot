language: uk

*** Налаштування ***
Документація      Що API відхиляє в тендерній пропозиції.
...
...               Одна закупівля відкривається на прийом пропозицій, і кожен
...               тест тут пропонує їй те, чого вона не візьме. Пропозицію
...               перевіряють проти закупівлі, на яку вона відповідає - її
...               лотів, предметів закупівлі, валюти, - тож більшість цих
...               перевірок про те, що ці двоє розходяться між собою.

Ресурс            ${CURDIR}/../../../../resources/procedure.resource

Налаштування Suite    Відкрити Закупівлю На Прийом Пропозицій
Розбірка Suite        Закрити Сесію Процедури

Тестові теги      negative    procedure:aboveThreshold    feature:bids


*** Тест-кейси ***
Пропозицію До Закупівлі З Лотами Подають По Лотах
    [Документація]    З лотами немає єдиної речі, на яку можна поставити ціну,
    ...               тож одна загальна вартість не означає нічого.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.lotValues=${None}
    ...                                    data.value=${{ {'amount': 1000, 'currency': 'UAH'} }}
    Run Keyword And Expect Error
    ...    *value should be posted for each lot of bid*
    ...    Створити Пропозицію    ${data}    index=0

Пропозиція Не Може Містити Двох Цін На Один Лот
    [Документація]    Дві ціни на один лот залишили б відкритим питання, яку з
    ...               них учасник мав на увазі.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.lotValues.1=${{ $data['data']['lotValues'][0] }}
    Run Keyword And Expect Error
    ...    *don't allow duplicated proposals*
    ...    Створити Пропозицію    ${data}    index=0

Пропозиція Не Може Бути На Лот Іншої Закупівлі
    [Документація]    Лот, на який пропонують, мусить бути одним з лотів, на
    ...               які подають пропозицію.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.lotValues.0.relatedLot=${{ __import__('uuid').uuid4().hex }}
    Run Keyword And Expect Error
    ...    *relatedLot should be one of lots*
    ...    Створити Пропозицію    ${data}    index=0

Ціну Пропозиції Вказують У Валюті Лота
    [Документація]    Ранжування пропозицій у різних валютах вимагало б курсу,
    ...               якого API не має.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.lotValues.0.value.currency=USD
    Run Keyword And Expect Error
    ...    *currency of bid should be identical to currency of value of lot*
    ...    Створити Пропозицію    ${data}    index=0

Ціна Пропозиції Має Той Самий Режим ПДВ, Що Й Лот
    [Документація]    Ціна з ПДВ і ціна без ПДВ не порівнювані.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.lotValues.0.value.valueAddedTaxIncluded=${True}
    Run Keyword And Expect Error
    ...    *valueAddedTaxIncluded of bid should be identical*
    ...    Створити Пропозицію    ${data}    index=0

Пропозиція Мусить Назвати Свого Учасника
    [Документація]    Анонімну пропозицію не визначити переможцем нікому.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.tenderers=${None}
    Run Keyword And Expect Error
    ...    *tenderers*This field is required*
    ...    Створити Пропозицію    ${data}    index=0

Пропозиція Називає Лише Одного Учасника
    [Документація]    Об'єднання подає пропозицію як одна сторона, тож у
    ...               пропозиції один учасник, хто б за ним не стояв.

    ${first}=     Дані Учасника
    ${second}=    Дані Учасника    identifier_id=13313462
    ${data}=      Дані Пропозиції    ${TENDER}    tenderers=${{ [$first, $second] }}
    Run Keyword And Expect Error
    ...    *tenderers*no more than 1 item*
    ...    Створити Пропозицію    ${data}    index=0

Учасник Мусить Вказати Свій Розмір
    [Документація]    Чи є учасник суб'єктом малого підприємництва - частина
    ...               того, про що звітують про закупівлю потім.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.tenderers.0.scale=${None}
    Run Keyword And Expect Error
    ...    *scale*This field is required*
    ...    Створити Пропозицію    ${data}    index=0

Пропозиція Не Може Сама Підтвердити Свою Прийнятність
    [Документація]    Відповідність критеріям прийнятності колись була
    ...               галочкою, яку ставив учасник. Тепер на неї відповідають
    ...               через критерії, а старого поля більше немає.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.selfEligible=${True}
    Run Keyword And Expect Error
    ...    *selfEligible*Rogue field*
    ...    Створити Пропозицію    ${data}    index=0

Пропозиція Не Може Оцінювати Предмет Іншої Закупівлі
    [Документація]    Ціну вказують на ті предмети закупівлі, які купують.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.items.0.id=${{ __import__('uuid').uuid4().hex }}
    Run Keyword And Expect Error
    ...    *Bid items ids should be on tender items ids*
    ...    Створити Пропозицію    ${data}    index=0

Ціни За Предмети Закупівлі Мусять Скластися В Ціну Пропозиції
    [Документація]    Ціну пропозиції вказують двічі: раз загальною сумою і раз
    ...               розподіленою по предметах закупівлі. Оскільки пропозиція
    ...               йде без ПДВ, ці двоє мусять дати рівно однаково.

    ${data}=    Дані Пропозиції    ${TENDER}
    ${data}=    Змінити Дані    ${data}    data.items.0.unit.value.amount=${1}
    Run Keyword And Expect Error
    ...    *Total amount of unit values should be equal*
    ...    Створити Пропозицію    ${data}    index=0

Пропозицію Не Перевести В Жоден Статус, Крім Поданої
    [Документація]    Пропозиція має рівно один хід: її подають. Будь-який
    ...               інший статус, до якого учасник міг би потягнутися,
    ...               відхиляється - але лише тоді, коли пропозиція вже досить
    ...               повна, щоб її взагалі розглядати, бо про критерії без
    ...               відповідей скаржаться раніше.

    ${bid}=    Подати Пропозицію    ${TENDER}    ${CRITERIA}    index=0
    Should Be Equal    ${bid}[status]    pending

    ${patch}=    Дані Зміни Пропозиції    active
    Run Keyword And Expect Error
    ...    *Can't update bid to (active) status*
    ...    Змінити Пропозицію    ${patch}    index=0


*** Ключових слова ***
Відкрити Закупівлю На Прийом Пропозицій
    [Документація]    Одна закупівля в ``active.tendering`` з одним лотом,
    ...               спільна для кожного тесту тут. Аукціону немає, тож чекати
    ...               нічого не доводиться.
    Відкрити Сесію Процедури
    ${tender}=      Створити Відкриту Закупівлю    lots=1    submission=quick(mode:no-auction)
    ${criteria}=    Опублікувати Критерії    ${tender}
    Додати Документи Закупівлі
    ${tender}=      Відкрити Прийом Пропозицій
    Set Suite Variable    ${TENDER}      ${tender}
    Set Suite Variable    ${CRITERIA}    ${criteria}
