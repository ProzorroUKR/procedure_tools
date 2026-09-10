*** Settings ***
Library   RequestsLibrary
Library   JSONLibrary
Library   Collections

*** Variables ***


*** Keywords ***
Почекати настання дати
    [Documentation]  Приймає строку в iso форматі і чекає настання вказаного дати/часу
    [Arguments]  ${timestamp}
    ${parsed_date}    Evaluate   datetime.datetime.fromisoformat($timestamp)   modules=datetime
    ${now}    Evaluate   datetime.datetime.now($parsed_date.tzinfo)    modules=datetime
    Log  ${parsed_date} - ${now}
    Log  ${parsed_date} - ${now}
    ${seconds}    Evaluate   ($parsed_date - datetime.datetime.now($parsed_date.tzinfo)).total_seconds()    modules=datetime
    IF  $seconds > 0
        Sleep  ${seconds}
    END