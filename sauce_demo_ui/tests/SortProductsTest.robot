*** Settings ***
Library             sauce_demo_ui.AppKeywords       headless=${True}
Suite Setup         Login To Sauce Demo App
Suite Teardown      Close Sauce Lab Demo App

*** Variables ***
${valid_username}                                 standard_user
${valid_password}                                 secret_sauce


*** Test Cases ***
Verify That Products Can Be Sorted By Name A to Z
    User Sorted The Products By Name A to Z
    User Should See That Products Are Sorted By Name A to Z

Verify That Products Can Be Sorted By Name Z to A
    User Sorted The Products By Name Z to A
    User Should See That Products Are Sorted By Name Z to A

Verify That Product Can Be Sorted By Price Low to High
    User Sorted The Products By Price Low To High
    User Should See That Products Are Sorted By Price Low To High

Verify That Products Can Be Sorted By Price High to Low
    User Sorted The Products By Price High To Low
    User Should See That Products Are Sorted By Price High To Low


*** Keywords ***
Login To Sauce Demo App
    Open Sauce Lab Demo App
    User Login To Sauce Lab Demo App    username=${valid_username}    password=${valid_password}
