// AIボタンの要素を取得します。
var ai_generate = document.getElementById("ai_generate");
// ローディング用のdivを取得します。
var loading = document.getElementById("loading");
// ローディング用のdivを非表示にします。
loading.style.display = "none";
// フォームのsubmitイベントをキャッチします。
ai_generate.addEventListener("click", function(event) {
  // デフォルトの送信動作をキャンセルします。
  event.preventDefault();
  // id correct の要素を取得
  var id_correct_answer = document.getElementById("id_correct_answer");
  // id correct の値が空白かどうか判定
  if (id_correct_answer.value == "") {
    // 空白だったら、id correct の値を「解説参照」と設定
    id_correct_answer.value = "解説参照";
  }
  // フォームの要素を取得します。
  var form = document.getElementById("question-form");
  // フォームの送信先URLを取得
  const url = form.action;
  // フォームデータを作成
  const data = new FormData(form);
  // フォームデータにai_generateの値を追加
  data.append("ai_generate", "true");

  // Ajaxでサーバーに送信する関数を定義
  async function send() {
    // ローディング画面を表示
    loading.style.display = "block";

    // fetch APIでサーバーに送信
    const response = await fetch(url, {
      method: "POST",
      body: data
    });

    // ローディング画面を非表示
    loading.style.display = "none";

    // レスポンスが正常なら
    if (response.ok) {
      // レスポンスのテキストを取得
      const text = await response.text();
      // 現在のページをレスポンスのテキストで書き換え
      document.open();
      document.write(text);
      document.close();
      // 履歴に追加
      history.pushState(null, "", url);
    } else {
      // エラー処理
      console.error("Error:", response.status, response.statusText);
    }
  }
  // 送信関数を呼び出す
  send();
});