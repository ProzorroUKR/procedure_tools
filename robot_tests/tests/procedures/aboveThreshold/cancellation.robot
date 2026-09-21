language: uk

*** Налаштування ***
Документація      Понад поріг, де лоти скасовують по ходу процедури.
...
...               Скасування - не одна дія: його створюють чернеткою, воно
...               потребує підстави й підписаного протоколу, перш ніж його
...               можна подати, а подане вичікує період, протягом якого
...               будь-хто може поскаржитись. Задоволена скарга зупиняє
...               скасування; відхилена - пропускає його.
...
...               Пʼять лотів проходять цей шлях у різні моменти - до
...               подання пропозицій, після аукціону, коли визначення
...               переможця вже стоїть, і коли вже існує договір, - і відмови
...               по дорозі тут така сама тема, як і скасування, що вдалися.

Ресурс            ${CURDIR}/../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури Зі Зверненнями
Розбірка Suite        Закрити Сесію Процедури
Налаштування тесту    Пропустити Якщо Попередня Стадія Впала
Розбирання тестy      Запамʼятати Невдалу Стадію

Тестові теги      procedure:aboveThreshold    feature:cancellation    slow


*** Тест-кейси ***
Опублікувати Закупівлю
    [Документація]    Пʼять лотів, щоб кілька з них можна було скасувати в
    ...               різні моменти, не завершивши закупівлю.
    [Теги]    phase:tendering

    Запланувати Закупівлю    aboveThreshold
    ${tender}=      Створити Відкриту Закупівлю    lots=5
    ${criteria}=    Опублікувати Критерії    ${tender}
    Додати Документи Закупівлі
    ${tender}=      Відкрити Прийом Пропозицій

    Length Should Be    ${tender}[lots]    5
    Set Suite Variable    ${TENDER}      ${tender}
    Set Suite Variable    ${CRITERIA}    ${criteria}
    Set Suite Variable    ${LOTS}        ${tender}[lots]

Відкликати Скасування, Не Подавши Його
    [Документація]    Чернетку скасування всієї закупівлі передумують і
    ...               відкликають. У закупівлі при цьому не змінюється нічого.
    [Теги]    phase:cancellation

    ${data}=            Дані Скасування
    ${cancellation}=    Створити Скасування    ${data}    index=0
    Should Be Equal    ${cancellation}[status]    draft

    ${withdraw}=        Дані Зміни Скасування    unsuccessful
    ${cancellation}=    Змінити Скасування    ${withdraw}    index=0
    Should Be Equal    ${cancellation}[status]    unsuccessful

    ${tender}=    Перечитати Закупівлю
    Should Be Equal    ${tender}[status]    active.tendering

Скарга Може Зупинити Скасування
    [Документація]    Лот виставляють на скасування. Подати його без
    ...               підписаного протоколу не можна. Подану скаргу на
    ...               скасування задовольняють, і завершується саме
    ...               скасування, а не лот.
    [Теги]    phase:cancellation    feature:complaints

    Потрібні Токени Органу Оскарження Та Бота

    ${data}=    Дані Скасування    related_lot=${LOTS}[2][id]
    Створити Скасування    ${data}    index=1

    ${submit}=    Дані Зміни Скасування    pending
    Run Keyword And Expect Error
    ...    *cancellationReport*pkcs7-signature is required*
    ...    Змінити Скасування    ${submit}    index=1

    ${report}=    Дані Протоколу Скасування    title=cancellation_1_report.p7s
    Додати Документ Скасування    ${report}    index=1
    ${cancellation}=    Змінити Скасування    ${submit}    index=1
    Should Be Equal    ${cancellation}[status]    pending

    ${complaint}=    Дані Скарги    ${cancellation}[id]    relates_to=cancellation
    Створити Скаргу На Скасування    ${complaint}    cancellation_index=1    index=0
    Змінити Скаргу На Скасування    ${{ {'data': {'status': 'pending'}} }}
    ...                             cancellation_index=1    index=0    role=bot
    ${accept}=    Дані Прийняття Скарги
    Змінити Скаргу На Скасування    ${accept}    cancellation_index=1    index=0    role=reviewer
    Змінити Скаргу На Скасування    ${{ {'data': {'status': 'satisfied'}} }}
    ...                             cancellation_index=1    index=0    role=reviewer

    ${cancelled}=    Дані Зміни Скасування    unsuccessful
    ${cancellation}=    Змінити Скасування    ${cancelled}    index=1
    Should Be Equal    ${cancellation}[status]    unsuccessful

