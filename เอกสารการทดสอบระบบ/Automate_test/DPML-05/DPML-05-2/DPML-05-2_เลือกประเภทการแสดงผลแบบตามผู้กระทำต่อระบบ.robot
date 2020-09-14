*** Settings ***
Library           Selenium2Library
*** Variables ***
${dpml_url}     http://localhost
${input_username}   css:#root > div > div > div.card > div > div:nth-child(2) > input
${input_password}   css:#root > div > div > div.card > div > div:nth-child(3) > input
${login_btn}    css:#root > div > div > div.card > div > div.row > div > button
${today_radio}  css:#root > div.content-wrapper.h-100 > section.content > div > div.card.card-primary > div.card-body.pb-0 > form > div > div:nth-child(1) > div > div > div:nth-child(1) > label
${datetime_radio}   css:#root > div.content-wrapper.h-100 > section.content > div > div.card.card-primary > div.card-body.pb-0 > form > div > div:nth-child(1) > div > div > div:nth-child(2) > label

${all_radio}    css:#root > div.content-wrapper.h-100 > section.content > div > div.card.card-primary > div.card-body.pb-0 > form > div > div:nth-child(2) > div > div > div:nth-child(1) > label
${user_radio}   css:#root > div.content-wrapper.h-100 > section.content > div > div.card.card-primary > div.card-body.pb-0 > form > div > div:nth-child(2) > div > div > div:nth-child(2) > label
${system_radio}     css:#root > div.content-wrapper.h-100 > section.content > div > div.card.card-primary > div.card-body.pb-0 > form > div > div:nth-child(2) > div > div > div:nth-child(3) > label

*** Keywords ***
open web
    Open Browser  ${dpml_url}     chrome

login "${username}" "${password}"
    Input Text  ${input_username}   ${username}
    Input Password  ${input_password}   ${password}
    Click Element   ${login_btn}

Select menu
    Selenium2Library.Execute Javascript     window.location.replace("/log")

Click radio date "${opt}"
    Run Keyword If      '${opt}' == 'today'     Click Element   ${today_radio}
    ...     ELSE    Click Element   ${datetime_radio}

Click radio type "${opt}"
    Run Keyword If      '${opt}' == 'all'     Click Element   ${all_radio}
    Run Keyword If      '${opt}' == 'user'     Click Element   ${user_radio}
    Run Keyword If      '${opt}' == 'system'     Click Element   ${system_radio}

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     5 

Wait "${sec}"
    Sleep   ${sec}

*** Test cases ***
# เลือกประเภทการแสดงผลแบบผู้กระทำต่อระบบทั้งหมด
DPML-05-2-1
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Select menu
    AND The url must be "http://localhost/log"
    AND Wait "1"
    AND Click radio type "all"
    THEN The alert must say "Get logs successfully."
    AND Wait "1"
    [Teardown]    Close Browser

# เลือกประเภทการแสดงผลแบบเฉพาะการกระทำของระบบ
DPML-05-2-2
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Select menu
    AND The url must be "http://localhost/log"
    AND Wait "1"
    AND Click radio type "system"
    THEN The alert must say "Get logs successfully."
    AND Wait "1"
    [Teardown]    Close Browser

# เลือกประเภทการแสดงผลแบบเฉพาะการกระทำของผู้ใช้งาน
DPML-05-2-3
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Select menu
    AND The url must be "http://localhost/log"
    AND Wait "1"
    AND Click radio type "user"
    THEN The alert must say "Get logs successfully."
    AND Wait "1"
    [Teardown]    Close Browser