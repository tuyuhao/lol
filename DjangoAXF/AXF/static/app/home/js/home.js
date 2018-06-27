$(function () {

     // 顶部轮播
     new Swiper ('#topSwiper', {
         loop: true,
         pagination: '.swiper-pagination',
      });

        // 必购商品轮播
     new Swiper ('#swiperMenu', {
         slidesPerView: 3
      })
});