document.addEventListener('DOMContentLoaded', function() {
  const changeButton = document.querySelector('#changeButton');
  const mask = document.querySelector('#mask');
  const modal = document.querySelector('#modal');
  const closeButton = document.querySelector('#closeButton');

  // 'changeButton' が存在する場合
    changeButton.addEventListener('click', function() {
      // フォームから新しいユーザー名とメールアドレスを取得
      const newUsername = document.getElementById('id_username').value; // フォームのユーザー名入力フィールドのID
      const newEmail = document.getElementById('id_email').value; // フォームのメールアドレス入力フィールドのID

      // モーダル内のテキストを更新（ラベルを含める）
      document.getElementById('modal-username').textContent = `アカウント名：${newUsername}`;
      document.getElementById('modal-email').textContent = `メールアドレス：${newEmail}`;

      // モーダルを表示
      modal.style.display = 'flex';
      mask.style.display = 'block';
    });
  // 'closeButton' が存在する場合のみイベントリスナーを追加

    closeButton.addEventListener('click', function() {
      modal.style.display = 'none';
      mask.style.display = 'none';
    });