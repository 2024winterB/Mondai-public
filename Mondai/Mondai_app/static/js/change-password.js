function togglePasswordVisibility(inputId) {
  let passwordInput = document.getElementById(inputId);
  let eyeIcon = document.getElementById(inputId + "-toggle");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      eyeIcon.classList.add("visible");
  } else {
      passwordInput.type = "password";
      eyeIcon.classList.remove("visible");
  }
}