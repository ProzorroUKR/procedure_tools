language: uk

*** Налаштування ***
Документація      Звітування про товар з вимогою локалізації.
...
...               Та сама процедура, що й звичайний прохід звітування, з однією
...               додачею: критерій про ступінь локалізації виробництва. Цей
...               критерій прив'язують до предмета закупівлі, а не до
...               закупівлі в цілому, і предмет мусить назвати товар з
...               каталогу - через це товар тут не той, що зазвичай.

Ресурс            ${CURDIR}/../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури
Розбірка Suite        Закрити Сесію Процедури
Налаштування тесту    Пропустити Якщо Попередня Стадія Впала
Розбирання тестy      Запамʼятати Невдалу Стадію

Тестові теги      procedure:reporting    feature:criteria


*** Змінні ***
${AWARD_AMOUNT}       ${475000}
${CONTRACT_AMOUNT}    ${475000.45}
${PAID_AMOUNT}        ${450000}


*** Тест-кейси ***
Створити План Закупівлі
    [Документація]    План мусить бути про той самий клас товарів, що й
    ...               закупівля, тож він вказує класифікатор, до якого
    ...               належить локалізований товар.
    [Теги]    phase:planning

    ${settings}=    Налаштування Запуску
    # план мусить бути про той самий клас товарів, що й закупівля, а критерій
    # локалізації потребує товару з каталогу
    ${classification}=    Дані Класифікатора    id=31120000-3    description=Генератори
    ${item}=        Дані Предмета Закупівлі    quantity=1000    classification=${classification}
    ${plan}=        Дані Плану Звітування    acceleration=${settings}[acceleration]
    ...                                      classification=${classification}
    ...                                      items=${{ [$item] }}
    Створити План    ${plan}
    Змінити План     ${{ {'data': {'status': 'scheduled'}} }}

Відзвітувати Про Закупівлю
    [Документація]    Закупівлю публікують з критерієм локалізації, який
    ...               прив'язаний до предмета закупівлі, якого він стосується,
    ...               а не до закупівлі в цілому. На предметі, що не називає
    ...               товару з каталогу, API цього критерію не приймає.
    [Теги]    phase:tendering

    ${settings}=    Налаштування Запуску
    ${item}=        Дані Локалізованого Предмета Закупівлі
    ${data}=        Дані Закупівлі Звітування    acceleration=${settings}[acceleration]
    ...                                          items=${{ [$item] }}
    ${tender}=      Створити Закупівлю    ${data}
    Should Be Equal    ${tender}[procurementMethodType]    reporting

    ${file}=        Дані Документа    title=tender_document_file.txt
    Додати Документ Закупівлі    ${file}
    ${proforma}=    Дані Проекту Договору
    ...             title=tender_document_contract_proforma.txt
    Додати Документ Закупівлі    ${proforma}

    ${item_id}=     Set Variable    ${tender}[items][0][id]
    ${criterion}=   Дані Критерію
    ...             CRITERION.OTHER.SUBJECT_OF_PROCUREMENT.LOCAL_ORIGIN_LEVEL
    ...             related_item=${item_id}
    ${criteria}=    Опублікувати Критерії Закупівлі    ${{ {'data': [$criterion]} }}
    Should Be Equal    ${criteria}[0][relatesTo]      item
    Should Be Equal    ${criteria}[0][relatedItem]    ${item_id}

    Активувати Закупівлю

Визначити Постачальника Переможцем
    [Документація]    Лімітована процедура не має пропозицій, тож замовник сам
    ...               називає постачальника, у якого купив, підписує рішення і
    ...               активує його.
    [Теги]    phase:qualification

    ${data}=    Дані Переможця    amount=${AWARD_AMOUNT}
    Визначити Переможця    ${data}
    Дочекатись Статусу Закупівлі    active    delay=${20}
    Дочекатись Документів ЄДР

    ${qualified}=    Дані Кваліфікації Переможця    eligible=${None}
    Змінити Переможця    ${qualified}    index=0
    ${notice}=       Дані Файлу Підпису
    ...              title=tender_award_0_document_file.p7s
    Додати Документ Переможця    ${notice}    index=0
    ${activate}=     Дані Зміни Переможця    active
    ${award}=        Змінити Переможця    ${activate}    index=0
    Should Be Equal    ${award}[status]    active

Підписати Договір І Внести До Нього Зміну
    [Документація]    Взяття прав на договір - це те, що взагалі дозволяє
    ...               його змінювати. Далі договір підписують, переоцінюють, а
    ...               нову ціну фіксують як зміну до нього.
    [Теги]    phase:contracting

    Отримати Права На Договір    index=0

    ${contract}=    Отримати Договір    index=0
    ${active}=      Дані Активації Договору    ${contract}    amount=${AWARD_AMOUNT}
    ${contract}=    Змінити Договір    ${active}    index=0
    Should Be Equal    ${contract}[status]    active

    ${value}=       Дані Вартості Договору    ${CONTRACT_AMOUNT}
    Змінити Договір    ${value}    index=0

    Внести Зміну До Договору    index=0    rationale_type=itemPriceChange

Закрити Договір
    [Документація]    Завершення договору із зазначенням суми, яку справді
    ...               сплатили, - це те, що завершує закупівлю.
    [Теги]    phase:contracting

    Завершити Договір    ${PAID_AMOUNT}    index=0
    Дочекатись Статусу Закупівлі    complete
    Закупівля Має Бути Завершена    complete
