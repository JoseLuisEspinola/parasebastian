function validarFormulario() {
    var apellido = document.getElementById('apellido').value.trim();
    var nombre = document.getElementById('nombre').value.trim();
    var email = document.getElementById('email').value.trim();
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var check = document.getElementById('dato_check').checked;

    // Validar que todos los campos obligatorios estén llenos
    if (apellido === '' || nombre === '' || email === '' || password1 === '' || password2 === '' || !check) {
        alert('Por favor, complete todos los campos obligatorios.');
        return false;
    }

    // Validar que las contraseñas coincidan
    if (password1 !== password2) {
        alert('Las contraseñas no coinciden.');
        return false;
    }

    // Validar formato de correo electrónico
    var emailRegExp = /^\S+@\S+\.\S+$/;
    if (!emailRegExp.test(email)) {
        alert('Ingrese un correo electrónico válido.');
        return false;
    }

    // Si todas las validaciones pasan, el formulario es válido
    alert("El formulario se envio correctamente...!!!");
    return true;
}

document.getElementById('form-registro').addEventListener('submit', function(event) {
    if (!validarFormulario()) {
        event.preventDefault(); // Evitar que se envíe el formulario si no pasa la validación
    }
});
