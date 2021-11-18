# vaccine-api-test

- Project to test: Flamby (Government module)
- Endpoint to test: create reservation (/reservation, method: POST) and login (/login, method: POST)

| Test Case ID | Name | Description |
|--------------|------|-------------|
|    TC-01     | test_create_reservation_but_not_login() | Verify that no one can not create any reservation if they not login |
|    TC-02     | test_create_reservation_with_fake_token() | Verify that no one can try to create reservation with a fake token |
|    TC-03     | test_create_reservation_with_valid_request_body() | Verify that the authorize user and valid format request body can create reservation |
|    TC-04     | test_create_reservation_with_invalid_datetime_format() | Verify that cannot create reservation with invalid datetime format |
|    TC-05     | test_create_reservation_with_no_request_body() | Verify that if user missing a require field, cannot create a reservation |
|    TC-06     | test_login_with_valid_id() | Verify that can login with registered account |
|    TC-07     | test_login_with_username_is_not_a_digit() | Verify that login path accept only citizen id username |
|    TC-08     | test_login_with_username_not_a_13_digit() | Verify that login path accept only citizen id username |
|    TC-09     | test_login_with_a_wrong_password() | Verify that if the user input the wrong password, they cannot get a access token back |
|    TC-10     | test_login_with_empty_request_body() | Verify that if user missing a require field, cannot login |