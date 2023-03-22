*** Settings ***
Library         sauce_demo_ui.AppKeywords     headless=${False}
Test Setup      Open Sauce Lab Demo App
Test Teardown   Close Sauce Lab Demo App

*** Variables ***
${invalid_username_and_password_err_msg}          Epic sadface: Username and password do not match any user in this service
${locked_out_user_err_msg}                        Epic sadface: Sorry, this user has been locked out.
${username_required_err_msg}                      Epic sadface: Username is required
${password_required_err_msg}                      Epic sadface: Password is required
${valid_username}                                 standard_user
${valid_password}                                 secret_sauce

*** Test Cases ***
Verify That User Cannot Login With Invalid Username And Password
    [Template]              Verify Login Using Invalid Credentials
    ${valid_username}       invalid_password      ${invalid_username_and_password_err_msg}
    invalid_username        ${valid_password}     ${invalid_username_and_password_err_msg}
    invalid_username        invalid_password      ${invalid_username_and_password_err_msg}
    locked_out_user         ${valid_password}     ${locked_out_user_err_msg}
    ${EMPTY}                ${EMPTY}              ${username_required_err_msg}
    standard_user           ${EMPTY}              ${password_required_err_msg}
    ${EMPTY}                ${valid_password}     ${username_required_err_msg}

Verify That User With Valid Username And Password Can Successfully Login
    User Login To Sauce Lab Demo App    username=${valid_username}        password=${valid_password}
    User Should Be In The Product Page Upon Successful Login


Verify That User Can Logout From Sauce Lab Demo App
    User Login To Sauce Lab Demo App    username=${valid_username}        password=${valid_password}
    User Should Be In The Product Page Upon Successful Login
    User Logout From Sauce Lab Demo App
    User Should Be In The Login Page Upon Successful Logout

*** Keywords ***
Verify Login Using Invalid Credentials
    [Arguments]     ${username}         ${password}         ${exp_err_msg}
    User Login To Sauce Lab Demo App    username=${username}        password=${password}
    User Should Not Be Able To Login
    Login Error Message Should Be    exp_err_msg=${exp_err_msg}
    [Teardown]      Reload Sauce Demo App

