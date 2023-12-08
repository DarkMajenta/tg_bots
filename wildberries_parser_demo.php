<?php

// Функция для отправки POST-запросов
function sendPostRequest($url, $data) {
    $options = array(
        'http' => array(
            'header' => "Content-type: application/x-www-form-urlencoded\r\n",
            'method' => 'POST',
            'content' => http_build_query($data),
        ),
    );
    $context = stream_context_create($options);
    $response = file_get_contents($url, false, $context);
    return $response;
}

// Функция для сохранения куки в файл
function saveCookies($cookies, $filename) {
    file_put_contents($filename, $cookies);
}

// Функция для загрузки куки из файла
function loadCookies($filename) {
    return file_get_contents($filename);
}

// Функция для авторизации
function authorize($phone) {
    // Запрос кода по номеру телефона
    $url = 'https://www.wildberries.ru/phone-verification/send-code';
    $data = array('phone' => $phone);
    $response = sendPostRequest($url, $data);

    // Обработка ответа и ввод кода полученного на телефон
    $code = readline('Введите код, полученный на телефон: ');

    // Сохранение полученных куки в файл
    saveCookies($http_response_header[6], 'cookies.txt');
}

// Функция для получения данных после авторизации
function getData() {
    // Загрузка сохраненных куки из файла
    $cookies = loadCookies('cookies.txt');

    // Создание контекста с сохраненными куками
    $options = array(
        'http' => array(
            'header' => "Cookie: " . $cookies,
        ),
    );
    $context = stream_context_create($options);

    // Запрос нужных данных
    $url = 'https://www.wildberries.ru/some-data-endpoint';
    $response = file_get_contents($url, false, $context);

    // Обработка полученных данных
    // ...

    return $data;
}

// Пример использования функций
$phone = readline('Введите номер телефона: ');
authorize($phone);
$data = getData();
var_dump($data);
