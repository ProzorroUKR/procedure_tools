language: uk

*** Налаштування ***
Документація      Від закупівлі з переможцями до закритої: договори, зміни до
...               них і їхнє завершення.

Ресурс            ${CURDIR}/../libraries.resource


*** Ключових слова ***
Підписати Договір
    [Документація]    Взяти права на договір, дати обом сторонам назвати
    ...               свого підписанта, і активувати договір.
    [Аргументи]    ${index}=0    ${amount}=${None}    ${with_signer_info}=${True}
    Отримати Права На Договір    index=${index}
    IF    ${with_signer_info}
        ${buyer}=       Дані Підписанта
        Заповнити Підписанта Замовника        ${buyer}       index=${index}
        ${supplier}=    Дані Підписанта
        Заповнити Підписанта Постачальника    ${supplier}    index=${index}
    END
    ${contract}=    Отримати Договір           index=${index}
    ${data}=        Дані Активації Договору    ${contract}    amount=${amount}
    ${contract}=    Змінити Договір            ${data}        index=${index}
    Should Be Equal    ${contract}[status]    active
    RETURN    ${contract}

Внести Зміну До Договору
    [Документація]    Створити зміну до договору і активувати її.
    [Аргументи]    ${index}=0    ${rationale_type}=itemPriceChange
    ${change}=      Дані Зміни До Договору    rationale_type=${rationale_type}
    ${contract}=    Створити Зміну До Договору    ${change}    index=${index}
    ${last}=        Evaluate    len($contract["changes"]) - 1
    ${activate}=    Дані Активації Зміни До Договору    ${contract}
    ${contract}=    Змінити Зміну До Договору    ${activate}    index=${index}    change_index=${last}
    Should Be Equal    ${contract}[changes][${last}][status]    active
    RETURN    ${contract}

Завершити Договір
    [Документація]    Закрити договір, вказавши суму, яку справді сплатили.
    [Аргументи]    ${amount}    ${index}=0
    ${data}=        Дані Завершення Договору    ${amount}
    ${contract}=    Змінити Договір    ${data}    index=${index}
    Should Be Equal    ${contract}[status]    terminated
    RETURN    ${contract}

Завершити Всі Договори
    [Документація]    Підписати кожен договір закупівлі, за потреби внести до
    ...               нього зміну, і закрити його, щоб сама закупівля могла
    ...               завершитись.
    [Аргументи]    ${amend}=${False}    ${with_signer_info}=${True}
    ${contracts}=    Отримати Договори
    FOR    ${index}    ${contract}    IN ENUMERATE    @{contracts}
        ${contract}=    Підписати Договір    index=${index}    with_signer_info=${with_signer_info}
        IF    ${amend}
            Внести Зміну До Договору    index=${index}    rationale_type=fiscalYearExtension
        END
        ${paid}=    Evaluate    round(${contract}[value][amount] * 0.9, 2)
        Завершити Договір    ${paid}    index=${index}
    END
    Дочекатись Статусу Закупівлі    complete
    Закупівля Має Бути Завершена    complete

Закупівля Має Бути Завершена
    [Документація]    Кінцевий статус - це той, з якого закупівля вже не
    ...               вийде, тож перевіряють і те, що вона в нього прийшла, і
    ...               те, що вона в ньому лишається: спробу замовника змінити
    ...               його відхиляють.
    [Аргументи]    ${status}
    ${tender}=    Перечитати Закупівлю
    Should Be Equal    ${tender}[status]    ${status}
    ${patch}=    Дані Зміни Закупівлі    active.tendering
    Run Keyword And Expect Error
    ...    *Can't update tender in current (${status}) status*
    ...    Змінити Закупівлю    ${patch}
    ${tender}=    Перечитати Закупівлю
    Should Be Equal    ${tender}[status]    ${status}

На Кожен Лот Має Бути Договір
    [Документація]    Багатолотова закупівля завершується договором на кожен
    ...               лот.
    ${tender}=       Перечитати Закупівлю
    ${contracts}=    Отримати Договори
    ${lots}=         Evaluate    len($tender.get("lots") or [1])
    Length Should Be    ${contracts}    ${lots}

Скасувати Закупівлю
    [Документація]    Створити скасування, підписати протокол і подати його.
    ...
    ...               Там, де процедура має скарги на скасування, скасування
    ...               вичікує період оскарження в ``pending``; де не має -
    ...               одразу стає ``active``. ``wait=${True}`` покриває обидва
    ...               випадки.
    [Аргументи]    ${reason_type}=noDemand    ${related_lot}=${None}    ${index}=0    ${wait}=${True}
    ${data}=      Дані Скасування    reason_type=${reason_type}    related_lot=${related_lot}
    ${created}=   Створити Скасування    ${data}    index=${index}
    Should Be Equal    ${created}[status]    draft

    ${report}=    Дані Протоколу Скасування    title=cancellation_report_${index}.p7s
    Додати Документ Скасування    ${report}    index=${index}

    ${submit}=          Дані Зміни Скасування    pending
    ${cancellation}=    Змінити Скасування    ${submit}    index=${index}
    IF    ${wait}
        ${cancellation}=    Дочекатись Статусу Скасування    active    index=${index}
        Should Be Equal    ${cancellation}[status]    active
    END
    RETURN    ${cancellation}
