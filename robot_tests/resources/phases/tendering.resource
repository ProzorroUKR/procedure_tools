language: uk

*** Налаштування ***
Документація      Усе до завершення прийому пропозицій: план, створена з нього
...               закупівля, її критерії й документи, і самі пропозиції.

Ресурс            ${CURDIR}/../libraries.resource


*** Ключових слова ***
Запланувати Закупівлю
    [Документація]    Створити план і поставити його в розклад. З нього
    ...               створюють наступну закупівлю.
    [Аргументи]    ${procurement_method_type}=aboveThreshold    ${reporting}=${False}
    ${settings}=    Налаштування Запуску
    IF    ${reporting}
        ${plan}=    Дані Плану Звітування    acceleration=${settings}[acceleration]
    ELSE
        ${plan}=    Дані Плану    ${procurement_method_type}    acceleration=${settings}[acceleration]
    END
    Створити План    ${plan}
    Змінити План     ${{ {'data': {'status': 'scheduled'}} }}

Створити Відкриту Закупівлю
    [Документація]    Створити відкриту закупівлю із заданими лотами,
    ...               прискорену так, як вказують налаштування запуску.
    [Аргументи]    ${lots}=1    ${submission}=${None}    ${config}=${None}    ${items}=${None}
    ...            &{overrides}
    ${settings}=      Налаштування Запуску
    # без аукціону лот не має мінімального кроку, і API його не приймає
    ${has_auction}=   Evaluate    ($config or {}).get("hasAuction", True)
    # "lots" - це або скільки лотів побудувати, або самі лоти, коли сьюіт мусив
    # побудувати їх раніше: наприклад, щоб прив'язати до одного з них критерій
    ${prebuilt}=      Evaluate    isinstance($lots, list)
    IF    ${prebuilt}
        ${lot_list}=    Set Variable    ${lots}
    ELSE
        ${lot_list}=    Дані Лотів    ${lots}    with_minimal_step=${has_auction}
    END
    ${submission}=    Set Variable If    $submission is not None    ${submission}    ${settings}[submission]
    ${data}=        Дані Закупівлі    lots=${lot_list}
    ...                               items=${items}
    ...                               acceleration=${settings}[acceleration]
    ...                               submission=${submission}
    ...                               config=${config}
    ...                               &{overrides}
    ${tender}=      Створити Закупівлю    ${data}
    Should Be Equal     ${tender}[status]    draft
    Length Should Be    ${tender}[lots]      ${{ len($lot_list) }}
    RETURN    ${tender}

Створити Закупівлю Звітування
    [Документація]    Відзвітувати про закупівлю, яка вже відбулася.
    [Аргументи]    ${amount}=${500000}    &{overrides}
    ${settings}=    Налаштування Запуску
    ${data}=        Дані Закупівлі Звітування    amount=${amount}
    ...                                          acceleration=${settings}[acceleration]
    ...                                          &{overrides}
    ${tender}=      Створити Закупівлю    ${data}
    Should Be Equal    ${tender}[procurementMethodType]    reporting
    RETURN    ${tender}

Опублікувати Критерії
    [Документація]    Опублікувати критерії закупівлі й повернути їх з id,
    ...               які призначило API: саме з них будують відповіді
    ...               пропозиції.
    ...
    ...               ``folder`` називає теку даних, чиї критерії публікувати:
    ...               процедура не приймає критеріїв, які не є її власними.
    [Аргументи]    ${tender}    ${folder}=aboveThreshold
    ${data}=        Дані Критеріїв    lots=${tender}[lots]    folder=${folder}
    ${criteria}=    Опублікувати Критерії Закупівлі    ${data}
    Should Not Be Empty    ${criteria}
    RETURN    ${criteria}

Додати Документи Закупівлі
    [Документація]    Проект договору і підписане оголошення.
    ${proforma}=    Дані Проекту Договору
    Додати Документ Закупівлі    ${proforma}
    ${notice}=      Дані Файлу Підпису    title=tender_notice.p7s
    Додати Документ Закупівлі    ${notice}

Відкрити Прийом Пропозицій
    [Документація]    Перевести закупівлю в ``active.tendering``.
    ${data}=      Дані Зміни Закупівлі    active.tendering
    ${tender}=    Змінити Закупівлю       ${data}
    Should Be Equal    ${tender}[status]    active.tendering
    RETURN    ${tender}

Активувати Закупівлю
    [Документація]    Перевести закупівлю лімітованої процедури в ``active``.
    ${data}=      Дані Зміни Закупівлі    active
    ${tender}=    Змінити Закупівлю       ${data}
    Should Be Equal    ${tender}[status]    active
    RETURN    ${tender}

Подати Пропозицію
    [Документація]    Створити чернетку пропозиції з документами, відповісти на
    ...               критерії, підписати пропозицію і подати її.
    [Аргументи]    ${tender}    ${criteria}    ${index}=0    ${amounts}=${None}
    ...            ${answer_features}=${True}    ${lot_ids}=${None}    &{overrides}

    ${proposal}=       Дані Документа    title=bid_${index}_proposal.txt
    ${eligibility}=    Дані Документа    title=bid_${index}_eligibility.txt
    ${financial}=      Дані Документа    title=bid_${index}_financial.txt

    # закупівля з неціновими критеріями не приймає пропозицію, яка не відповіла
    # ні на один з них
    ${features}=    Evaluate    $tender.get("features") or []
    IF    ${answer_features} and ${features}
        ${parameters}=    Дані Параметрів    ${features}
    ELSE
        ${parameters}=    Set Variable    ${None}
    END

    ${data}=    Дані Пропозиції    ${tender}
    ...                            amounts=${amounts}
    ...                            parameters=${parameters}
    ...                            lot_ids=${lot_ids}
    ...                            documents=${{ [$proposal] }}
    ...                            eligibility_documents=${{ [$eligibility] }}
    ...                            financial_documents=${{ [$financial] }}
    ...                            &{overrides}
    ${bid}=     Створити Пропозицію    ${data}    index=${index}
    Should Be Equal    ${bid}[status]    draft

    ${responses}=    Дані Відповідей На Вимоги    ${criteria}
    ...                                           document_title=${proposal}[data][title]
    Додати Відповіді На Критерії    ${responses}    index=${index}

    ${signature}=    Дані Підпису Пропозиції    title=bid_${index}_proposal.p7s
    Додати Документ Пропозиції    ${signature}    index=${index}

    ${bid}=    Змінити Пропозицію    ${{ {'data': {'status': 'pending'}} }}    index=${index}
    Should Be Equal    ${bid}[status]    pending
    RETURN    ${bid}
