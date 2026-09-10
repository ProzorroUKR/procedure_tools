*** Settings ***
Library   Browser
Library   DateTime
Resource  cdb.api.resource
Resource  common.resource
Resource  auction.resource

*** Variables ***
${BROWSER}    chrome
${HEADLESS}   False

*** Test Cases ***
Понадпорогова процедура
    [Documentation]  Позитивний сценарій понадпорогової закупівлі
    [Tags]  auction   aboveThreshold    smoke

    ${result}  Створити тендер  file_name=aboveThreshold.multilot/tender_create.json
    Log  Відповідь від апі: ${result}

    ${tender_id}  Знайти ідентифікатор  ${result}
    ${tender_token}  Знайти токен доступу  ${result}
    ${tender_status}  Знайти статус тендера  ${result}
    ${tender}    Set Variable    ${result['data']}
    Log  Тендер ${tender_id} створено в статусі ${tender_status}, токен доступу ${tender_token}

    ${criteria_list}  Додати критерії до тендера  file_name=aboveThreshold.multilot/criteria_create.json    tender_id=${tender_id}   tender_token=${tender_token}

    ${result}  Опублікувати тендер   tender_id=${tender_id}   tender_token=${tender_token}
    ${tender_status}  Знайти статус тендера  ${result}
    Should Be Equal As Strings   active.tendering  ${tender_status}

    # перша пропозиція
    ${result}  Подати драфт тендерної пропозиції  file_name=aboveThreshold.multilot/bid_create_0.json  tender_id=${tender_id}
    ${bid_0_id}  Знайти ідентифікатор  ${result}
    ${bid_0_token}  Знайти токен доступу  ${result}
    Додати відповіді по критеріям  criteria_list=${criteria_list}  file_name=aboveThreshold.multilot/bid_res_post_0.json  tender_id=${tender_id}  bid_id=${bid_0_id}  bid_token=${bid_0_token}
    Опублікувати тендерну пропозицію  tender_id=${tender_id}  bid_id=${bid_0_id}  bid_token=${bid_0_token}

    # друга пропозиція
    ${result}  Подати драфт тендерної пропозиції  file_name=aboveThreshold.multilot/bid_create_1.json  tender_id=${tender_id}
    ${bid_1_id}  Знайти ідентифікатор  ${result}
    ${bid_1_token}  Знайти токен доступу  ${result}
    Додати відповіді по критеріям  criteria_list=${criteria_list}  file_name=aboveThreshold.multilot/bid_res_post_1.json  tender_id=${tender_id}  bid_id=${bid_1_id}  bid_token=${bid_1_token}
    Опублікувати тендерну пропозицію  tender_id=${tender_id}  bid_id=${bid_1_id}  bid_token=${bid_1_token}

    ${tender}  Отримати тендер  tender_id=${tender_id}
    Почекати настання дати   ${tender['tenderPeriod']['endDate']}
    Прискорити дату початку аукціону  tender=${tender}

    ${auction_url}  Почекати посилання на аукціон  tender_id=${tender_id}   lot_index=0
     # взяти інфу по аукціону з апі ауіцонів, щоб знати коли буде ставка учасника
    ${auction_info}  Отримати інформацію про аукціон   url=${auction_url}

    New Page  url=${auction_url}
    Sleep  2 seconds
    Take Screenshot


    ${bid_1}   Отримати тендерну пропозицію з апі  tender_id=${tender_id}  bid_id=${bid_1_id}  bid_token=${bid_1_token}
    Log   ${bid_1}
    ${participation_1_url}    Set Variable    ${bid_1['lotValues'][0]['participationUrl']}

    Go To  url=${participation_1_url}
    Sleep  2 seconds
    Take Screenshot

    Click  text="Так"
    Sleep  2 seconds
    Take Screenshot


    ${first_bid_1_stage}    Set Variable    ${auction_info['stages'][1]}
    Should Be Equal As Strings   bids   ${first_bid_1_stage['type']}
    Почекати настання дати   ${first_bid_1_stage['start']}

    Sleep  5 seconds
    Зробити ставку аукціона  amount=450


    Sleep  2 seconds
    Take Screenshot


Понадпорогова процедура без аукціону
    [Documentation]  Позитивний сценарій понадпорогової закупівлі
    [Tags]  no-auction   aboveThreshold    smoke

    ${result}  Створити тендер  file_name=aboveThreshold.multilot/tender_create.json   submissionMethodDetails=quick(mode:no-auction)
    Log  Відповідь від апі: ${result}

