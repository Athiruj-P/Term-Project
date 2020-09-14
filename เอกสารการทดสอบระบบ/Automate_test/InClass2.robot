*** Settings ***
Library           Selenium2Library
*** Keywords ***
open dekdee
    Open Browser        http://dekdee.buu.ac.th/testing/      chrome

I want to input username and password "${username}" "${password}"
    Input Text          //*[@id="username_field"]             ${username}
    Input Text          //*[@id="password_field"]             ${password}

I click button
    Click Element         //*[@id="login_button"]

I should see result "${value}"
    Title Should Be     ${value}   
*** Test cases ***
Test case 1
    Given open dekdee
    When I want to input username and password "demo" "mode"
    AND I click button
    Then I should see result "Welcome Page"
Test case 2
    Given open dekdee
    When I want to input username and password "demo" "mod"
    AND I click button
    Then I should see result "Error Page"
Test case 3
    Given open dekdee
    When I want to input username and password "emo" "mode"
    AND I click button
    Then I should see result "Error Page"
Test case 4
    Given open dekdee
    When I want to input username and password "demo" ""
    AND I click button
    Then I should see result "Error Page"
Test case 5
    Given open dekdee
    When I want to input username and password "" "mode"
    AND I click button
    Then I should see result "Error Page"