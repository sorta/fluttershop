

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

function collapseInput()
{
    $("#pe_radio_buttons").collapse("hide");
    $("#pe_post_buttons").collapse("hide");
}

function expandInput()
{
    $("#pe_title").collapse("show");
    $("#pe_details").collapse("show");
    $("#pe_post_buttons").collapse("show");
}

function hideText()
{
    $("#pe_txt").collapse("hide");
}

function spt(e)
{
    var x = e.target.toString().slice(-3);
    $("#sel_post_type").attr("value", x);
}

function enableTab(tabname, val)
{
    // $(tabname).click(function (e)
    //     {
    //         e.preventDefault();
    //         $(this).tab('show');
    //     }
    // );
}

$(document).ready(function()
{
    $("#pe0").on('show', expandInput);
    $('a[data-toggle="pill"]').on('show', spt);
});
