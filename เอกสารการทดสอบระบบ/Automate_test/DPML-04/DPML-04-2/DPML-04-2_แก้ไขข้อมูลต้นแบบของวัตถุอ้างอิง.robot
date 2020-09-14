*** Settings ***
Library     Selenium2Library
*** Variables ***
${dpml_url}     http://localhost
${input_username}   css:#root > div > div > div.card > div > div:nth-child(2) > input
${input_password}   css:#root > div > div > div.card > div > div:nth-child(3) > input
${login_btn}    css:#root > div > div > div.card > div > div.row > div > button
${open_edit_modal}    css:#DataTables_Table_0 > tbody > tr:nth-child(2) > td.d-flex.justify-content-center > div > button.btn.btn-warning.btn-sm.mr-2

${input_model_name}     css:#model_name
${input_model_width}     css:#width
${input_model_height}     css:#height
${dropdown}     css:#unit
${input_weight}    css:#file

${edit_model_btn}    css:body > div.fade.fade.modal.show > div > div > div.d-flex.justify-content-between.modal-footer > button.btn.btn-warning
${progress_bar}     css:#root > div.content-wrapper.h-100 > section.content > div > div > div > div > div:nth-child(1) > div > div > div

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
    Click Element   ${open_edit_modal}

Insert model name "${name}"
    Input Text  ${input_model_name}   ${name}

Insert model width "${width}"
    Input Text  ${input_model_width}   ${width}

Insert model height "${height}"
    Input Text  ${input_model_height}   ${height}

Select unit "${value}"
    Select From List By Value   ${dropdown}   ${value}

Choose file "${path}"
    Choose File     ${input_weight}     ${path}

Upload should be disabled
    Element Should Be Disabled   ${edit_model_btn}

Click edit button
    Click Element   ${edit_model_btn}    

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
# กรอกชื่อข้อมูลต้นแบบของวัตถุอ้างอิงและเลือกไฟล์ข้อมูลต้นแบบของวัตถุอ้างอิงโดยนามสกุลไฟล์ถูกต้อง
DPML-04-2-1
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model name "robot_ref_1_edit"
    AND Insert model width "30"
    AND Insert model height "30"
    AND Select unit "2"
    AND Choose file "C:/Users/First-AP/Desktop/fake_model.weights"

    AND Click edit button
    AND Progress bar must show up
    AND The alert must say "Edited a model data successfully."
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกชื่อข้อมูลต้นแบบของวัตถุอ้างอิงถูกต้อง
DPML-04-2-2
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model name "robot_rename"
    AND Click edit button
    AND The alert must say "Edited a model data successfully."
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกไฟล์ข้อมูลต้นแบบของวัตถุอ้างอิงโดยนามสกุลไฟล์ถูกต้อง
DPML-04-2-3
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Choose file "C:/Users/First-AP/Desktop/fake_model.weights"
    AND Click edit button
    AND Progress bar must show up
    AND The alert must say "Edited a model data successfully."
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกขนาดความกว้างถูกต้อง
DPML-04-2-4
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model height "35"
    AND Click edit button
    AND The alert must say "Edited a model data successfully."
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกขนาดความยาวถูกต้อง 
DPML-04-2-5
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model width "35"
    AND Click edit button
    AND The alert must say "Edited a model data successfully."
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกหน่วยของขนาดวัตถุอ้างอิงถูกต้อง
DPML-04-2-6
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model width ""
    AND Upload should be disabled
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกชื่อข้อมูลต้นแบบของวัตถุอ้างอิงน้อยกว่า 3 ตัวอักษร
DPML-04-2-7
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model name "qw"
    AND The error message must say "Model name must contain minimum 3 characters and maximum 30 characters."
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกชื่อข้อมูลต้นแบบของวัตถุอ้างอิงไม่ถูกต้อง
DPML-04-2-8
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model name "qw$#@"
    AND The error message must say "Model name must be English, Thai, number, a space ( ) and underscore (_) are allow."
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกขนาดความกว้างน้อยกว่าหรือเท่ากับ 0
DPML-04-2-9
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model width "-1"
    AND The error message must say "Width must greater than 0."
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกขนาดความยาวน้อยกว่าหรือเท่ากับ 0
DPML-04-2-10
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Insert model height "-1"
    AND The error message must say "Height must greater than 0."
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกไฟล์ข้อมูลต้นแบบของวัตถุอ้างอิงโดยนามสกุลไฟล์ไม่ถูกต้อง
DPML-04-2-11
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND select menu
    AND The url must be "http://localhost/ref_management"
    AND Wait "1"
    AND Open modal 
    AND Wait "1"

    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/box_green_screen.jpg"
    AND The error message must say "File extension must be *.weights"
    THEN Wait "1"
    [Teardown]    Close Browser