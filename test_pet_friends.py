from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Extra', animal_type='kitty',
                                     age='20', pet_photo='images/Cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Мои тесты/Позитивные


def test_add_pet_without_photo(name: str = 'Гена', animal_type='sloth', age=10):
    """Проверка возможности добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_pet_jpeg_photo(pet_photo='images/sloth1.jpeg'):
    """Проверка возможности добавления фото формата jpeg к существующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ""

    else:
        raise Exception('There is no my pets')


def test_add_pet_png_photo(pet_photo='images/blob.png'):
    """Проверка возможности добавления фото формата png к существующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ""

    else:
        raise Exception('There is no my pets')


# Мои тесты/Негативные


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """ Проверка запроса api ключа с невалидным email возвращает статус 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_invalid_password(email=valid_email,  password=invalid_password):
    """ Проверка запроса api ключа с невалидным паролем возвращает статус 403"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_invalid_key(filter='my_pets'):
    """Проверка получения списка питомцев с невалидным ключом api"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = 'invalid_key'
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200
    assert 'my_pets' not in result


def test_add_pet_without_photo_and_invalid_age(name: str = 'Гена', animal_type='sloth', age=-1):
    """Проверка возможности добавить питомца с отрицательным значением age"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    if status == 200:
        raise Exception("Age accepts negative value")
    else:
        assert status == 500


def test_add_pet_gif_photo(pet_photo='images/kitten.gif'):
    """Проверка возможности добавления фото формата gif к существующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500

    else:
        raise Exception('There is no my pets')


def test_add_pet_with_empty_data(name='', animal_type='', age='', pet_photo='images/tiger.jpeg'):
    """Проверка возможности добавить питомца с пустыми значениями"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    if status != 200:
        pass
    else:
        raise Exception('Blank pet added')


def test_delete_someones_pet():
    """Проверка возможности удаления чужого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')
    if len(all_pets['pets']) == 0:
        raise Exception('There is no pets')
    else:
        pet_id = all_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "")
        assert status == 200
        assert pet_id not in all_pets.values()
