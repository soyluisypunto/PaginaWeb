document.querySelectorAll(".btn-eliminar").forEach(btn => {
    btn.addEventListener("click", () => {
        if (!confirm("¿Eliminar este comentario?")) return;

        const comentario = btn.closest(".comentario");
        const id = comentario.dataset.id;

        fetch(`/eliminar_comentario/${id}`, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                comentario.remove();
            } else {
                alert("Error al eliminar");
            }
        });
    });
});
