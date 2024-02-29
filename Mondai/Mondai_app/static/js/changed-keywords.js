document.addEventListener('DOMContentLoaded', function() {
  // クエリストリングスを解析。モダール表示のきっかけのパラメータを取得
  const urlParams = new URLSearchParams(window.location.search);
  //「modal」というパラメータの取得
  const show_modal = urlParams.get('modal');
  
  //URLのクエリパラメータをチェックし'modal=show'だった時のみ
  if (show_modal == 'show'){
    const mask = document.getElementById('mask');
    const modal = document.getElementById('modal');
    //maskのdisplayのプロパテを「none→block」にする。
    mask.style.display = 'block';
    //modalのdisplayのプロパテを「none→flex」にする。
    modal.style.display = 'flex';
  }
});
