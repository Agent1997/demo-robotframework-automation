*** Settings ***
Library             sauce_demo_ui.AppKeywords       headless=${False}
Suite Setup         Login To Sauce Demo App
Suite Teardown      Close Sauce Lab Demo App

*** Variables ***
${valid_username}                                 standard_user
${valid_password}                                 secret_sauce


*** Test Cases ***
Verify That Products Can Be Sorted By Name A to Z
    User Sorted The Products By Name A to Z
    Sleep    3s

Verify That Products Can Be Sorted By Name Z to A
    User Sorted The Products By Name Z to A
    Sleep    3s

Verify That Product Can Be Sorted By Price Low to High
    User Sorted The Products By Price Low To High
    Sleep    3s

Verify That Products Can Be Sorted By Price High to Low
    User Sorted The Products By Price High To Low
    Sleep    3s


*** Keywords ***
Login To Sauce Demo App
    Open Sauce Lab Demo App
    User Login To Sauce Lab Demo App    username=${valid_username}    password=${valid_password}
