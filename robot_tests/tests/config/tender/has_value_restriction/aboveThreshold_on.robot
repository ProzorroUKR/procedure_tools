language: uk

*** Налаштування ***
Документація      ``hasValueRestriction`` робить вартість лота граничною межею.
...
...               Коли він увімкнений, пропозицію, дорожчу за лот,
...               відхиляють. Коли вимкнений - а саме так іде вбудований потік
...               понад поріг - ту саму пропозицію приймають, і вартість лота
...               є лише очікуваною. Це один із двох параметрів, які ця
...               процедура справді може вибирати, тож варто мати обидва
...               боки.

Ресурс            ${CURDIR}/../../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури
Розбірка Suite        Закрити Сесію Процедури
Налаштування тесту    Пропустити Якщо Попередня Стадія Впала
Розбирання тестy      Запамʼятати Невдалу Стадію

Тестові теги      config    config:hasValueRestriction    procedure:aboveThreshold


*** Тест-кейси ***
Опублікувати Закупівлю, Що Обмежує Вартість
    [Документація]    Один лот, параметр увімкнений.
    [Теги]    phase:tendering

    ${config}=      Дані Конфігу Закупівлі    hasValueRestriction=${True}
    ${tender}=      Створити Відкриту Закупівлю    lots=1    submission=quick(mode:no-auction)
    ...                                            config=${config}
    ${settings}=    Отримати Конфіг Закупівлі
    Should Be Equal    ${settings}[hasValueRestriction]    ${True}

    ${criteria}=    Опублікувати Критерії    ${tender}
    Додати Документи Закупівлі
    ${tender}=      Відкрити Прийом Пропозицій

    Set Suite Variable    ${TENDER}      ${tender}
    Set Suite Variable    ${CRITERIA}    ${criteria}

Пропозицію, Дорожчу За Лот, Відхиляють
    [Документація]    Межею є вартість лота, і відмова це й називає.
    [Теги]    phase:tendering    negative

    ${over}=    Evaluate    round(${TENDER}[lots][0][value][amount] * 2, 2)
    ${data}=    Дані Пропозиції    ${TENDER}    amounts=${{ [$over] }}
    Run Keyword And Expect Error
    ...    *value of bid should be less than value of lot*
    ...    Створити Пропозицію    ${data}    index=0

Пропозицію В Межах Вартості Лота Приймають
    [Документація]    Та сама пропозиція в межах вартості лота проходить,
    ...               тож відмова вище була про суму і ні про що інше.
    [Теги]    phase:tendering

    Подати Пропозицію    ${TENDER}    ${CRITERIA}    index=0
    ${bid}=    Отримати Пропозицію    0
    Should Be Equal    ${bid}[status]    pending
