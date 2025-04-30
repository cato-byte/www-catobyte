// menu.js
//document.addEventListener("DOMContentLoaded", function () {
//    const hamburger = document.querySelector(".hamburger");
//    const navbar = document.querySelector(".navbar");
  
//    hamburger.addEventListener("click", function () {
//      navbar.classList.toggle("active");
//    });
//  });
document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.querySelector(".hamburger");
    const navbar = document.querySelector(".navbar");

    hamburger.addEventListener("click", function () {
      navbar.classList.toggle("active");
    });
    
    document.addEventListener("click", function (e) {
        // If click is outside both the navbar and the hamburger
        if (!e.target.closest(".navbar") && !e.target.closest(".hamburger")) {
          navbar.classList.remove("active");
        }
      });

  });