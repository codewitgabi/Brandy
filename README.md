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
```GET /auth/api/user/detail/<user_id>```\
Returns the detail related to the user having the unique identifier.
* __user-update__\
```PUT PATCH /auth/api/user/update/<user_id>/```\
Update the user with the given id. Use `PATCH` for updating a single field. `PUT` request method requires you to update the `username` and `email`.
* __user_registration__\
```POST /auth/api/register/```\
Endpoint for user registration
* __verify-otp__\
```GET /auth/api/register/verify-otp/<otp>/```\
Verifies OTP sent on user registration
* __resend-otp__\
```PUT/PATCH /auth/api/register/resend-otp/```\
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
* __follow-user__\
```POST /auth/api/follow/```\
Follows the user with the id passed in the request body. Returns the followed user on success.
* __unfollow-user__\
```POST /auth/api/unfollow/```\
Unfollows the user with the id passed in the request body. Returns the followed user on success.


[tailor_api](https://github.com/codewitgabi/tailor_api/tree/main/tailor_api)\
This app holds endpoints related to tailors; their rating and personal description. Endpoints always begin with `/tailor/api`.Available endpoints are;

* __tailors-list__\
```GET /tailor/api/list```\
Returns a list of all available tailors and a full description regarding their rating, average amongst others.
* __tailor-creation__\
```POST /tailor/api/create/```\
Creates a new instance of a tailor. Returns a `500` error if it already exists.
* __tailor-update__\
```PUT PATCH /tailor/api/update/<user_id>/```\
Updates the given tailor using the `user_id` passed in the url.
* __rating__\
```POST /tailor/api/rating/```\
Creates a new rating for a tailor if it doesn't exist.
* __rating-update-via-Rating__\
```PUT /tailor/api/rating/update/<rating_id>/```\
Updates an existing rating for a particular tailor where the `rating_id` is readily available.
* __rating-update-via-Tailor__\
```PUT /tailor/api/rating/update/<tailor_id>/tailor/```\
Updates an existimg tailor rating where the `tailor_id` is readily available. This would be used in most cases.
* __wallet-notification__\
```GET /tailor/api/wallet/notification/```\
Gets the wallet notification for a tailor. By default, it renders all notifications. To get notification for a particular wallet, pass a query parameter `?wallet` to the url. `?wallet=credit` returns the tailor's credit notification, `?wallet=withdrawal` returns the tailor's withdrawal notification, `?wallet=pending` returns the tailor's pending balnace notifications.
* __Book-Tailor__\
```POST /tailor/api/book/```\
Books a user with the given id.
* __TailorBookingsList__\
```GET /tailor/api/mybooking/```\
Gets all bookings made to the logged in tailor.
* __dashboard__\
```GET /tailor/api/dashboard/```\
Renders data to be displayed on a tailor's dashboard.
* __get-customers__\
```GET /tailor/api/get-customers/```\
Returns all customers that the current logged in tailor has worked for.
* __CreateRatingImage__\
```POST /tailor/api/rating/image/create/<uuid:tailor_id>/```\
Creates images uploaded by a user during tailor rating.
* __Feedbacks__\
```GET /tailor/api/feedbacks/```\
Gets all related ratings and feedbacks of the current tailor.


[shop_api](https://github.com/codewitgabi/tailor_api/tree/main/shop_api)\
This app holds every endpoint that are cloth related. This is where the main functionality of the API lie.

* __product-upload__\
```POST /shop/api/product/upload/```\
Creates a cloth instance and save it to the database.
* __store-view__\
```GET /shop/api/product/store/```\
Gets all product uploaded by a particular tailor. Requires authentication and the user must be a tailor instance to be able to see result else an invalid response is raised.
* __product-list__\
```GET /shop/api/product/list/```\
Gets all the cloth available. To get cloth based on category, pass the category as a query parameter to the url. e.g `/shop/api/product/list/?q=<category_query>` returns all men-related cloth. There are certain filters like category on the cloth section page. For that, also pass it as a query parameter in the manner. `/shop/api/product/list/?category=<subcategory_query>`. Note that you can pass these two params together by using the `&` operator.
* __product-update__\
``` PATCH PUT /shop/api/product/update/<uuid:id>/```\
Updates an uploaded product using its given uuid. The get the best result, use a `PATCH` request.
* __add-to-favorite__\
```POST /shop/api/product/add-to-fav/```\
Adds a product to your favorite list.
* __remove-from-favorite__\
```DELETE /shop/api/product/remove-from-fav/<int:id>/```\
Removes a product from a user's favorite list.
* __favorite-list__\
```GET /shop/api/product/favorites/list/```\
Returns a list of all the products in a users favorite list
* __product-create-comment__\
```POST /shop/api/product/comment/create/```\
Creates a comment related to a product.
* __get-product-comment__\
```GET /shop/api/product/<uuid:id>/comments/```\
Gets all product related comment. The product's id is to be passed in the url.
* __rate-product__\
```POST /shop/api/product/rating/```\
Creates a rating for a product.
* __like-product__\
```POST /shop/api/product/like/```\
Like event for a product.
* __unlike-product__\
```DELETE /shop/api/product/unlike/<int:id>/```\
Deletes like object from previously liked product.
* __save-debitcard__\
```POST /shop/api/card/create/```\
Saves a user's debit card details to the database.
* __add/remove-from-cart__\
```POST cart/<str:action>/<uuid:cloth_id>/```\
Adds product with the given `id` to the currently logged in user's cart. The specified action determines the action to be done. use `add` to add to the cart and `sub` to remove from cart.
* __cart-display__\
```GET /shop/api/cart/display/```\
Display the cart details of the currently logged in user.
* __cart-complete__\
```POST /shop/api/cart/complete/```\
Clears a user cart after successful payment.
* __transactions__\
```GET /shop/api/transactions/```\
Returns a list of all transactions made by a tailor. Can only be accessed by a tailor.

[chat](https://github.com/codewitgabi/tailor_api/tree/main/chat)\
This app contains endpoints for chat messages.

* __create-message__\
```POST /chat/api/create/```\
Creates a chat message between two users by passing the id of the user to receive the message. The sender is automatically the logged in user.
* __get-messages__\
```GET /chat/api/get-messages/<uuid:id>/```\
Gets all messages of the logged in user and the user with the given id.

## Author
Gabriel Michael Ojomakpene\
09020617734\
codewitgabi222@gmail.com