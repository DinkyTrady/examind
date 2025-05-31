// Smooth scrolling animation
document.addEventListener("DOMContentLoaded", function () {
  // Add smooth reveal animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate-fade-in");
      }
    });
  }, observerOptions);

  // Observe all sections
  document.querySelectorAll("section").forEach((section) => {
    observer.observe(section);
  });

  // Add parallax effect to hero
  window.addEventListener("scroll", function () {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector("section.bg-teal-500");
    if (hero) {
      hero.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
  });
});

/* for navigation homepage */
// Mobile menu functionality
const menuNav = document.getElementById("mobile-menu");
const menuBtn = document.getElementById("mobile-menu-button");
const menuIcon = document.getElementById("menu-icon");
const closeIcon = document.getElementById("close-icon");

menuBtn.addEventListener("click", () => {
  if (menuNav.classList.contains("translate-x-full")) {
    menuNav.classList.remove("translate-x-full");
    menuIcon.classList.add("hidden");
    closeIcon.classList.remove("hidden");
  } else {
    menuNav.classList.add("translate-x-full");
    menuIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");
  }
});

/* change devs in homepage */
// Developer carousel for mobile
document.addEventListener("DOMContentLoaded", function () {
  window.addEventListener("resize", function () {
    const developers = document.querySelectorAll("#developers-grid > div");

    if (window.innerWidth >= 1280) {
      // On large screens, show all developers
      developers.forEach((dev) => {
        dev.style.display = "flex";
      });
    } else {
      // On small screens, maintain the carousel behavior
      updateDevDisplay();
    }
  });

  // Only run on mobile/small screens
  if (window.innerWidth < 1280) {
    const developers = document.querySelectorAll("#developers-grid > div");
    const prevBtn = document.getElementById("prev-dev");
    const nextBtn = document.getElementById("next-dev");
    const currentDevElement = document.getElementById("current-dev");
    const totalDevs = developers.length;
    let currentIndex = 0;

    // Initialize: hide all developers except the first one
    function updateDevDisplay() {
      developers.forEach((dev, index) => {
        dev.style.display = index === currentIndex ? "flex" : "none";
      });
      currentDevElement.textContent = currentIndex + 1;
    }

    // Initial setup
    updateDevDisplay();

    // Previous button click
    prevBtn.addEventListener("click", function () {
      currentIndex = (currentIndex - 1 + totalDevs) % totalDevs;
      updateDevDisplay();
    });

    // Next button click
    nextBtn.addEventListener("click", function () {
      currentIndex = (currentIndex + 1) % totalDevs;
      updateDevDisplay();
    });
  }
});

// use for redirect warning
function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = "none";
  }
}

// Optional: Auto-close after 3 seconds
window.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("errorModal");
  if (modal) {
    setTimeout(() => {
      closeModal("errorModal");
    }, 3000);
  }
});

// logout confirmation modal
const logoutBtn = document.getElementById("logout-btn");
const logoutModal = document.getElementById("logout-modal");
const cancelLogout = document.getElementById("cancel-logout");

logoutBtn.addEventListener("click", function (e) {
  e.preventDefault();
  logoutModal.classList.remove("hidden");
});

cancelLogout.addEventListener("click", function () {
  logoutModal.classList.add("hidden");
});
