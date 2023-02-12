# Project Description

Backend API for flutter application. It comprises of different features. Some of which are;
* User Authentication -> (Registration, Login, etc)
* Ecommerce
* Chat -> It has a chat application built into it to allow users communicate with the tailors

The project is devided into various django apps. This is to ensure simplicity and easy debugging since it will be a very lenghty API. Below are a description of all the various apps

[auth_api](https://github.com/codewitgabi/tailor_api/tree/main/auth_api)
* This app holds all endpoint related to user authentication and user listing generally. available endpoints included in this app are;

* __user_list__
Endpoint ```/auth/api/users/list/```
This endpoint returns all the available users (both customers and tailors) excluding superusers and staffs.
* __user_detail__
Endpoint ```/auth/api/users/detail/<user_unique_identifier>```
Returns the detail related to the user having the unique identifier.
* __user_registration__
Endpoint ```/auth/api/register/```
Endpoint for user registration
* __verify-otp__
Endpoint ```/auth/api/register/verify-otp/<int:otp>/```
Verifies OTP sent on user registration
* __resend-otp__
Endpoint ```/auth/api/register/resend-otp/```
Re-sends an otp to the user on expired otp
* __login__
Endpoint ```/auth/api/login/```
Returns two tokens to be used for user authentication and login. The access token is passed in the headers as Bearer or JWT authorization.
* __refresh-login-token__
Endpoint ```/auth/api/login/token/refresh/```
In a case where the user's access token has expired, this endpoint will refresh the user's token and generate a new one for the user
* __logout__
Endpoint ```/auth/api/logout/```
Logs a user out of a system by blacklisting their refresh token.
* __change-password__
Endpoint ```/auth/api/change-password/```
Changes a user password and then log them out of previously logged in devices
* __password-reset__
Endpoint ```/auth/api/password-reset/```
In a case where a user has forgotten their password, this endpoint will send an email to the user with a code to use for verification that the given account is theirs. After that, their password can now be changed.

