*** Settings ***
Library           Selenium2Library
*** Variables ***
${date}             dom=$("body > div > div > form > div:nth-child(8) > input")
*** Keywords ***
open web
    Open Browser  http://dekdee.buu.ac.th/exam_testing/     chrome

select age
    Selenium2Library.Execute Javascript     $("body > div > div > form > select").val(1)

input firstname and lastname "${fname}" "${lname}"
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(4) > input").val("${fname}")    
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(5) > input").val("${lname}")    

input phonenum mail and birthday "${phone}" "${mail}" "${bd}"  
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(6) > input").val("${phone}")    
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(7) > input").val("${mail}")    
    # Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(8) > input").val("${bd}")
    Input Text  ${date}     ${bd}
    # Press Key       dom=$("body > div > div > form > div:nth-child(8) > input")      \\13    
    # Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(10) > input").click()
    Click Element   dom=$("body > div > div > form > div:nth-child(10) > input")

    
input username passwaord "${user}" "${pass}"
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(10) > input").val("${user}")    
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(11) > input").val("${pass}")    
    Selenium2Library.Execute Javascript  $("#comf_pass").val("${pass}") 

input username passwaord confirm "${user}" "${pass}" ${conpass}"
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(10) > input").val("${user}")    
    Selenium2Library.Execute Javascript  $("body > div > div > form > div:nth-child(11) > input").val("${pass}")    
    Selenium2Library.Execute Javascript  $("#comf_pass").val("${conpass}")

check radio email
    Selenium2Library.Execute Javascript     $("#exampleRadios1").prop("checked", true);

check radio notify
    Selenium2Library.Execute Javascript     $("#exampleRadios2").prop("checked", true);

check checkbox accept
    Selenium2Library.Execute Javascript     $("#exampleCheck1").prop("checked", true);

check checkbox email
    Selenium2Library.Execute Javascript     $("#exampleCheck2").prop("checked", true);

I want to click register 
     Selenium2Library.Execute Javascript    $("body > div > div > form > button").click()
    
I should see
    Title Should Be     "Result"
*** Test cases ***
# Test case 1
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE08" "SE#07Athiruj01"
#     AND check radio email
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see

# Test case 2
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE08" "SE#07Athiruj01"
#     AND check radio notify
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see


# Test case 3
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE" "SE#07Athiruj01"
#     AND check radio email
#     AND check checkbox accept
#     # AND check checkbox email
#     AND I want to click register
#     THEN I should see


# Test case 4
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE" "SE#07Athiruj01"
#     AND check radio email
#     # AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see


# Test case 5
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "ภูษิตาภรณ์"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE" "SE#07Athiruj01"
#     AND check radio email
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see


# Test case 6
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0855" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE" "SE#07Athiruj01"
#     AND check radio email
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see


# Test case 7
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     AND input username passwaord "UpToYouSE" "SE#07"
#     AND check radio email
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see


# Test case 8
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/1998" 
#     # AND input username passwaord "@@@@@eiei+-*/" "SE#07"
#     AND input username passwaord confirm "UpToYouSE" "SE#07Athiruj01" 5845"
#     AND check radio email
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see

# Test case 9
#     Given open web
#     When select age
#     AND input firstname and lastname "Athiruj" "Poositaporn"
#     AND input phonenum mail and birthday "0850769454" "601160116@go.buu.ac.th" "12/11/2541" 
#     AND input username passwaord "@UpToYouSE" "SE#07Athiruj01"
#     AND check radio notify
#     AND check checkbox accept
#     AND check checkbox email
#     AND I want to click register
#     THEN I should see

Test case 10
    Given open web
    When check checkbox accept
    AND check radio notify
    AND I want to click register
    THEN I should see