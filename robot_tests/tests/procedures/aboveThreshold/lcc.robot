language: uk

*** Налаштування ***
Документація      Понад поріг, де оцінюють вартість володіння, а не вартість
...               купівлі.
...
...               Переможця визначають за вартістю життєвого циклу, тож
...               порівнюють ціну плюс те, скільки товар коштуватиме в
...               експлуатації та в утилізації. Цей критерій визначення
...               переможця відкриває набір критеріїв, яких API не приймає у
...               звичайній закупівлі, і пропозиції відповідають і на них теж.
...               Беруть участь троє учасників.
...
...               Усе інше йде так само, як у звичайному проході понад поріг.

Ресурс            ${CURDIR}/../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури Зі Зверненнями
Розбірка Suite        Закрити Сесію Процедури
Налаштування тесту    Пропустити Якщо Попередня Стадія Впала
Розбирання тестy      Запамʼятати Невдалу Стадію

Тестові теги      procedure:aboveThreshold    feature:lifeCycleCost    slow


*** Тест-кейси ***
Створити План Закупівлі
    [Документація]    План - це те, з чого створюється закупівля, тож він іде
    ...               першим і його ставлять у розклад, перш ніж проти нього
    ...               можна витратити кошти.
    [Теги]    phase:planning

    Запланувати Закупівлю

Опублікувати Закупівлю
    [Документація]    Закупівля одразу оголошує, що переможця визначають за
    ...               вартістю життєвого циклу - саме це дозволяє їй мати
    ...               критерії вартості експлуатації, обслуговування та
    ...               завершення життєвого циклу поряд зі звичайними.
    [Теги]    phase:tendering

    ${tender}=      Створити Відкриту Закупівлю    lots=3    awardCriteria=lifeCycleCost

    ${file}=        Дані Документа    title=tender_document_file.txt
    Додати Документ Закупівлі    ${file}
    ${proforma}=    Дані Проекту Договору
    ...             title=tender_document_contract_proforma.txt
    Додати Документ Закупівлі    ${proforma}

    ${criteria}=    Опублікувати Критерії    ${tender}    folder=aboveThreshold.lcc

    ${notice}=      Дані Файлу Підпису    title=tender_document_notice.p7s
    Додати Документ Закупівлі    ${notice}

    ${tender}=      Відкрити Прийом Пропозицій

    Set Suite Variable    ${TENDER}      ${tender}
    Set Suite Variable    ${CRITERIA}    ${criteria}

Поставити Звернення І Відповісти На Них
    [Документація]    Двоє постачальників звертаються щодо закупівлі, і
    ...               замовник відповідає обом. Звернення без відповіді
    ...               тримало б закупівлю в періоді подання пропозицій, тож
    ...               відповіді на них - частина шляху до аукціону.
    [Теги]    phase:tendering    feature:questions

    FOR    ${index}    IN RANGE    2
        ${data}=        Дані Звернення
        ${question}=    Поставити Звернення    ${data}    index=${index}
        ${answer}=      Дані Відповіді На Звернення
        ${question}=    Відповісти На Звернення    ${answer}    index=${index}
        Should Not Be Empty    ${question}[dateAnswered]
    END

Подати Шість Скарг На Закупівлю
    [Документація]    Шість скарг на закупівлю, поки що всі залишені в
    ...               чернетках. Їх подають разом, щоб потім кожну можна було
    ...               довести до іншого завершення.
    [Теги]    phase:tendering    feature:complaints

    Потрібні Токени Органу Оскарження Та Бота
    FOR    ${index}    IN RANGE    6
        ${data}=         Дані Скарги    ${TENDER}[id]    relates_to=tender
        ${complaint}=    Створити Скаргу На Закупівлю    ${data}    index=${index}
        Should Be Equal    ${complaint}[status]    draft
    END

