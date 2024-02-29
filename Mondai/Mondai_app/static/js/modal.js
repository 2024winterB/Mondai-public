document.addEventListener('DOMContentLoaded', function() {
  // モーダル表示処理
  const mask = document.getElementById('mask');
  const modal = document.getElementById('modal');

  // ここでパスワード変更完了ページがロードされた時点でモーダルを表示
  mask.style.display = 'block';
  modal.style.display = 'flex';
});