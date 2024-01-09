document.addEventListener("DOMContentLoaded", function() {
    var selectButtons = document.querySelectorAll(".select-tariff");
    var modalOverlay = document.querySelector(".modal-overlay");
    var successForm = document.querySelector(".success-form");
    var customForm = document.getElementById("custom-form");

    selectButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            // Отобразить модальное окно выбора способа оплаты
            modalOverlay.style.display = "flex";

            // Здесь можно добавить соответствующую логику для выбора способа оплаты
        });
    });

    customForm.addEventListener("submit", function(event) {
        event.preventDefault();

        // Получить значения полей формы
        var lastName = document.getElementById("last-name").value;
        var firstName = document.getElementById("first-name").value;
        var email = document.getElementById("email").value;
        var checkbox1 = document.getElementById("checkbox1").checked;
        var checkbox2 = document.getElementById("checkbox2").checked;

        // Отправить данные на сервер (можно использовать AJAX или другие методы)
        // В данном примере просто показываем успешное сообщение после отправки формы
        successForm.style.display = "block";
        customForm.reset();
    });
});
