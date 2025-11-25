function confirmarEliminacionSimple(titulo, url) {
    Swal.fire({
        title: '¿Eliminar Oferta?',
        html: `¿Estás seguro de eliminar: <strong>${titulo}</strong>?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar confirmación de éxito inmediata
            Swal.fire({
                title: '¡Eliminado!',
                text: `La oferta "${titulo}" ha sido eliminada correctamente`,
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                // Redirigir después de que el usuario haga clic en "Aceptar"
                window.location.href = url;
            });
        }
    });
}