
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

function loadTab()
{
  /* grabs URL from HREF attribute then adds an  */
  /* ID from the DIV I want to grab data from    */
  var myUrl = $(this).attr("href");
  $("#ActiveTab").load(myUrl);
  return false;
}
