language: uk

*** Налаштування ***
Документація      ``valueCurrencyEquality`` вирішує, чи мусить пропозиція бути
...               у валюті закупівлі.
...
...               Кожна вбудована тека даних ставить його в true. Спроба
...               іншого значення показує чому: закупівлі понад поріг не
...               дозволено його вимикати, тож пропозиції в іншій валюті - не
...               той випадок, який тут може виникнути. Цей сьюіт тримає це
...               обмеження на місці.

Ресурс            ${CURDIR}/../../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури
Розбірка Suite        Закрити Сесію Процедури

Тестові теги      config    config:valueCurrencyEquality    procedure:aboveThreshold    negative


*** Тест-кейси ***
Однаковість Валюти Не Вимкнути
    [Документація]    API відхиляє закупівлю навідріз, називаючи параметр.
    [Теги]    phase:tendering

    ${config}=      Дані Конфігу Закупівлі    valueCurrencyEquality=${False}
    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі    lots=${{ [] }}
    ...                               acceleration=${settings}[acceleration]
    ...                               config=${config}
    Run Keyword And Expect Error
    ...    *valueCurrencyEquality*is not one of*
    ...    Створити Закупівлю    ${data}

Однаковість Валюти Увімкнена За Замовчуванням
    [Документація]    Значення, яке кожна процедура отримує, не питаючи.
    [Теги]    phase:tendering

    ${config}=    Дані Конфігу Закупівлі
    Should Be Equal    ${config}[valueCurrencyEquality]    ${True}
