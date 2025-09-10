---
slides_folder: "1-intro"
---

# Introduction

<div class="swiper">
  <div class="swiper-wrapper">
    {% for image_path in slideshow_for_page() %}
    <div class="swiper-slide">
      <img src="../{{ image_path }}" alt="Slideshow image">
    </div>
    {% endfor %}
  </div>
  
  <div class="swiper-pagination"></div>
  <div class="swiper-button-prev"></div>
  <div class="swiper-button-next"></div>

</div>