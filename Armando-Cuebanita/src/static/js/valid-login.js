document.addEventListener('DOMContentLoaded', function() {
    var formLogin = document.getElementById('form-login');
    var btnEnviar = formLogin.querySelector('.btn-form');

    btnEnviar.addEventListener('click', function(event) {
        event.preventDefault(); // Evitar que el formulario se envíe automáticamente

        var email = document.getElementById('email').value.trim();
        var password = document.getElementById('password1').value;
        var check = document.getElementById('check').checked;

        // Validar que el correo electrónico, la contraseña y el checkbox no estén vacíos
        if (email === '' || password === '' || !check) {
            alert('Por favor, complete todos los campos.');
            return;
        }

        // Validar formato de correo electrónico
        var emailRegExp = /^\S+@\S+\.\S+$/;
        if (!emailRegExp.test(email)) {
            alert('Ingrese un correo electrónico válido.');
            return;
        }

        // Si todas las validaciones pasan, enviar el formulario
        alert("El formulario LOGIN fue aceptado sin problemas");
        formLogin.submit();
    });
});