Провести Першу Скаргу До Кінця
    [Документація]    Перша скарга проходить увесь шлях: бот передає її
    ...               органу оскарження, далі йде обмін повідомленнями, орган
    ...               приймає скаргу і задовольняє її, а замовник повідомляє,
    ...               що він на це зробив.
    ...
    ...               Повідомлення - це розмова. Орган оскарження пише одній
    ...               стороні, ця сторона відповідає органу, і кожна відповідь
    ...               вказує, на яке повідомлення вона відповідає.
    [Теги]    phase:tendering    feature:complaints

    ${complaint}=    Змінити Скаргу На Закупівлю    ${{ {'data': {'status': 'pending'}} }}
    ...                                        index=0    role=bot
    ${objection}=    Set Variable    ${complaint}[objections][0][id]

    ${to_complainer}=    Дані Повідомлення У Скарзі    ${objection}    recipient=complaint_owner
    ${c}=    Написати У Скаргу На Закупівлю    ${to_complainer}
    ...      index=0    post_index=0    role=reviewer

    ${answer}=    Дані Повідомлення У Скарзі    ${objection}
    ...           recipient=aboveThresholdReviewers    related_post=${c}[posts][0][id]
    ${c}=    Написати У Скаргу На Закупівлю    ${answer}
    ...      index=0    post_index=1    role=complainer

    ${to_owner}=    Дані Повідомлення У Скарзі    ${objection}    recipient=tender_owner
    ${c}=    Написати У Скаргу На Закупівлю    ${to_owner}
    ...      index=0    post_index=2    role=reviewer

    ${answer}=    Дані Повідомлення У Скарзі    ${objection}
    ...           recipient=aboveThresholdReviewers    related_post=${c}[posts][2][id]
    ${c}=    Написати У Скаргу На Закупівлю    ${answer}
    ...      index=0    post_index=3    role=tenderer
    Length Should Be    ${c}[posts]    4

    ${accept}=    Дані Прийняття Скарги
    Змінити Скаргу На Закупівлю    ${accept}    index=0    role=reviewer
    Змінити Скаргу На Закупівлю    ${{ {'data': {'status': 'satisfied'}} }}
    ...                       index=0    role=reviewer
    ${complaint}=    Змінити Скаргу На Закупівлю
    ...              ${{ {'data': {'status': 'resolved', 'tendererAction': 'Внесено зміни'}} }}
    ...              index=0    role=tenderer
    Should Be Equal    ${complaint}[status]    resolved

Завершити Решту Скарг Кожну По-Своєму
    [Документація]    Решта скарг доходять до інших завершень: припинена,
    ...               бо замовник усунув порушення, на яке скаржились;
    ...               відхилена по суті; визнана недійсною як дублікат; і
    ...               відкликана як подана помилково. Одну залишають у
    ...               чернетці - це теж завершення.
    [Теги]    phase:tendering    feature:complaints

    ${accept}=    Дані Прийняття Скарги

    Змінити Скаргу На Закупівлю    ${{ {'data': {'status': 'pending'}} }}    index=1    role=bot
    Змінити Скаргу На Закупівлю    ${accept}                                 index=1    role=reviewer
    ${stopped}=    Дані Відхилення Скарги    stopped    buyerViolationsCorrected
    ${c}=          Змінити Скаргу На Закупівлю    ${stopped}    index=1    role=reviewer
    Should Be Equal    ${c}[status]    stopped

    Змінити Скаргу На Закупівлю    ${{ {'data': {'status': 'pending'}} }}    index=2    role=bot
    Змінити Скаргу На Закупівлю    ${accept}                                 index=2    role=reviewer
    ${c}=    Змінити Скаргу На Закупівлю    ${{ {'data': {'status': 'declined'}} }}
    ...                                index=2    role=reviewer
    Should Be Equal    ${c}[status]    declined

    Змінити Скаргу На Закупівлю    ${{ {'data': {'status': 'pending'}} }}    index=3    role=bot
    ${invalid}=    Дані Відхилення Скарги    invalid    alreadyExists
    ${c}=          Змінити Скаргу На Закупівлю    ${invalid}    index=3    role=reviewer
    Should Be Equal    ${c}[status]    invalid

    ${mistaken}=    Дані Помилкової Скарги
    ${c}=           Змінити Скаргу На Закупівлю    ${mistaken}    index=4    role=complainer
    Should Be Equal    ${c}[status]    mistaken

    # скаргу 5 навмисно залишають у чернетці, як її залишає тека даних

Зібрати Пропозиції
    [Документація]    Троє учасників подають по пропозиції і відповідають на
    ...               кожен критерій, разом з критеріями вартості життєвого
    ...               циклу.
    [Теги]    phase:tendering

    # третій лот навмисно залишають без пропозицій, щоб поруч із лотами, за
    # які змагаються, ішов лот, на який не подав ніхто
    ${wanted}=    Evaluate    [$TENDER["lots"][0]["id"], $TENDER["lots"][1]["id"]]
    FOR    ${index}    IN RANGE    3
        Подати Пропозицію    ${TENDER}    ${CRITERIA}    index=${index}    lot_ids=${wanted}
    END
    ${bids}=    Отримати Пропозиції
    Length Should Be    ${bids}    3
    Дочекатись Наступної Перевірки Закупівлі

