*** Settings ***
Library           Selenium2Library
*** Keywords ***
เปิดเว็บ Google
    Open Browser        https://www.google.com      chrome
ฉันต้องการค้นหา "${value}"
    Input Text          //*[@name="q"]              ${value}
กดปุ่มค้นหา
    Submit Form         //form[@name='f']
ต้องแสดงผลลัพธ์ "${value}"
    Title Should Be     ${value} - ค้นหาด้วย Google
*** Test cases ***
Test case 1
    Given เปิดเว็บ Google
    When ฉันต้องการค้นหา "Testing"
    AND กดปุ่มค้นหา
    Then ต้องแสดงผลลัพธ์ "Testing"