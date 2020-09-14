*** Settings ***
Library     Selenium2Library
*** Variables ***
${dpml_url}     http://localhost
${input_username}   css:#root > div > div > div.card > div > div:nth-child(2) > input
${input_password}   css:#root > div > div > div.card > div > div:nth-child(3) > input
${login_btn}    css:#root > div > div > div.card > div > div.row > div > button
${input_img}    css:#image_file
${upload_btn}   css:#root > div.content-wrapper > section.content > div > div > div > div:nth-child(5) > button
${dropdown}     css:#root > div.content-wrapper > section.content > div > div > div > div.row.d-flex.justify-content-center.align-content-center > div.col-md-3 > select
** Keywords ***
open web
    Open Browser  ${dpml_url}     chrome

login "${username}" "${password}"
    Input Text  ${input_username}   ${username}
    Input Password  ${input_password}   ${password}
    Click Element   ${login_btn}

Choose file "${path}"
    Choose File     ${input_img}     ${path}

Select unit "${value}"
    Wait Until Element Is Enabled   ${dropdown}
    Select From List By Value   ${dropdown}   ${value}

Upload should be "${opt}"
    Run Keyword If  '${opt}' == 'enable'  Element Should Be Enabled   ${upload_btn}
    Run Keyword Unless  '${opt}' == 'enable'  Element Should Be Disabled   ${upload_btn}

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     5 

Wait "${sec}"
    Sleep   ${sec}
*** Test cases ***
# เลือกหน่วยการวัดขนาดวัตถุ
DPML-02-2-1
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/IMG_01.jpg"
    AND Select unit "2"
    AND Upload should be "enable"
    THEN Wait "1"
    [Teardown]    Close Browser

# ไม่เลือกหน่วยการวัดขนาดวัตถุ
DPML-02-2-2
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/IMG_01.jpg"
    AND Select unit "0"
    AND Upload should be "disenabled"
    THEN Wait "1"
    [Teardown]    Close Browser

