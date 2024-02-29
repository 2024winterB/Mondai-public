function truncateText(elementClass, maxLengthSmall, maxLengthLarge) {
  let elements = document.getElementsByClassName(elementClass);
  for (let i = 0; i < elements.length; i++) {
    let element = elements[i];
    let originalText = element.getAttribute("data-original-text");
    let currentMaxLength = window.innerWidth <= 480 ? maxLengthSmall : maxLengthLarge;

    if (!originalText) {
      // 初回のみ元のテキストを保存
      originalText = element.textContent.trim();
      element.setAttribute("data-original-text", originalText);
    }

    if (originalText.length > currentMaxLength) {
      element.textContent = originalText.substring(0, currentMaxLength) + "…";
    } else {
      element.textContent = originalText;
    }
  }
}

// ウィンドウサイズ変更時に実行
window.addEventListener("resize", function () {
  truncateText("truncate", 4, 7);
  truncateText("tagtitle", 6, 10);
  truncateText("qstitle", 8, 15);
  truncateText("lgtitle", 10, 15);
});

// 初回実行
truncateText("truncate", 4, 7);
truncateText("tagtitle", 6, 10);
truncateText("qstitle", 8, 15);
truncateText("lgtitle", 10, 15);


// h1の文字数制限
document.addEventListener("DOMContentLoaded", function () {
  // キーワードの表示要素を取得
  let keywordElement = document.getElementById("keyword-name");
  // 制限する文字数（デフォルトは10文字）
  let charLimit = 13;
  // レスポンシブ表示時の制限文字数（例：6文字）
  let responsiveCharLimit = 9;
  // キーワードのテキストを取得
  let keywordText = keywordElement.textContent;
  // 対象の要素が list-question クラスを持っているかどうかを判定
  let isListQuestion = keywordElement.classList.contains("list-question");
  // 対象の要素が creation クラスを持っているかどうかを判定
  let isCreation = keywordElement.classList.contains("creation");
  // suffixText をオブジェクトとして定義
  let suffixText = {
    default: "の編集",
    alternative: "の問題一覧",
    creation: "の問題作成",
    edit: "の問題編集", // 追加した部分
  };
  // 対象の要素に応じて suffixText を選択
  let selectedSuffix = isListQuestion
    ? suffixText.alternative
    : isCreation
    ? suffixText.creation
    : suffixText.default;

  if (isListQuestion && isCreation) {
    // もし、"list-question" と "creation" の両方が存在する場合
    selectedSuffix = suffixText.edit;
  }

  // 初期表示時の文字数制限を適用
  applyCharLimit(keywordElement, keywordText, selectedSuffix, charLimit);

  // ウィンドウサイズ変更時に制限を変更（レスポンシブ）
  window.addEventListener("resize", function () {
    // 対象の要素に応じて suffixText を再選択
    let isListQuestion = keywordElement.classList.contains("list-question");
    let isCreation = keywordElement.classList.contains("creation");
    let selectedSuffix = isListQuestion
      ? suffixText.alternative
      : isCreation
      ? suffixText.creation
      : suffixText.default;

    if (isListQuestion && isCreation) {
      // もし、"list-question" と "creation" の両方が存在する場合
      selectedSuffix = suffixText.edit;
    }

    if (window.innerWidth < 480) {
      // 画面が小さい場合は制限をresponsiveCharLimitに変更
      applyCharLimit(
        keywordElement,
        keywordText,
        selectedSuffix,
        responsiveCharLimit
      );
    } else {
      // 画面が大きい場合は制限をcharLimitに変更
      applyCharLimit(keywordElement, keywordText, selectedSuffix, charLimit);
    }
  });
});

// 文字数制限を適用する関数
function applyCharLimit(element, text, suffix, limit) {
  console.log("Before Limit:", text);
  console.log("Suffix:", suffix);
  console.log("Limit:", limit);

  // テキストをトリミング
  text = text.trim();

  if (text.length + suffix.length > limit) {
    // 制限を超える場合はテキストを制限数まで切り詰めて表示
    let truncatedText = text.substring(0, limit - suffix.length).trim();
    element.textContent = truncatedText + "…" + suffix;

    console.log("After Limit:", element.textContent);
  } else {
    // 制限を超えない場合はそのまま表示
    element.textContent = text + suffix;
    console.log("After Limit:", element.textContent);
  }
}


