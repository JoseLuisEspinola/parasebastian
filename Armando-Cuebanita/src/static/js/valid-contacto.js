// Función para validar el formulario
function validarFormulario(event) {
    event.preventDefault(); // Evitar el envío del formulario

    // Validar los campos: capturo el valor de los campos
    var apellido = document.getElementById("apellido").value;
    var nombre = document.getElementById("nombre").value;
    var telefono = document.getElementById("telefono").value;
    var email = document.getElementById("email").value;
    var mensaje = document.getElementById("mensaje").value;

    var errores = []; 

    console.log(apellido);

    if (apellido.trim() === "") {
        errores.push("Por favor, ingrese su apellido.");
    }

    if (nombre.trim() === "") {
        errores.push("Por favor, ingrese su nombre.");
    }

    if (!/^\+?[0-9]{2}-?[0-9]{10}$/.test(telefono)) {
        errores.push("El teléfono debe tener el formato correcto (+xx-1234567810).");
    }

    if (!/^\S+@\S+\.\w+(\.\w{2,})?$/.test(email)) {
        errores.push("Por favor, ingrese un correo electrónico válido (x@x.xxx).");
    }

    if (mensaje.trim() === "") {
        errores.push("Por favor, ingrese su mensaje.");
    }

    // Mostrar mensajes de error si la longitud es mayor a cero
    if (errores.length > 0) {
        alert(errores.join("\n"));
        return; // Detener el envío del formulario si hay errores, osea que se retorna
    }

    // Se enviará el formulario si no hay errores
    // Aquí podrías enviar el formulario mediante "algo" o hacer cualquier otra cosa
    alert("Formulario enviado correctamente.");
}

// Event listener al formulario "escuchar" el evento submit del boton
document.getElementById("form-contacto").addEventListener("submit", validarFormulario);
