

/* swiper control */
var mySwiper = new Swiper('.swiper-story', {
    slidesPerView: 'auto',
    centeredSlides: false,
    spaceBetween: 15
});
var mySwiper2 = new Swiper('.swiper-post', {
    slidesPerView: 'auto',
    centeredSlides: false,
    spaceBetween: 1,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
});

$(document).ready(function(){
    /* photos gallery */
    $('.grid').masonry({
         itemSelector: '.grid-item',
         percentPosition: true
    });


});
$(window).on("load resize", function () {
     $('.grid').masonry({
         itemSelector: '.grid-item',
         percentPosition: true
     });
 });
