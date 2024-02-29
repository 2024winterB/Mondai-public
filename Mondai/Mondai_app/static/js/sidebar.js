// ページが完全に読み込まれたときの処理
document.addEventListener('DOMContentLoaded', function() {
  // "nav_toggle" 要素がクリックされた時の処理を追加
  document.querySelector('.nav_toggle').addEventListener('click', function () {
    // "nav_toggle" 要素と "nav" 要素についている "show" クラスをトグル（ON/OFF切り替え）
    document.querySelector('.nav_toggle').classList.toggle('show');
    document.querySelector('.nav').classList.toggle('show');
  });
});