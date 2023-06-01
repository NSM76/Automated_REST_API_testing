import pytest

from api_pf import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


@pytest.fixture()
def get_key():
    """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
            JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    return auth_key


@pytest.fixture()
def del_pet():
    """Метод удаляет последнего добавленного питомца"""

    yield
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    print('\nСтатус удаления последнего питомца', status)

    assert status == 200
    assert pet_id not in my_pets.values()


@pytest.fixture()
def request_fixture(request):

    with open('log.txt', 'a', encoding="utf8") as myFile:
        myFile.write(f'\nЛоги теста : {request.function.__name__}\nПрименяется фикстура : {request.fixturename}\n'
                     f'scope фикстуры :{request.scope}\nПуть к файлу запуска теста : {request.fspath}'
                     '\n____________________________________')

    yield