Провести Аукціон
    [Документація]    Аукціон ранжує пропозиції. Закупівля проходить через нього
    ...               і виходить на кваліфікацію, де починається визначення
    ...               переможців.
    [Теги]    phase:auction

    Дочекатись Статусу Закупівлі    ${{ ['active.auction', 'active.qualification', 'active.awarded'] }}
    ...                   fail_status=unsuccessful
    Дочекатись Аукціону
    Дочекатись Статусу Закупівлі    ${{ ['active.qualification', 'active.awarded'] }}
    ...                   fail_status=unsuccessful

Кваліфікувати Першого Переможця
    [Документація]    Першого переможця кваліфікують, рішення підписують і
    ...               активують - це відкриває період, протягом якого на нього
    ...               можна поскаржитись.
    [Теги]    phase:qualification

    Дочекатись Документів ЄДР
    ${award}=    Кваліфікувати Переможця    index=0
    Set Suite Variable    ${AWARD}    ${award}

Подати Шість Скарг На Переможця
    [Документація]    Ті самі шість завершень, що й у скарг на закупівлю,
    ...               цього разу проти рішення про переможця, а не проти умов
    ...               закупівлі: задоволена й виконана, припинена, відхилена,
    ...               недійсна, відкликана, і одна залишена в чернетці.
    [Теги]    phase:qualification    feature:complaints

    FOR    ${index}    IN RANGE    6
        ${objection}=    Дані Заперечення    ${AWARD}[id]    relates_to=award
        ${data}=         Дані Скарги    ${AWARD}[id]    relates_to=award
        ...                                objections=${{ [$objection] }}
        Створити Скаргу На Переможця    ${data}    award_index=0    index=${index}
    END

    ${accept}=    Дані Прийняття Скарги

    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'pending'}} }}    award_index=0    index=0    role=bot
    Змінити Скаргу На Переможця    ${accept}                                 award_index=0    index=0    role=reviewer
    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'satisfied'}} }}  award_index=0    index=0    role=reviewer
    ${c}=    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'resolved', 'tendererAction': 'Внесено зміни'}} }}
    ...                               award_index=0    index=0    role=tenderer
    Should Be Equal    ${c}[status]    resolved

    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'pending'}} }}    award_index=0    index=1    role=bot
    Змінити Скаргу На Переможця    ${accept}                                 award_index=0    index=1    role=reviewer
    ${stopped}=    Дані Відхилення Скарги    stopped    buyerViolationsCorrected
    Змінити Скаргу На Переможця    ${stopped}    award_index=0    index=1    role=reviewer

    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'pending'}} }}    award_index=0    index=2    role=bot
    Змінити Скаргу На Переможця    ${accept}                                 award_index=0    index=2    role=reviewer
    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'declined'}} }}   award_index=0    index=2    role=reviewer

    Змінити Скаргу На Переможця    ${{ {'data': {'status': 'pending'}} }}    award_index=0    index=3    role=bot
    ${invalid}=    Дані Відхилення Скарги    invalid    alreadyExists
    Змінити Скаргу На Переможця    ${invalid}    award_index=0    index=3    role=reviewer

    ${mistaken}=    Дані Помилкової Скарги
    Змінити Скаргу На Переможця    ${mistaken}    award_index=0    index=4    role=complainer

Подати Вимоги До Першого Переможця
    [Документація]    Вимогу врегульовують усередині процедури: замовник на
    ...               неї відповідає, а скаржник каже, чи це вирішило справу.
    ...               Одну вимогу так і вирішують; другу натомість
    ...               відкликають.
    [Теги]    phase:qualification    feature:claims

    ${data}=    Дані Вимоги
    Створити Вимогу До Переможця    ${data}    award_index=0    index=0
    Змінити Вимогу До Переможця    ${{ {'data': {'status': 'claim'}} }}    award_index=0    index=0    role=complainer
    ${answer}=    Дані Відповіді На Вимогу    resolution_type=resolved
    Змінити Вимогу До Переможця    ${answer}    award_index=0    index=0    role=tenderer
    ${resolution}=    Дані Вирішення Вимоги    satisfied=${True}
    ${claim}=    Змінити Вимогу До Переможця    ${resolution}    award_index=0    index=0    role=complainer
    Should Be Equal    ${claim}[status]    resolved

    ${data}=    Дані Вимоги
    Створити Вимогу До Переможця    ${data}    award_index=0    index=1
    ${cancel}=    Дані Скасування Вимоги
    ${claim}=     Змінити Вимогу До Переможця    ${cancel}    award_index=0    index=1    role=complainer
    Should Be Equal    ${claim}[status]    cancelled