Виставити Лот На Скасування
    [Документація]    Лот виставляють на скасування, змінивши по дорозі
    ...               підставу і додавши і звичайний документ, і підписаний
    ...               протокол. Подання починає період, у якому будь-хто може
    ...               поскаржитись.
    [Теги]    phase:cancellation

    ${data}=    Дані Скасування    related_lot=${LOTS}[1][id]
    Створити Скасування    ${data}    index=2

    Змінити Скасування    ${{ {'data': {'reasonType': 'forceMajeure'}} }}    index=2

    ${file}=      Дані Документа    title=cancellation_2_file.txt
    Додати Документ Скасування    ${file}    index=2
    ${report}=    Дані Протоколу Скасування    title=cancellation_2_report.p7s
    Додати Документ Скасування    ${report}    index=2

    ${submit}=          Дані Зміни Скасування    pending
    ${cancellation}=    Змінити Скасування    ${submit}    index=2
    Should Be Equal    ${cancellation}[status]    pending

    ${second}=    Дані Скасування    related_lot=${LOTS}[1][id]
    Run Keyword And Expect Error
    ...    *Forbidden because of a pending cancellation*
    ...    Створити Скасування    ${second}    index=3

    ${activate}=    Дані Зміни Скасування    active
    Run Keyword And Expect Error
    ...    *Can't switch cancellation status from pending to active*
    ...    Змінити Скасування    ${activate}    index=2

Скасування, Що Очікує, Блокує Лише Свій Лот
    [Документація]    Поки лот чекає на скасування, його не можна зачіпати, але
    ...               решта закупівлі живе далі: інший лот можна додати,
    ...               змінити й видалити як завжди.
    ...
    ...               Це варто сказати, бо так було не завжди: скасування одного
    ...               лота, що очікувало, колись блокувало всі лоти, тож додати
    ...               новий теж було не можна.
    [Теги]    phase:tendering    feature:cancellation

    ${blocked}=    Set Variable    ${LOTS}[1][id]
    ${index}=      Evaluate    [lot["id"] for lot in $LOTS].index("${blocked}")

    Run Keyword And Expect Error
    ...    *pending cancellation*
    ...    Змінити Лот    ${{ {'data': {'title': 'Лот під скасуванням'}} }}    index=${index}

    ${data}=    Дані Лота    title=Лот доданий під час скасування
    ${lot}=     Додати Лот    ${{ {'data': $data} }}
    ${tender}=  Перечитати Закупівлю
    Should Be Equal    ${tender}[lots][-1][id]    ${lot}[id]

    ${added}=    Evaluate    len($tender["lots"]) - 1
    ${lot}=      Змінити Лот    ${{ {'data': {'title': 'Перейменований лот'}} }}    index=${added}
    Should Be Equal    ${lot}[title]    Перейменований лот

    Видалити Лот    index=${added}
    ${tender}=    Перечитати Закупівлю
    Should Be Equal As Integers    ${{ len($tender["lots"]) }}    5

Відхилена Скарга Пропускає Скасування
    [Документація]    Хтось скаржиться на скасування, а орган оскарження скаргу
    ...               відхиляє, тож скасування стоїть і лот іде.
    [Теги]    phase:cancellation    feature:complaints

    ${cancellation}=    Отримати Скасування    index=2
    ${complaint}=    Дані Скарги    ${cancellation}[id]    relates_to=cancellation
    Створити Скаргу На Скасування    ${complaint}    cancellation_index=2    index=0
    Змінити Скаргу На Скасування    ${{ {'data': {'status': 'pending'}} }}
    ...                             cancellation_index=2    index=0    role=bot
    ${accept}=    Дані Прийняття Скарги
    Змінити Скаргу На Скасування    ${accept}    cancellation_index=2    index=0    role=reviewer
    Змінити Скаргу На Скасування    ${{ {'data': {'status': 'declined'}} }}
    ...                             cancellation_index=2    index=0    role=reviewer

    ${cancellation}=    Дочекатись Статусу Скасування    active    index=2
    Should Be Equal    ${cancellation}[status]    active

Зібрати Пропозиції
    [Документація]    Двоє учасників подають пропозиції на лоти, які ще
    ...               стоять. Скасований лишають у спокої.
    [Теги]    phase:tendering

    ${wanted}=    Evaluate
    ...    [$LOTS[0]["id"], $LOTS[2]["id"], $LOTS[3]["id"], $LOTS[4]["id"]]
    FOR    ${index}    IN RANGE    2
        Подати Пропозицію    ${TENDER}    ${CRITERIA}    index=${index}    lot_ids=${wanted}
    END
    Дочекатись Наступної Перевірки Закупівлі

