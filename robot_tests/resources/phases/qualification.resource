language: uk

*** Налаштування ***
Документація      Від завершення прийому пропозицій до закупівлі з
...               переможцями: аукціон, визначення переможців і періоди
...               оскарження.

Ресурс            ${CURDIR}/../libraries.resource


*** Ключових слова ***
Дочекатись Проведення Аукціону
    [Документація]    Дочекатись кінця періоду подання пропозицій, потім
    ...               аукціону, і залишити закупівлю на кваліфікації.
    Дочекатись Наступної Перевірки Закупівлі
    Дочекатись Статусу Закупівлі    ${{ ['active.auction', 'active.qualification', 'active.awarded'] }}
    ...                             fail_status=unsuccessful
    Дочекатись Аукціону

Дочекатись Кваліфікації
    [Документація]    Дочекатись кінця періоду подання пропозицій у закупівлі,
    ...               яка не проводить аукціону.
    Дочекатись Наступної Перевірки Закупівлі
    Дочекатись Статусу Закупівлі    ${{ ['active.qualification', 'active.awarded'] }}
    ...                             fail_status=unsuccessful

Кваліфікувати Переможця
    [Документація]    Кваліфікувати одного переможця, підписати рішення і
    ...               активувати його. Лімітовані процедури не підтверджують
    ...               відповідність критеріям прийнятності - для них
    ...               передають ``eligible=${None}``.
    [Аргументи]    ${index}=0    ${eligible}=${True}
    ${qualification}=    Дані Кваліфікації Переможця    eligible=${eligible}
    Змінити Переможця    ${qualification}    index=${index}

    ${notice}=    Дані Файлу Підпису    title=award_notice_${index}.p7s
    Додати Документ Переможця    ${notice}    index=${index}

    ${activate}=    Дані Зміни Переможця    active
    ${award}=       Змінити Переможця       ${activate}    index=${index}
    Should Be Equal    ${award}[status]    active
    RETURN    ${award}

Кваліфікувати Всіх Переможців
    [Документація]    Кваліфікувати всіх переможців, яких дає процедура, а потім
    ...               дочекатись періодів оскарження.
    ...
    ...               Відкрита процедура створює переможців своїх лотів по ходу,
    ...               тож коли жоден з них не очікує рішення, вона ще чекає,
    ...               поки закупівля вийде з кваліфікації, і лише тоді вважає,
    ...               що більше переможців не буде. Лімітована процедура на
    ...               кшталт звітування має одного переможця і в кваліфікацію
    ...               не входить узагалі, тож передає ``wait_status=${None}``
    ...               і зупиняється на першому порожньому проході.
    [Аргументи]    ${eligible}=${True}    ${wait_status}=active.awarded
    Дочекатись Документів ЄДР
    WHILE    ${True}    limit=15    on_limit_message=переможці все не переставали з'являтися
        ${awards}=    Отримати Переможців
        ${pending}=   Evaluate
        ...    [index for index, award in enumerate($awards) if award["status"] == "pending"]
        IF    ${pending}
            FOR    ${index}    IN    @{pending}
                Кваліфікувати Переможця    index=${index}    eligible=${eligible}
            END
            CONTINUE
        END
        IF    $wait_status is None    BREAK
        ${tender}=    Перечитати Закупівлю
        IF    "${tender}[status]" != "active.qualification"    BREAK
        Почекати Секунд    5
    END
    Дочекатись Періоду Оскарження Переможців
    IF    $wait_status is not None
        Дочекатись Статусу Закупівлі    ${wait_status}    fail_status=unsuccessful
    END

Перемогти Має Дешевша Пропозиція
    [Документація]    Перевірити рейтинг, який дав аукціон, а не повірити,
    ...               що він його дав: кожен лот завершується рівно одним
    ...               активним переможцем, і ним стала найдешевша пропозиція
    ...               на цей лот.
    ${tender}=    Перечитати Закупівлю
    ${awards}=    Отримати Переможців
    ${bids}=      Отримати Пропозиції
    ${lots}=      Evaluate    [lot["id"] for lot in $tender.get("lots") or []]
    IF    ${lots}
        FOR    ${lot_id}    IN    @{lots}
            ${winners}=    Evaluate
            ...    [a for a in $awards if a["status"] == "active" and a.get("lotID") == "${lot_id}"]
            Length Should Be    ${winners}    1    лот ${lot_id} має не рівно одного активного переможця
            ${offers}=    Evaluate
            ...    sorted(v["value"]["amount"] for b in $bids for v in b.get("lotValues", []) if v["relatedLot"] == "${lot_id}")
            Should Be Equal As Numbers    ${winners}[0][value][amount]    ${offers}[0]
        END
    ELSE
        ${winners}=    Evaluate    [a for a in $awards if a["status"] == "active"]
        Length Should Be    ${winners}    1
        ${offers}=       Evaluate    sorted(b["value"]["amount"] for b in $bids)
        Should Be Equal As Numbers    ${winners}[0][value][amount]    ${offers}[0]
    END
