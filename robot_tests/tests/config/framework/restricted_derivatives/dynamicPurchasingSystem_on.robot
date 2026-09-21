language: uk

*** Налаштування ***
Документація      ``restrictedDerivatives`` - це бік фреймворку для
...               ``restricted``: він обмежує те, що можуть показувати
...               процедури, похідні від фреймворку.
...
...               Кожна вбудована тека даних ставить його в false, а бік true
...               потребує майданчика, акредитованого на дані з обмеженим
...               доступом. Без цієї акредитації API відхиляє фреймворк
...               раніше, ніж можна побачити щось про сам параметр, тож сьюіт
...               це й повідомляє і пропускається, а не перевіряє
...               середовище.

Ресурс            ${CURDIR}/../../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури
Розбірка Suite        Закрити Сесію Процедури

Тестові теги      config    config:restrictedDerivatives    procedure:dynamicPurchasingSystem


*** Тест-кейси ***
Похідні Процедури З Обмеженим Доступом Потребують Акредитованого Майданчика
    [Документація]    Створити такий фреймворк; пропустити, коли цьому
    ...               майданчику не дозволено.
    [Теги]    phase:framework

    ${settings}=    Налаштування Запуску
    ${config}=      Дані Конфігу Фреймворку    restrictedDerivatives=${True}
    ${data}=        Дані Фреймворку    acceleration=${settings}[acceleration]    config=${config}
    ${failed}    ${error}=    Run Keyword And Ignore Error    Створити Фреймворк    ${data}
    IF    "${failed}" == "FAIL"
        Skip If    "accreditation" in """${error}"""
        ...    цей майданчик не акредитований на дані фреймворку з обмеженим доступом
        Fail    ${error}
    END
    ${config}=    Отримати Значення Контексту    framework_config
    Should Be Equal    ${config}[restrictedDerivatives]    ${True}

Звичайний Фреймворк Створюється
    [Документація]    Значення за замовчуванням працюють, тож невдача вище
    ...               стосується параметра, а не тіла запиту фреймворку.
    [Теги]    phase:framework

    ${settings}=     Налаштування Запуску
    ${data}=         Дані Фреймворку    acceleration=${settings}[acceleration]
    ${framework}=    Створити Фреймворк    ${data}
    Should Be Equal    ${framework}[status]    draft
    ${config}=    Отримати Значення Контексту    framework_config
    Should Be Equal    ${config}[restrictedDerivatives]    ${False}
    Should Be Equal    ${config}[hasItems]                 ${False}
