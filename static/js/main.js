document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("clickMe");
  btn.addEventListener("click", () => {
    alert("Button clicked!");
  });
});

document.addEventListener("click", () => {
  const hamburger = document.getElementById("hamburger");

  hamburger.addEventListener("click", () => {
    //logic for showing the mobile nav items menu
  });
});
