document.addEventListener("DOMContentLoaded", function () {
  let cells = document.querySelectorAll('.hoverable-cell, .hoverable-img');

  cells.forEach(cell => {
      cell.addEventListener('mouseenter', function () {
          let arrow = this.closest('tr').querySelector('.arrow-cell img');
          if (arrow) {
              arrow.style.transform = 'translate(5px, 0)';
              arrow.style.transitionDuration = '500ms';
          }
      });

      cell.addEventListener('mouseleave', function () {
          let arrow = this.closest('tr').querySelector('.arrow-cell img');
          if (arrow) {
              arrow.style.transform = 'none';
          }
      });
  });
});