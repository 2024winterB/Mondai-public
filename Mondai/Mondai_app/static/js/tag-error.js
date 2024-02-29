function checkTagLength() {
  let tagInput = document.getElementById("id_search_tag").value;
  let errorMessage = document.getElementById("tag-error-message");

  if (tagInput.length > 10) {
      errorMessage.style.display = "block";
      errorMessage.innerHTML = "<li>タグは10文字以下で入力してください。</li>";
  } else {
      errorMessage.style.display = "none";
      errorMessage.innerHTML = "";
  }
}