Визначити Другого Переможця І Потім Скасувати Його
    [Документація]    Другого переможця підтверджують, вимогу проти нього
    ...               відхиляють, а потім визначення скасовують. Скасування
    ...               переможця, який уже був активним, повертає закупівлю до
    ...               визначення переможців.
    [Теги]    phase:qualification

    Кваліфікувати Переможця    index=1

    ${data}=    Дані Вимоги    status=claim
    Створити Вимогу До Переможця    ${data}    award_index=1    index=0
    ${answer}=    Дані Відповіді На Вимогу    resolution_type=declined
    Змінити Вимогу До Переможця    ${answer}    award_index=1    index=0    role=tenderer

    ${cancelled}=    Дані Зміни Переможця    cancelled
    ${award}=        Змінити Переможця    ${cancelled}    index=1
    Should Be Equal    ${award}[status]    cancelled
    Отримати Вимоги До Переможця    award_index=1

Відмовити Третьому Учаснику
    [Документація]    Третьому учаснику відмовляють: не кваліфікований і не
    ...               відповідає критеріям прийнятності, через що визначення
    ...               переможця стає неуспішним. Вимогу, яка за цим іде,
    ...               відхиляють, і скаржник це фіксує, відмовившись прийняти
    ...               відповідь.
    [Теги]    phase:qualification

    ${refused}=    Дані Кваліфікації Переможця    qualified=${False}    eligible=${False}
    Змінити Переможця    ${refused}    index=2
    ${notice}=     Дані Файлу Підпису    title=tender_award_2_document_file.p7s
    Додати Документ Переможця    ${notice}    index=2
    ${award}=      Змінити Переможця    ${{ {'data': {'status': 'unsuccessful'}} }}    index=2
    Should Be Equal    ${award}[status]    unsuccessful

    ${data}=    Дані Вимоги    status=claim
    Створити Вимогу До Переможця    ${data}    award_index=2    index=0
    ${answer}=    Дані Відповіді На Вимогу    resolution_type=declined
    Змінити Вимогу До Переможця    ${answer}    award_index=2    index=0    role=tenderer
    ${unsatisfied}=    Дані Вирішення Вимоги    satisfied=${False}
    Змінити Вимогу До Переможця    ${unsatisfied}    award_index=2    index=0    role=complainer
    Отримати Вимоги До Переможця    award_index=2

Визначити Четвертого Переможця
    [Документація]    Четвертого переможця підтверджують, і він стоїть.
    ...               Коли періоди оскарження всіх переможців вичерпані,
    ...               закупівля переходить до визначених переможців і можна
    ...               працювати над договорами.
    [Теги]    phase:qualification

    Кваліфікувати Переможця    index=3
    Дочекатись Періоду Оскарження Переможців
    Дочекатись Статусу Закупівлі    active.awarded    fail_status=unsuccessful

Підписати І Закрити Договори
    [Документація]    Кожен лот, що лишився, має договір. Обидві сторони
    ...               називають свого підписанта, договори підписують, один
    ...               переоцінюють і змінюють, а закриття всіх завершує
    ...               закупівлю.
    [Теги]    phase:contracting

    FOR    ${index}    IN    ${0}    ${2}
        Підписати Договір    index=${index}
    END

    ${contract}=    Отримати Договір    index=0
    ${value}=       Evaluate    round(${contract}[value][amount], 2)
    Змінити Договір  ${{ {'data': {'value': {'amount': $value, 'amountNet': $value, 'valueAddedTaxIncluded': False}}} }}
    ...             index=0
    Внести Зміну До Договору  index=0    rationale_type=fiscalYearExtension

    FOR    ${index}    IN    ${0}    ${2}
        ${contract}=    Отримати Договір    index=${index}
        ${paid}=        Evaluate    round(${contract}[value][amount] * 0.9, 2)
        Завершити Договір    ${paid}    index=${index}
    END

    Дочекатись Статусу Закупівлі    complete
    Закупівля Має Бути Завершена    complete


*** Ключових слова ***
Відкрити Сесію Процедури Зі Зверненнями
    [Документація]    Цей сценарій ставить звернення, які запуск, налаштований
    ...               на швидкість, міг вимкнути.
    Запустити Сесію Процедури    disable_questions=${False}
    Set Suite Variable    ${PHASE_FAILED}    ${False}
