const form = document.getElementById("formEncuesta");
const notificacion = document.getElementById("notificacion");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    fetch(form.action, {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (response.ok) {
            notificacion.classList.add("mostrar");

            form.reset();

            setTimeout(() => {
                notificacion.classList.remove("mostrar");
            }, 3000);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
