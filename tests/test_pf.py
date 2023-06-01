import os
import pytest
import sys

sys.path.append('../')

from api_pf import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password

pf = PetFriends()


@pytest.mark.usefixtures('del_pet')
class TestAddPetsPositive:

    @pytest.mark.add
    def test_add_new_pet_with_valid_data(self, get_key, name='Баль', animal_type='белка',
                                         age='4', pet_photo=r'images\P1040103.jpg'):
        """Проверяем что можно добавить питомца с корректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Получаем api ключ через фикстуру get_key
        print('PET_PHOTO путь', pet_photo)

        # Добавляем питомца
        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name

    @pytest.mark.add
    def test_add_new_pet_without_photo(self, get_key, request_fixture, name='Repl', animal_type='cat',
                                       age='17'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        # Получаем api ключ через фикстуру get_key

        # Добавляем питомца
        status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

        # print('Проверка добавления питомца', result)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['pet_photo'] == ''


@pytest.mark.usefixtures('del_pet')
class TestAddNegative:

    @pytest.mark.add
    def test_add_new_pet_without_age(self, get_key, name='Барбоскин', animal_type='двортерьер',
                                     age='', pet_photo='images\cat1.jpg'):
        """Проверяем что можно добавить питомца c пустым значением в поле age"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Получаем api ключ через фикстуру get_key

        # Добавляем питомца
        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['age'] == ''

    @pytest.mark.add
    def test_add_new_pet_with_speсial_symbols_data(self, get_key, name='@#$*&^', animal_type='*&^$%#',
                                                   age='#$%^*&^&%^', pet_photo=r'images\cat1.jpg'):
        """Проверяем что можно добавить питомца cо спецсимволами в полях name, animal_type, age"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Получаем api ключ через фикстуру get_key

        # Добавляем питомца
        status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        assert result['age'] == age

    @pytest.mark.xfail
    def test_add_new_pet_without_photo_empty_data(self, get_key, name='', animal_type='', age=''):
        """Проверяем что можно добавить питомца с пустыми полями name, animal_type, age  без фото"""

        # Получаем api ключ через фикстуру get_key

        # Добавляем питомца
        status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == ''
        assert result['animal_type'] == ''
        assert result['age'] == ''
        assert result['pet_photo'] == ''


class TestGetList:

    @pytest.mark.list
    def test_get_all_pets_with_valid_key(self, get_key, filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Получаем api ключ через фикстуру get_key. Далее используя этот ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        status, result = pf.get_list_of_pets(get_key, filter)
        # print('принтуем get_key', get_key)

        assert status == 200
        assert len(result['pets']) > 0

    @pytest.mark.list
    def test_get_my_pets_with_valid_key(self, get_key, filter='my_pets'):
        """ Проверяем что запрос питомцев c параметром 'my_pets'возвращает не пустой список.
        Получаем api ключ через фикстуру get_key. Далее, используя этот ключ,
        запрашиваем список питомцев c параметром 'my_pets' и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

        _, my_pets = pf.get_list_of_pets(get_key, filter)

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            # добавляем нового питомца
            pf.add_new_pet_without_photo(get_key, "ADD", "cat_add", "7")

        status, result = pf.get_list_of_pets(get_key, filter)
        assert status == 200
        assert len(result['pets']) > 0


    @pytest.mark.list
    def test_get_all_pets_with_not_valid_key(self, get_key, filter='argaeg'):
        """ Проверяем что запрос всех питомцев c невалидным значением параметра filter возвращает ошибку 500.
        Получаем api ключ через фикстуру get_key. Далее, используя этот ключ,
        запрашиваем список всех питомцев. Доступное значение параметра filter - 'my_pets' либо '' """

        status, result = pf.get_list_of_pets(get_key, filter)

        assert status == 500




class TestUpdatePet:

    def test_successful_update_self_pet_info(self, get_key, request_fixture, name='Мурзик', animal_type='Котэ', age='5'):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем api ключ через фикстуру get_key

        # Получаем список своих питомцев
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Если список не пустой, то пробуем обновить данные последнего питомца( имя, тип и возраст)
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    # @pytest.mark.skip
    def test_add_pet_photo(self, get_key, request_fixture, pet_photo=r'images\cat1.jpg'):
        """Проверяем что можно добавить или заменить фото питомца с корректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Получаем api ключ через фикстуру get_key

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            # добавляем нового питомца
            pf.add_new_pet_without_photo(get_key, "ADD", "cat_add", "7")

            # запрашиваем список своих питомцев
            _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Запоминаем id первого питомца из списка
        pet_id = my_pets['pets'][0]['id']

        # Добавляем или заменяем фото питомца
        status, result = pf.add_pet_photo(get_key, pet_id, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert 'pet_photo' in result

class TestAuthNegative:

    @pytest.mark.auth
    def test_get_api_key_for_not_valid_password(self, email=valid_email, password=not_valid_password):
        """ Проверяем что запрос api ключа с невалидным password возвращает статус 403 """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403



    @pytest.mark.auth
    def test_get_api_key_for_not_valid_email(self, email=not_valid_email, password=valid_password):
        """ Проверяем что запрос api ключа с невалидным email возвращает статус 403 """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403



    @pytest.mark.auth
    def test_get_api_key_empty_data(self, email='', password=''):
        """ Проверяем что запрос api ключа с пустыми email и password возвращает статус 403 """

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403

class TestDeletePet:

    def test_successful_delete_self_pet(self, get_key):
        """Проверяем возможность удаления питомца"""

        # Получаем api ключ через фикстуру get_key

        # Получаем список своих питомцев
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(get_key, "Суперкот", "кот", "3", "images\cat1.jpg")
            _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(get_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(get_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()






