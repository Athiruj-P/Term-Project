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
${progress_bar}     css:#root > div.content-wrapper > section.content > div > div > div > div.collapse > div > div > div
${precessing_status}    css:#root > div.content-wrapper > section.content > div > div > div > div.row.dflex.justify-content-center.mt-3.mb-2 > p

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

Click upload button
    Click Element   ${upload_btn}    

Progress bar must show up
    Wait Until Element Is Visible   ${progress_bar}     5

Processing status must show up
    Wait Until Element Is Visible   ${precessing_status}    5

Result must show up
    Wait Until Page Contains    Result image     5

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     30 

Wait "${sec}"
    Sleep   ${sec}
*** Test cases ***
# กดปุ่มอัปโหลดไฟล์รูปภาพเพื่อวัดขนาดวัตถุ
DPML-02-3-1
    [Documentation]     กดปุ่มอัปโหลดไฟล์รูปภาพเพื่อวัดขนาดวัตถุ
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/IMG_01.jpg"
    AND Select unit "2"
    AND Click upload button
    AND Progress bar must show up
    AND Processing status must show up
    THEN Wait "1"
    [Teardown]    Close Browser

# อัปโหลดไฟล์รูปภาพที่ตรงตามเงื่อนไขที่กำหนด
DPML-02-3-2
    [Documentation]     อัปโหลดไฟล์รูปภาพที่ตรงตามเงื่อนไขที่กำหนด
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/IMG_01.jpg"
    AND Select unit "2"
    AND Click upload button
    AND Progress bar must show up
    AND Processing status must show up
    AND The alert must say "Measure object size successfully"
    AND Result must show up
    THEN Wait "1"
    [Teardown]    Close Browser

# อัปโหลดไฟล์รูปภาพที่สนใจโดยไม่มีวัตถุที่ผ่านการเรียนรู้ของเครื่อง
DPML-02-3-3
    [Documentation]     อัปโหลดไฟล์รูปภาพที่สนใจโดยไม่มีวัตถุที่ผ่านการเรียนรู้ของเครื่อง
    [Tags]    Negative
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/Learning img/IMG_7953_resized.jpg"
    AND Select unit "2"
    AND Click upload button
    AND Progress bar must show up
    AND Processing status must show up
    AND The alert must say "Object not detected"
    AND Result must show up
    THEN Wait "1"
    [Teardown]    Close Browser

# อัปโหลดไฟล์รูปภาพที่สนใจโดยไม่มีวัตถุอ้างอิงติดอยู่บนวัตถุที่สนใจวัดขนาด
DPML-02-3-4
    [Documentation]     อัปโหลดไฟล์รูปภาพที่สนใจโดยไม่มีวัตถุอ้างอิงติดอยู่บนวัตถุที่สนใจวัดขนาด
    [Tags]    Negative
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/box_green_screen.jpg"
    AND Select unit "2"
    AND Click upload button
    AND Progress bar must show up
    AND Processing status must show up
    AND The alert must say "Reference object not detected"
    AND Result must show up
    THEN Wait "1"
    [Teardown]    Close Browser


