import pytest
from selenium import webdriver
import os
import time


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_page_path = os.path.join(current_dir, "test_pets_page.html")

    if not os.path.exists(test_page_path):
        create_test_html_page(test_page_path)

    driver.base_url = f"file:///{test_page_path}"

    yield driver

    time.sleep(1)
    driver.quit()


def create_test_html_page(file_path):
    html_content = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PetFriends</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <div id="all_pets" style="display: block;">
                <h1>Все питомцы</h1>
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <img src="https://via.placeholder.com/300x200?text=Cat+Photo" 
                                 class="card-img-top" alt="Кот Барсик">
                            <div class="card-body">
                                <h5 class="card-title">Барсик</h5>
                                <p class="card-text">Персидский кот, 3 года</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <img src="https://via.placeholder.com/300x200?text=Dog+Photo" 
                                 class="card-img-top" alt="Собака Шарик">
                            <div class="card-body">
                                <h5 class="card-title">Шарик</h5>
                                <p class="card-text">Овчарка, 5 лет</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <img src="https://via.placeholder.com/300x200?text=Parrot+Photo" 
                                 class="card-img-top" alt="Попугай Кеша">
                            <div class="card-body">
                                <h5 class="card-title">Кеша</h5>
                                <p class="card-text">Волнистый попугай, 2 года</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="my_pets" style="display: none;">
                <h1>Мои питомцы</h1>
                <div class="alert alert-info">
                    У вас 3 питомца
                </div>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Фото</th>
                            <th>Имя</th>
                            <th>Порода</th>
                            <th>Возраст</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><img src="https://via.placeholder.com/50x50?text=Cat" alt="Барсик"></td>
                            <td>Барсик</td>
                            <td>Персидский кот</td>
                            <td>3 года</td>
                        </tr>
                        <tr>
                            <td><img src="https://via.placeholder.com/50x50?text=Dog" alt="Шарик"></td>
                            <td>Шарик</td>
                            <td>Овчарка</td>
                            <td>5 лет</td>
                        </tr>
                        <tr>
                            <td><img src="https://via.placeholder.com/50x50?text=Parrot" alt="Кеша"></td>
                            <td>Кеша</td>
                            <td>Волнистый попугай</td>
                            <td>2 года</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-4">
                <button id="show_all_pets" class="btn btn-primary">Все питомцы</button>
                <button id="show_my_pets" class="btn btn-secondary">Мои питомцы</button>
            </div>
        </div>

        <script>
            document.getElementById('show_all_pets').addEventListener('click', function() {
                document.getElementById('all_pets').style.display = 'block';
                document.getElementById('my_pets').style.display = 'none';
            });

            document.getElementById('show_my_pets').addEventListener('click', function() {
                document.getElementById('all_pets').style.display = 'none';
                document.getElementById('my_pets').style.display = 'block';
            });
        </script>
    </body>
    </html>
    '''

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


@pytest.fixture(scope="function")
def auth_browser(browser):
    browser.get(browser.base_url)
    time.sleep(1)

    try:
        show_my_pets_button = browser.find_element("id", "show_my_pets")
        show_my_pets_button.click()
        time.sleep(1)
    except:
        pass

    return browser