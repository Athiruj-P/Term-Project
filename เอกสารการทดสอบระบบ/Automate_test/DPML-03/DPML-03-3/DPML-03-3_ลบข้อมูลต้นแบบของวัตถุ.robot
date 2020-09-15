*** Settings ***
Library     Selenium2Library
*** Variables ***
${dpml_url}     http://localhost
${input_username}   css:#root > div > div > div.card > div > div:nth-child(2) > input
${input_password}   css:#root > div > div > div.card > div > div:nth-child(3) > input
${login_btn}    css:#root > div > div > div.card > div > div.row > div > button
${open_delete_modal}    css:#DataTables_Table_0 > tbody > tr.even > td.d-flex.justify-content-center > div > button.btn.btn-danger.btn-sm
${input_weight}    css:#input_model_file
${input_model_name}     css:#model_name
${delete_model_btn}    css:body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled
${delete_close_btn}    css:body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled
${progress_bar}     css:#root > div.content-wrapper.h-100 > section.content > div > div > div > div > div:nth-child(1) > div > div > div
${open_delete_modal_active}     css:#DataTables_Table_0 > tbody > tr.odd > td.d-flex.justify-content-center > div > button.btn.btn-danger.btn-sm

** Keywords ***
open web
    Open Browser  ${dpml_url}     chrome

login "${username}" "${password}"
    Input Text  ${input_username}   ${username}
    Input Password  ${input_password}   ${password}
    Click Element   ${login_btn}

Select menu
    Selenium2Library.Execute Javascript     window.location.replace("/ml_management")

Open modal 
    Click Element   ${open_delete_modal}

Open modal button should be disabled
    Element Should Be Disabled   ${open_delete_modal_active}

Insert model name "${name}"
    Input Text  ${input_model_name}   ${name}

Choose file "${path}"
    Choose File     ${input_weight}     ${path}

Select unit "${value}"
    Wait Until Element Is Enabled   ${dropdown}
    Select From List By Value   ${dropdown}   ${value}

Upload should be disabled
    Element Should Be Disabled   ${delete_model_btn}

Click delete button
    Click Element   ${delete_model_btn}    

Progress bar must show up
    Wait Until Element Is Visible   ${progress_bar}     5

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     30 

The error message must say "${text}"
    Wait Until Page Contains    ${text}     5

Wait "${sec}"
    Sleep   ${sec}

*** Test cases ***
# กดปุ่มลบข้อมูลต้นแบบของวัตถุที่มีสถานะปิดใช้งาน
DPML-03-3-1
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ml_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"
    AND Click delete button
    AND Wait "1"
    AND The alert must say "The model has been deleted."
    AND Click delete button
    THEN Wait "1"
    [Teardown]    Close Browser

# กดปุ่มลบข้อมูลต้นแบบของวัตถุที่มีสถานะเปิดใช้งาน
DPML-03-3-2
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ml_management"
    AND Wait "1"
    AND Open modal button should be disabled
    AND Wait "1"
    [Teardown]    Close Browser