Провести Аукціон
    [Документація]    Аукціон ранжує пропозиції на лотах, які залишились.
    [Теги]    phase:auction

    Дочекатись Статусу Закупівлі    ${{ ['active.auction', 'active.qualification', 'active.awarded'] }}
    ...                             fail_status=unsuccessful
    Дочекатись Аукціону
    Дочекатись Статусу Закупівлі    ${{ ['active.qualification', 'active.awarded'] }}
    ...                             fail_status=unsuccessful

Скасувати Лот Після Аукціону
    [Документація]    Лот можна скасувати й після того, як подання пропозицій
    ...               завершилось, і цього разу на шляху не стоїть жодна
    ...               скарга.
    [Теги]    phase:cancellation

    ${data}=    Дані Скасування    related_lot=${LOTS}[3][id]
    Створити Скасування    ${data}    index=4
    ${report}=    Дані Протоколу Скасування    title=cancellation_4_report.p7s
    Додати Документ Скасування    ${report}    index=4
    Змінити Скасування    ${{ {'data': {'status': 'pending'}} }}    index=4
    ${cancellation}=    Дочекатись Статусу Скасування    active    index=4
    Should Be Equal    ${cancellation}[status]    active
    Отримати Переможців

Визначити Переможців На Лотах, Що Лишились
    [Документація]    Лоти, які вціліли, отримують своїх переможців.
    [Теги]    phase:qualification

    Кваліфікувати Переможця    index=0
    Кваліфікувати Переможця    index=1
    Отримати Переможців

Скасувати Лоти З Визначеними Переможцями
    [Документація]    Лот, чиє визначення переможця ще в межах свого періоду
    ...               оскарження, скасувати не можна. Коли цей період минув -
    ...               можна, як і лот, на якому переможця вже визначили.
    [Теги]    phase:cancellation

    ${early}=    Дані Скасування    related_lot=${LOTS}[4][id]
    Run Keyword And Expect Error
    ...    *Cancellation can't be add when exists active complaint period*
    ...    Створити Скасування    ${early}    index=5

    Дочекатись Періоду Оскарження Переможців

    ${data}=    Дані Скасування    related_lot=${LOTS}[2][id]
    Створити Скасування    ${data}    index=5
    ${report}=    Дані Протоколу Скасування    title=cancellation_5_report.p7s
    Додати Документ Скасування    ${report}    index=5
    Змінити Скасування    ${{ {'data': {'status': 'pending'}} }}    index=5
    Дочекатись Статусу Скасування    active    index=5
    Отримати Переможців

    ${data}=    Дані Скасування    related_lot=${LOTS}[4][id]
    Створити Скасування    ${data}    index=6
    ${report}=    Дані Протоколу Скасування    title=cancellation_6_report.p7s
    Додати Документ Скасування    ${report}    index=6
    Змінити Скасування    ${{ {'data': {'status': 'pending'}} }}    index=6
    Дочекатись Статусу Скасування    active    index=6
    Отримати Договори

Скасувати Останній Лот, Коли Договір Уже Існує
    [Документація]    Договір не є захистом: лот, що стоїть за ним, усе одно
    ...               можна скасувати, і договір іде разом з ним.
    [Теги]    phase:contracting    phase:cancellation

    Отримати Права На Договір    index=0
    ${buyer}=       Дані Підписанта
    Заповнити Підписанта Замовника        ${buyer}       index=0
    ${supplier}=    Дані Підписанта
    Заповнити Підписанта Постачальника    ${supplier}    index=0

    ${data}=    Дані Скасування    related_lot=${LOTS}[0][id]
    Створити Скасування    ${data}    index=7
    ${report}=    Дані Протоколу Скасування    title=cancellation_7_report.p7s
    Додати Документ Скасування    ${report}    index=7
    Змінити Скасування    ${{ {'data': {'status': 'pending'}} }}    index=7
    Дочекатись Статусу Скасування    active    index=7
    Отримати Договори

Закупівля Завершується Скасованою
    [Документація]    Коли скасовані всі лоти, купувати вже нічого, тож
    ...               закупівля йде слідом за своїми лотами.
    [Теги]    phase:cancellation

    Дочекатись Статусу Закупівлі    cancelled
    Закупівля Має Бути Завершена    cancelled


*** Ключових слова ***
Відкрити Сесію Процедури Зі Зверненнями
    [Документація]    Кроки зі скаргами потребують ролей органу оскарження, а
    ...               звернення в запуску, налаштованому на швидкість, можуть
    ...               бути вимкнені.
    Запустити Сесію Процедури    disable_questions=${False}
    Set Suite Variable    ${PHASE_FAILED}    ${False}
