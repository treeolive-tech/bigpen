const btnBackToTop = document.querySelector("#btn-back-to-top");

function toggleScrollTop() {
  if (btnBackToTop) {
    window.scrollY > 100
      ? btnBackToTop.classList.add("active")
      : btnBackToTop.classList.remove("active");
  }
}

btnBackToTop.addEventListener("click", (e) => {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

window.addEventListener("load", toggleScrollTop);
document.addEventListener("scroll", toggleScrollTop);
