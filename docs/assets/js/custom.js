// docs/assets/js/custom.js

document.addEventListener('DOMContentLoaded', function () {
  const swiper = new Swiper('.swiper', {
    // Disable looping for a better fullscreen experience
    loop: false,
    
    // If you want pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

    // If you want navigation buttons
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
});