// Custom JS for Proyecto-TPI
document.addEventListener('DOMContentLoaded', function () {
  try {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (el) { new bootstrap.Tooltip(el); });
  } catch (e) {}
});



