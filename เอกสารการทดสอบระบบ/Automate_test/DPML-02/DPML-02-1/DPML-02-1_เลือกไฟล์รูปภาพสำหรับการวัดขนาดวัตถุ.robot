*** Settings ***
Library     Selenium2Library
*** Variables ***
${dpml_url}     http://localhost

*** Keywords ***
open web
    Open Browser  ${dpml_url}     chrome

login "${username}" "${password}"
    Input Text  css:#root > div > div > div.card > div > div:nth-child(2) > input   ${username}
    Input Password  css:#root > div > div > div.card > div > div:nth-child(3) > input   ${password}
    Click Element   css:#root > div > div > div.card > div > div.row > div > button

Choose file "${path}"
    Choose File     css:#image_file     ${path}

Dropdown should be enabled
    Element Should Be Enabled   css:#root > div.content-wrapper > section.content > div > div > div > div.row.d-flex.justify-content-center.align-content-center > div.col-md-3 > select

The url must be "${text}"
    Wait Until Location Is    ${text}     5 

The alert must say "${text}"
    Wait Until Page Contains    ${text}     5 

Wait "${sec}"
    Sleep   ${sec}
*** Test cases ***
# เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.bpm" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
DPML-02-1-1
    [Documentation]     เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.bpm" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/all_extension/BMP.bmp"
    AND Dropdown should be enabled
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.jpg" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
DPML-02-1-2
    [Documentation]     เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.jpg" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/all_extension/JPG.jpg"
    AND Dropdown should be enabled
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.jpe" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
DPML-02-1-3
    [Documentation]     เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.jpe" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/all_extension/JPE.jpe"
    AND Dropdown should be enabled
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.png" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
DPML-02-1-4
    [Documentation]     เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ "*.png" และขนาดไฟล์รูปภาพน้อยกว่าเท่ากับ 10 MB
    [Tags]    Positive
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/all_extension/PNG.png"
    AND Dropdown should be enabled
    THEN Wait "1"
    [Teardown]    Close Browser

# เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ที่ไม่ถูกต้อง
DPML-02-1-5
    [Documentation]     เลือกไฟล์รูปภาพด้วยนามสกุลไฟล์ที่ไม่ถูกต้อง
    [Tags]    Negative
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/เอกสารปฏิบัติงานสหกิจศึกษา บทที่1.pdf"
    AND The alert must say "Wrong file extension, Please upload an new image."
    THEN Wait "1"
    [Teardown]    Close Browser

# ขนาดไฟล์รูปภาพมากกว่า 10 MB
DPML-02-1-6
    [Documentation]     ขนาดไฟล์รูปภาพมากกว่า 10 MB
    [Tags]    Negative
    GIVEN open web
    WHEN login "admin" "123123"
    AND The url must be "http://localhost/upload"
    AND Choose file "C:/Users/First-AP/Desktop/Homework/4th Year/CSI_project/Photo/DPML_test_img/large_file/SamplePNGImage_20mbmb.png"
    AND The alert must say "Image file size is more than 10MB."
    THEN Wait "1"
    [Teardown]    Close Browser
