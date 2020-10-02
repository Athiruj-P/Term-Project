*** Settings ***
Library           Selenium2Library
*** Variables ***
${dpml_url}     http://localhost

*** Keywords ***
open web
    Open Browser  ${dpml_url}     chrome

input username and password "${username}" "${password}"
    # Selenium2Library.Execute Javascript  $("#root > div > div > div.card > div > div:nth-child(2) > input").val()    
    # Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(5) > input").val("${lname}")
    Input Text  css:#root > div > div > div.card > div > div:nth-child(2) > input   ${username}
    Input Password  css:#root > div > div > div.card > div > div:nth-child(3) > input   ${password}

Click login button
    Click Element   css:#root > div > div > div.card > div > div.row > div > button

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     5 

Wait "${sec}"
    Sleep   ${sec}
*** Test cases ***
# กรอกข้อมูลชื่อผู้ใช้งานและรหัสผ่านถูกต้อง
DPML-01-1-1
    [Documentation]     กรอกข้อมูลชื่อผู้ใช้งานและรหัสผ่านถูกต้อง
    [Tags]    Positive
    GIVEN open web
    WHEN input username and password "admin" "123123"
    AND Click login button
    AND The url must be "http://localhost/upload"
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกข้อมูลชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง
DPML-01-1-2
    [Documentation]     กรอกข้อมูลชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง
    [Tags]    Negative
    GIVEN open web
    WHEN input username and password "admin" "qweasd"
    AND Click login button
    AND The alert must say "Wrong username or password."
    THEN Wait "1"
    [Teardown]    Close Browser

# ไม่กรอกข้อมูลชื่อผู้ใช้งานและกรอกรหัสผ่าน
DPML-01-1-3 
    [Documentation]     ไม่กรอกข้อมูลชื่อผู้ใช้งานและกรอกรหัสผ่าน
    [Tags]    Negative
    GIVEN open web
    WHEN input username and password "" "123123"
    AND Click login button
    AND The alert must say "Blank username or password"
    THEN Wait "1"
    [Teardown]    Close Browser

# กรอกข้อมูลชื่อผู้ใช้งานและไม่กรอกรหัสผ่าน
DPML-01-1-4
    [Documentation]     กรอกข้อมูลชื่อผู้ใช้งานและไม่กรอกรหัสผ่าน
    [Tags]    Negative
    GIVEN open web
    WHEN input username and password "admin" ""
    AND Click login button
    AND The alert must say "Blank username or password"
    THEN Wait "1"
    [Teardown]    Close Browser

# ไม่กรอกข้อมูลชื่อผู้ใช้งานและไม่กรอกรหัสผ่าน
DPML-01-1-5
    [Documentation]     ไม่กรอกข้อมูลชื่อผู้ใช้งานและไม่กรอกรหัสผ่าน
    [Tags]    Negative
    GIVEN open web
    WHEN input username and password "" ""
    AND Click login button
    AND The alert must say "Blank username or password"
    THEN Wait "1"
    [Teardown]    Close Browser