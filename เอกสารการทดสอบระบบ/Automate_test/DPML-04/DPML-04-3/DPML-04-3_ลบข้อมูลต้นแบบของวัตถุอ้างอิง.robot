*** Settings ***
Library     Selenium2Library
*** Variables ***
${dpml_url}     http://localhost
${input_username}   css:#root > div > div > div.card > div > div:nth-child(2) > input
${input_password}   css:#root > div > div > div.card > div > div:nth-child(3) > input
${login_btn}    css:#root > div > div > div.card > div > div.row > div > button
${open_delete_modal}    css:#DataTables_Table_0 > tbody > tr:nth-child(2) > td.d-flex.justify-content-center > div > button.btn.btn-danger.btn-sm
${delete_model_btn}    css:body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled

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
    Click Element   ${open_delete_modal}

Click delete button
    Click Element   ${delete_model_btn}    

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     30 

Wait "${sec}"
    Sleep   ${sec}
*** Test cases ***
# กรอกชื่อข้อมูลต้นแบบของวัตถุอ้างอิงและเลือกไฟล์ข้อมูลต้นแบบของวัตถุอ้างอิงโดยนามสกุลไฟล์ถูกต้อง
DPML-04-3-1
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"
    AND Click delete button
    AND Wait "1"
    AND The alert must say "The model has been deleted."
    AND Click delete button
    THEN Wait "1"
    [Teardown]    Close Browser
