language: uk

*** Налаштування ***
Документація      Що API відхиляє при створенні й початковому налаштуванні
...               закупівлі.
...
...               Це найдешевші перевірки з усіх: більшості не потрібна
...               процедура взагалі - лише запит, який мусить повернутися
...               відхиленим. Кожна називає причину, якої очікує, бо тест, що
...               приймає будь-яку невдачу, проходить з неправильної причини.

Ресурс            ${CURDIR}/../../../../resources/procedure.resource

Налаштування Suite    Відкрити Сесію Процедури
Розбірка Suite        Закрити Сесію Процедури

Тестові теги      negative    procedure:aboveThreshold


*** Тест-кейси ***
Закупівля Без Аукціону Не Може Мати Мінімального Кроку
    [Документація]    Мінімальний крок аукціону - це на скільки пропозиція
    ...               мусить перевищити попередню під час аукціону. Без
    ...               аукціону перевищувати нічого, тож поле не має сенсу.
    [Теги]    config:hasAuction

    ${config}=      Дані Конфігу Закупівлі    hasAuction=${False}
    ${lots}=        Дані Лотів    1
    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі    lots=${lots}    config=${config}
    ...                               acceleration=${settings}[acceleration]
    # повертаємо мінімальний крок назад - саме його прибирає конструктор даних
    ${data}=        Змінити Дані    ${data}    data.lots.0.minimalStep=${{ {'amount': 25, 'currency': 'UAH'} }}
    Run Keyword And Expect Error
    ...    *minimalStep*Rogue field*
    ...    Створити Закупівлю    ${data}

Закупівля Без Аукціону Не Може Назвати Режим Подання
    [Документація]    Режим подання налаштовує, як пропозиції потрапляють
    ...               в аукціон, тож його відхиляють, коли аукціону немає.
    [Теги]    config:hasAuction

    ${config}=      Дані Конфігу Закупівлі    hasAuction=${False}
    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі    lots=${{ [] }}    config=${config}
    ...                               acceleration=${settings}[acceleration]
    ${data}=        Змінити Дані    ${data}
    ...             data.submissionMethodDetails=quick(mode:fast-forward)
    Run Keyword And Expect Error
    ...    *submissionMethodDetails*Rogue field*
    ...    Створити Закупівлю    ${data}

Закупівлю Не Створити Без Предметів Закупівлі
    [Документація]    Без них немає що купувати.

    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі    acceleration=${settings}[acceleration]
    ${data}=        Змінити Дані    ${data}    data.items=${{ [] }}
    Run Keyword And Expect Error
    ...    *items*at least 1 item*
    ...    Створити Закупівлю    ${data}

Невідоме Поле Відхиляється Навідріз
    [Документація]    API не приймає жодного поля, якого не знає, і саме через
    ...               це випадковий аргумент конструктора даних видно одразу.

    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі    acceleration=${settings}[acceleration]
    ${data}=        Змінити Дані    ${data}    data.somethingInvented=yes
    Run Keyword And Expect Error
    ...    *somethingInvented*Rogue field*
    ...    Створити Закупівлю    ${data}

Критерії Вартості Життєвого Циклу Вимагають Відповідного Критерію Визначення Переможця
    [Документація]    Ці критерії про те, скільки товар коштує у володінні, тож
    ...               вони мають сенс лише тоді, коли закупівлю так і оцінюють.
    [Теги]    feature:criteria

    ${settings}=    Налаштування Запуску
    ${lots}=        Дані Лотів    1
    ${data}=        Дані Закупівлі    lots=${lots}    acceleration=${settings}[acceleration]
    ${tender}=      Створити Закупівлю    ${data}

    ${criteria}=    Дані Критеріїв    lots=${tender}[lots]    folder=aboveThreshold.lcc
    Run Keyword And Expect Error
    ...    *lifeCycleCost awardCriteria*
    ...    Опублікувати Критерії Закупівлі    ${criteria}

Замовник Будь-Якого Виду Поки Що Приймається
    [Документація]    Які види замовників можуть проводити які процедури,
    ...               записано в стандартах, і API відхиляє ті, що не пасують -
    ...               але лише з 2027-02-23, дати, з якої перевірку ввімкнено.
    ...               Доти загальний вид "other" проходить і в закупівлі понад
    ...               поріг, що цей тест і фіксує. Очікується, що він почне
    ...               падати, коли дата настане, і тоді стане тестом відмови.

    ${data}=      Закупівля Під Перевіркою
    ${entity}=    Дані Замовника    kind=other
    ${data}=      Змінити Дані    ${data}    data.procuringEntity=${entity}
    ${tender}=    Створити Закупівлю    ${data}
    Should Be Equal    ${tender}[procuringEntity][kind]    other

Відкрита Закупівля Не Є Лімітованою Процедурою
    [Документація]    Метод закупівлі й тип процедури мусять узгоджуватись між
    ...               собою.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.procurementMethod=limited
    Run Keyword And Expect Error
    ...    *procurementMethod should be open*
    ...    Створити Закупівлю    ${data}

Категорія Предмета Закупівлі Мусить Бути Однією З Відомих API
    [Документація]    Товари, послуги або роботи: те, що купують, вирішує, які
    ...               правила застосовуються до закупівлі, тож вигадати це не
    ...               можна.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.mainProcurementCategory=animals
    Run Keyword And Expect Error
    ...    *mainProcurementCategory*Value must be one of*
    ...    Створити Закупівлю    ${data}

