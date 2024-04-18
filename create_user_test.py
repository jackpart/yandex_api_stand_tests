# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request
# Импортируем модуль data, в котором определены данные, необходимые для HTTP-запросов.
import data


def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body


# Функция для позитивной проверки
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
        + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == ("Имя пользователя введено некорректно. "
                                               "Имя может содержать только русские или латинские буквы, "
                                               "длина должна быть не менее 2 и не более 15 символов")


def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"


def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Аа")


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Абвгдежзиклмноп")


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")


def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аaaaaaaaaaaaaaaa")


def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


def test_create_user_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")


def test_create_user_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")


def test_create_user_digit_in_first_name_get_error_response():
    negative_assert_symbol("123")


def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)


def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)


def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(123)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
