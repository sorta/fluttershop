

// fix sub nav on scroll
var $win = $(window);
var $nav = $('#subnav');
var navTop = $('#subnav').length && $('#subnav').offset().top - 40;
var isFixed = 0;

processScroll();

$win.on('scroll', processScroll);

function processScroll() {
  var i, scrollTop = $win.scrollTop();
  if (scrollTop >= navTop && !isFixed) {
    isFixed = 1;
    $nav.addClass('subnav-fixed');
  } else if (scrollTop <= navTop && isFixed) {
    isFixed = 0;
    $nav.removeClass('subnav-fixed');
  }
}
