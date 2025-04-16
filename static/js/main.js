document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("clickMe");
  if (btn) {
    btn.addEventListener("click", () => {
      alert("Button clicked!");
    });
  }

  const hamburger = document.getElementById("hamburger");
  const navItems = document.querySelector(".nav-item-container");
  if (hamburger && navItems) {
    hamburger.addEventListener("click", () => {
      navItems.classList.toggle("active");
    });
  }
});

// Modal functionality for adding a new card
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("add-card-modal");
  const addCardBtn = document.getElementById("add-card-btn");
  const closeModal = document.querySelector(".modal .close");

  addCardBtn.addEventListener("click", function () {
    modal.style.display = "block";
  });

  closeModal.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
});
