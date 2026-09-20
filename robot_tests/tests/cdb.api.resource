*** Settings ***
Library   RequestsLibrary
Library   JSONLibrary
Library   Collections
Library   procedure_tools/utils/data.py

*** Variables ***
${TIMEZONE}   %{TIMEZONE}
${files_prefix}   ../procedure_tools/data

${cdb_api_host}   %{CDB_API_HOST}
${quintagroup_token}   %{QUINTAGROUP_TOKEN}
${chronograph_token}   %{CHRONOGRAPH_TOKEN}

${ds_upload_url}   %{DS_UPLOAD_URL}
${ds_user}   %{DS_USER}
${ds_pass}   %{DS_PASS}


*** Keywords ***

Створити тендер
    [Arguments]  ${file_name}   ${submissionMethodDetails}=quick(mode:fast-auction)  ${authorization}=${quintagroup_token}  ${expected_status}=201
    ${body}  Load Json From File   file_name=${files_prefix}/${file_name}
    Set Acceleration Data   ${body['data']}
    Set To Dictionary  ${body['data']}  mode   test
    Set To Dictionary  ${body['data']}  submissionMethodDetails   ${submissionMethodDetails}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    POST    url=${cdb_api_host}/tenders    json=${body}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()}
    Log  Створено тендер ${cdb_api_host}/tenders/${result['data']['id']}
    RETURN  ${result}


Отримати тендер
    [Arguments]  ${tender_id}  ${authorization}=${quintagroup_token}  ${expected_status}=200
    ${headers}  Create Dictionary  Authorization=Bearer ${authorization}
    ${response}    GET    url=${cdb_api_host}/tenders/${tender_id}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()['data']}
    RETURN  ${result}


Знайти ідентифікатор
    [Arguments]  ${data}
    RETURN  ${data['data']['id']}


Знайти токен доступу
    [Arguments]  ${data}
    ${authorization} =  Set Variable  ${data['access']['token']}
    RETURN  ${authorization}


Знайти статус тендера
    [Arguments]  ${data}
    ${authorization} =  Set Variable  ${data['data']['status']}
    RETURN  ${authorization}


Додати критерії до тендера
    [Documentation]  Додає обов'язкові criteria до тендера
    [Arguments]  ${file_name}  ${tender_id}   ${tender_token}  ${authorization}=${quintagroup_token}  ${expected_status}=201
    ${body}  Load Json From File   file_name=${files_prefix}/${file_name}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    POST    url=${cdb_api_host}/tenders/${tender_id}/criteria?acc_token=${tender_token}    json=${body}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()["data"]}
    RETURN  ${result}


Опублікувати тендер
    [Documentation]  Переводить тендер у наступний публічний статус
    [Arguments]  ${tender_id}   ${tender_token}  ${authorization}=${quintagroup_token}  ${expected_status}=200
    ${data}    Create Dictionary    status=active.tendering
    ${body}    Create Dictionary    data=${data}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    PATCH    url=${cdb_api_host}/tenders/${tender_id}?acc_token=${tender_token}    json=${body}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()}
    RETURN  ${result}


# Пропозиції / біди
Подати драфт тендерної пропозиції
    [Documentation]  Створює драфт bid в тендері
    [Arguments]  ${file_name}  ${tender_id}  ${authorization}=${quintagroup_token}  ${expected_status}=201
    ${body}  Load Json From File   file_name=${files_prefix}/${file_name}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    POST    url=${cdb_api_host}/tenders/${tender_id}/bids    json=${body}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()}
    RETURN  ${result}

Отримати тендерну пропозицію з апі
    [Documentation]  Прідвантажує документ в док сервіс і додає його до біда
    [Arguments]  ${tender_id}  ${bid_id}  ${bid_token}   ${authorization}=${quintagroup_token}  ${expected_status}=200
    ${headers}  Create Dictionary  Authorization=Bearer ${authorization}
    ${response}    GET    url=${cdb_api_host}/tenders/${tender_id}/bids/${bid_id}?acc_token=${bid_token}  headers=${headers}   expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()['data']}
    RETURN  ${result}

Опублікувати тендерну пропозицію
    [Documentation]  Переводить статус bid з draft в pending
    [Arguments]  ${tender_id}  ${bid_id}  ${bid_token}   ${authorization}=${quintagroup_token}  ${expected_status}=200
    ${data}    Create Dictionary    status=pending
    ${body}    Create Dictionary    data=${data}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    PATCH    url=${cdb_api_host}/tenders/${tender_id}/bids/${bid_id}?acc_token=${bid_token}  json=${body}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()}
    RETURN  ${result}


