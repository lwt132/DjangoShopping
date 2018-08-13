$(function () {
    initswiper()  //轮播
    mustBuyswiper()

})

function initswiper() {
  var mySwiper = new Swiper ('#topSwiper', {
    loop: true,
      autoplay: 500,
    // 如果需要分页器
    pagination: '.swiper-pagination',
  })
}

function mustBuyswiper(){
  var swiper = new Swiper('#swiperMenu', {
        slidesPerView: 3,
        spaceBetween: 10
    })
}
