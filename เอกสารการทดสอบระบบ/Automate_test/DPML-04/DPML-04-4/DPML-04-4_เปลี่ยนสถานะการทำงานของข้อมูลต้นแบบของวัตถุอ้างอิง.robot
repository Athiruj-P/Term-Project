*** Settings ***
Library     Selenium2Library
*** Variables ***
${dpml_url}     http://localhost
${input_username}   css:#root > div > div > div.card > div > div:nth-child(2) > input
${input_password}   css:#root > div > div > div.card > div > div:nth-child(3) > input
${login_btn}    css:#root > div > div > div.card > div > div.row > div > button
${open_switch_modal}    css:#DataTables_Table_0 > tbody > tr:nth-child(2) > td:nth-child(6) > label
${switch_model_btn}    css:body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled
${open_switch_modal_active}     css:#DataTables_Table_0 > tbody > tr:nth-child(1) > td:nth-child(6) > label > div

** Keywords ***
open web
    Open Browser  ${dpml_url}     chrome

login "${username}" "${password}"
    Input Text  ${input_username}   ${username}
    Input Password  ${input_password}   ${password}
    Click Element   ${login_btn}

Select menu
    Selenium2Library.Execute Javascript     window.location.replace("/ref_management")

Open modal 
    Click Element   ${open_switch_modal}

Click switch button
    Click Element   ${switch_model_btn}    

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     30 

The error message must say "${text}"
    Wait Until Page Contains    ${text}     5

Element should have class "${className}"
    Wait until page contains element  ${open_switch_modal_active}.${className}

Wait "${sec}"
    Sleep   ${sec}

*** Test cases ***
# เปิดการทำงานของข้อมูลต้นแบบของวัตถุ
DPML-03-4-1
    [Documentation]     เปิดการทำงานของข้อมูลต้นแบบของวัตถุอ้างอิง
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"
    AND Click switch button
    AND Wait "1"
    AND The alert must say "Change active model successfully."
    THEN Wait "1"
    [Teardown]    Close Browser

# ปิดการทำงานของข้อมูลต้นแบบของวัตถุที่มีสถานะเปิดใช้งาน
DPML-03-4-2
    [Documentation]     ปิดการทำงานของข้อมูลต้นแบบของวัตถุที่มีสถานะเปิดใช้งาน
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Element should have class "no-drop" 
    THEN Wait "1"
    [Teardown]    Close Browser
