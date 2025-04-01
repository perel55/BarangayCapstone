let currentIndex = 0;
const slides = document.querySelectorAll(".slide");

function moveSlide(step) {
    slides[currentIndex].classList.remove("active");
    currentIndex = (currentIndex + step + slides.length) % slides.length;
    slides[currentIndex].classList.add("active");
    document.querySelector(".slider").style.transform = `translateX(-${currentIndex * 100}%)`;
}

document.addEventListener("DOMContentLoaded", () => {
    setInterval(() => moveSlide(1), 5000); // Auto-slide every 5 seconds
});