Завантажити документ на доксервіс
    [Documentation]  Прідвантажує документ в док сервіс і додає його до біда
    [Arguments]  ${file_name}   ${expected_status}=200
    ${files}    Create Dictionary    file=${file_name}
    ${auth}     Evaluate    ("${ds_user}", "${ds_pass}")
    ${response}   POST    url=${ds_upload_url}  auth=${auth}   files=${files}    expected_status=${expected_status}
    ${file_data}  Set Variable  ${response.json()['data']}
    RETURN  ${file_data}

Додати документ до тендерної пропозиції
    [Documentation]  Прідвантажує документ в док сервіс і додає його до біда
    [Arguments]  ${file_name}  ${tender_id}  ${bid_id}  ${bid_token}   ${authorization}=${quintagroup_token}  ${expected_status}=201
    ${file_data}  Завантажити документ на доксервіс   file_name=${file_name}

    ${body}    Create Dictionary    data=${file_data}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    POST    url=${cdb_api_host}/tenders/${tender_id}/bids/${bid_id}/documents?acc_token=${bid_token}  json=${body}   headers=${headers}   expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()['data']}
    RETURN  ${result}


Додати відповіді по критеріям
    [Documentation]  Публікує
    [Arguments]  ${file_name}   ${criteria_list}  ${tender_id}  ${bid_id}  ${bid_token}   ${authorization}=${quintagroup_token}  ${expected_status}=201
    ${body}  Load Json From File   file_name=${files_prefix}/${file_name}

    # проводим махінації над відповідями
    FOR    ${response}    IN    @{body['data']}
        # якщо евіденс це файл, то доведется його підвантажити
        IF  'evidences' in $response
            FOR    ${evidence}    IN    @{response['evidences']}
                IF  $evidence['type'] == 'document'
                    ${document}  Додати документ до тендерної пропозиції   file_name=aboveThreshold.multilot/tender_create.json  tender_id=${tender_id}  bid_id=${bid_id}  bid_token=${bid_token}
                    Set To Dictionary  ${evidence['relatedDocument']}  id   ${document['id']}
                END
            END
        END
        # копіюєм ід з крітеріїв у відповіді, коли співпадає title
        FOR    ${criteria}    IN    @{criteria_list}
            FOR    ${group}    IN    @{criteria['requirementGroups']}
                FOR    ${requirement}    IN    @{group['requirements']}
                    IF  $response['requirement']['title'] == $requirement['title']
                        Set To Dictionary  ${response['requirement']}   id   ${requirement['id']}
                    END
                END
            END
        END
    END

    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${authorization}
    ${response}    POST    url=${cdb_api_host}/tenders/${tender_id}/bids/${bid_id}/requirement_responses?acc_token=${bid_token}  json=${body}   headers=${headers}    expected_status=${expected_status}
    ${result}    Set Variable    ${response.json()}
    RETURN  ${result}


# Аукціони
Почекати посилання на аукціон
    [Documentation]  Чекає поки в тендері з'явиться посилання на аукціон. Якщо вказаний індес лоту, то для лота.
    [Arguments]  ${tender_id}   ${lot_index}=${None}
    FOR    ${index}    IN RANGE    100
        ${tender}  Отримати тендер  tender_id=${tender_id}

        IF  $lot_index is not None
            IF  'auctionUrl' in $tender['lots'][int($lot_index)]
                ${url}  Evaluate   $tender['lots'][int($lot_index)]['auctionUrl']
                RETURN  ${url}
            END
        ELSE
            IF  'auctionUrl' in $tender
                RETURN  ${tender['auctionUrl']}
            END
        END

        Sleep  5 seconds
    END


Прискорити дату початку аукціону
    [Documentation]  Змінює auctionPeriod.startDate
    [Arguments]  ${tender}
    ${tender_id}    Set Variable    ${tender['id']}
    ${start_date}   Evaluate  (datetime.datetime.now(pytz.timezone('Europe/Kiev')) + datetime.timedelta(seconds=30)).isoformat()    modules=datetime,pytz
    ${auction_period}   Create Dictionary  startDate=${start_date}
    IF  'lots' in $tender
        @{lots}    Create List
        FOR  ${lot}  IN   ${tender['lots']}
            ${lot_patch}  Create Dictionary  auctionPeriod=${auction_period}
            Append To List   ${lots}   ${lot_patch}
        END
        ${data}  Create Dictionary  lots=${lots}
    ELSE
        ${data}  Create Dictionary  auctionPeriod=${auction_period}
    END
    ${body}    Create Dictionary    data=${data}
    ${headers}  Create Dictionary  Content-Type=application/json   Authorization=Bearer ${chronograph_token}
    ${response}    PATCH   url=${cdb_api_host}/tenders/${tender_id}/chronograph  json=${body}   headers=${headers}
    ${result}    Set Variable    ${response.json()['data']}
    # треба почекати ресинхронізацію апі аукціонів з апі тендерів
    # але аукціон все одно не пропустим, бо там 5 хв пауза на початку
    Sleep  3 minutes
    RETURN  ${result}