Очікувану Вартість Вказують Без ПДВ
    [Документація]    Очікувані вартості порівнюють між закупівлями, тож
    ...               усі вони подаються однаково.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.value.valueAddedTaxIncluded=${True}
    Run Keyword And Expect Error
    ...    *valueAddedTaxIncluded should be false*
    ...    Створити Закупівлю    ${data}

Центральна Закупівельна Організація Мусить Назвати Покупців
    [Документація]    ЦЗО здійснює закупівлі в інтересах інших замовників, тож
    ...               вона мусить вказати, хто вони.

    ${data}=      Закупівля Під Перевіркою
    ${entity}=    Дані Замовника    kind=central
    ${data}=      Змінити Дані    ${data}    data.procuringEntity=${entity}
    Run Keyword And Expect Error
    ...    *buyers*This field is required*
    ...    Створити Закупівлю    ${data}

Закупівля Мусить Вказати Етапи Оплати Й Поставки
    [Документація]    Етапи оплати й поставки - це те, до чого постачальник
    ...               може притягнути замовника, тож відкрита закупівля без них
    ...               не виходить.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.milestones=${{ [] }}
    Run Keyword And Expect Error
    ...    *at least one milestone*
    ...    Створити Закупівлю    ${data}

Частки Етапів Мусять Складатися У Сто Відсотків
    [Документація]    Етапи одного виду ділять між собою всю оплату, тож їхні
    ...               частки дають сто відсотків.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.milestones.0.percentage=${10}
    Run Keyword And Expect Error
    ...    *milestone percentages*is not equal 100*
    ...    Створити Закупівлю    ${data}

Предмети Закупівлі Мусять Бути Одного Класу
    [Документація]    Одна закупівля купує щось одне. Купівля двох
    ...               непов'язаних речей разом відсікла б постачальників і
    ...               тих, і тих.

    ${data}=     Закупівля Під Перевіркою
    ${other}=    Дані Класифікатора    id=44617100-9    description=Коробки картонні
    ${item}=     Дані Предмета Закупівлі    classification=${other}
    ${data}=     Змінити Дані    ${data}    data.items.1=${item}
    Run Keyword And Expect Error
    ...    *should be identical*
    ...    Створити Закупівлю    ${data}

Предмет Закупівлі Мусить Вказати Дату Поставки
    [Документація]    Дата поставки - частина того, до чого зобов'язується
    ...               постачальник, тож її вимагають від кожного предмета
    ...               закупівлі.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.items.0.deliveryDate=${None}
    Run Keyword And Expect Error
    ...    *deliveryDate*This field is required*
    ...    Створити Закупівлю    ${data}

Предмет Закупівлі Мусить Вказати Одиницю Виміру
    [Документація]    Без одиниці виміру не зрозуміти, що взагалі означала б
    ...               ціна за одиницю.

    ${data}=    Закупівля Під Перевіркою
    ${data}=    Змінити Дані    ${data}    data.items.0.unit=${None}
    Run Keyword And Expect Error
    ...    *unit*This field is required*
    ...    Створити Закупівлю    ${data}

Предмет Закупівлі Може Належати Лише Лоту Своєї Закупівлі
    [Документація]    Лот, до якого прив'язаний предмет закупівлі, мусить бути
    ...               одним з лотів, що створюються поруч із ним.

    ${settings}=    Налаштування Запуску
    ${lots}=        Дані Лотів    1
    ${data}=        Дані Закупівлі    lots=${lots}    acceleration=${settings}[acceleration]
    ${data}=        Змінити Дані    ${data}    data.items.0.relatedLot=${{ __import__('uuid').uuid4().hex }}
    Run Keyword And Expect Error
    ...    *relatedLot should be one of lots*
    ...    Створити Закупівлю    ${data}

Мінімальний Крок Не Може Перевищувати Лот, Якому Належить
    [Документація]    Крок - це на скільки одна пропозиція мусить перевищити
    ...               попередню, тож крок, більший за сам лот, завершив би
    ...               аукціон, не давши йому початися.

    ${settings}=    Налаштування Запуску
    ${lots}=        Дані Лотів    1    amount=${2500}
    ${data}=        Дані Закупівлі    lots=${lots}    acceleration=${settings}[acceleration]
    ${data}=        Змінити Дані    ${data}    data.lots.0.minimalStep.amount=${5000}
    Run Keyword And Expect Error
    ...    *Minimal step value should be less than lot value*
    ...    Створити Закупівлю    ${data}

Мінімальний Крок Успадковує Валюту Закупівлі
    [Документація]    Крок в одній валюті й вартість в іншій порівняти було б
    ...               неможливо, тож замість відхилити лот API перезаписує
    ...               валюту й режим ПДВ кроку із закупівлі. Надіслана
    ...               чужа валюта не змінює нічого.

    ${settings}=    Налаштування Запуску
    ${lots}=        Дані Лотів    1
    ${data}=        Дані Закупівлі    lots=${lots}    acceleration=${settings}[acceleration]
    ${data}=        Змінити Дані    ${data}    data.lots.0.minimalStep.currency=USD
    ${tender}=      Створити Закупівлю    ${data}
    Should Be Equal    ${tender}[lots][0][minimalStep][currency]    ${tender}[value][currency]


*** Ключових слова ***
Закупівля Під Перевіркою
    [Документація]    Закупівля понад поріг, яку прийняли б як вона є, щоб те,
    ...               що змінює тест, було єдиною причиною, яку API може мати
    ...               для відмови.
    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі    acceleration=${settings}[acceleration]
    RETURN    ${data}
