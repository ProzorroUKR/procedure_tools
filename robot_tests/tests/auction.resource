*** Settings ***
Library   RequestsLibrary
Library   Browser

*** Variables ***


*** Keywords ***
Отримати інформацію про аукціон
    [Documentation]  Приймає url аукіона і повертає апі дані про нього
    [Arguments]  ${url}
    ${api_url}    Evaluate   $url.replace('tenders', 'api/auctions')
    ${response}    GET   url=${api_url}
    ${result}    Set Variable    ${response.json()}
    RETURN  ${result}


Зробити ставку аукціона
    [Documentation]  Робить ставку під час раунда ставок аукціона
    [Arguments]  ${amount}
    Type Text  input[id=bid-amount-input]  ${amount}
    Click   button[id=place-bid-button]
