// Custom JS for Proyecto-TPI
document.addEventListener('DOMContentLoaded', function () {
  try {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (el) { 
      new bootstrap.Tooltip(el); 
    });
  } catch (e) {}
});




  // -------------------------------
  // Inicializar mensajes tipo Toast
  // -------------------------------
  try {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
      var toast = new bootstrap.Toast(toastEl, {
        delay: 3500,
        autohide: true
      });
      toast.show();
    });
  } catch (e) {}

