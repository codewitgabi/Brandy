# Project Documentation

Backend API for flutter application. It comprises of different features. Some of which are;
* User Authentication -> (Registration, Login, etc)
* Ecommerce
* Chat -> It has a chat application built into it to allow users communicate with the tailors

The project is divided into various django apps. This is to ensure simplicity and easy debugging since it will be a very lenghty API. Below are a description of all the various apps

[auth_api](https://github.com/codewitgabi/tailor_api/tree/main/auth_api)\
This app holds all endpoint related to user authentication and user listing generally. available endpoints included in this app are;

* __user_list__\
```GET /auth/api/users/list/```\
This endpoint returns all the available users (both customers and tailors) excluding superusers and staffs.
* __user_detail__\
```GET /auth/api/users/detail/<user_id>```\
Returns the detail related to the user having the unique identifier.
* __user_registration__\
```POST /auth/api/register/```\
Endpoint for user registration
* __verify-otp__\
```GET /auth/api/register/verify-otp/<otp>/```\
Verifies OTP sent on user registration
* __resend-otp__\
```POST /auth/api/register/resend-otp/```\
Re-sends an otp to the user on expired otp
* __login__\
```POST /auth/api/login/```\
Returns two tokens to be used for user authentication and login. The access token is passed in the headers as Bearer or JWT authorization.
* __refresh-login-token__\
```POST /auth/api/login/token/refresh/```\
In a case where the user's access token has expired, this endpoint will refresh the user's token and generate a new one for the user
* __logout__\
```POST /auth/api/logout/```\
Logs a user out of a system by blacklisting their refresh token. The user's refresh token should be passed as body of the request.
* __change-password__\
```POST /auth/api/change-password/```\
Changes a user password and then log them out of previously logged in devices
* __password-reset__\
```POST /auth/api/password-reset/```\
In a case where a user has forgotten their password, this endpoint will send an email to the user with a code to use for verification that the given account is theirs. After that, their password can now be changed.

[tailor_api](https://github.com/codewitgabi/tailor_api/tree/main/tailor_api)\
This app holds endpoints related to tailors; their rating and personal description. Endpoints always begin with `/tailor/api`.Available endpoints are;

* __tailors-list__\
```GET /tailor/api/list```\
Returns a list of all available tailors and a full description regarding their rating, average amongst others.
* __tailor-creation__\
```POST /tailor/api/create/```\
Creates a new instance of a tailor. Returns a `500` error if it already exists.
* __rating__\
```POST /tailor/api/rating/```\
Creates a new rating for a tailor if it doesn't exist.
* __rating-update-via-Rating__\
```PUT /tailor/api/rating/update/<rating_id>/```\
Updates an existing rating for a particular tailor where the `rating_id` is readily available.
* __rating-update-via-Tailor__\
```PUT /tailor/api/rating/update/<tailor_id>/tailor/```\
Updates an existimg tailor rating where the `tailor_id` is readily available. This would be used in most cases.

