

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

function flip_cb()
{
    var thisid = "#" + this.id + "_c";
    var pst_cb = $(thisid);
    pst_cb.attr('checked', !pst_cb.attr('checked'));
}

function setDeleteTab(id, name)
{
    $("input#delete_tab_id").val(id);
    $("input#delete_tab_name").val(name);
    $("span#delete_tab_label").text(name);
}

function setEditTab(action, parent, name, rank, title, desc, tid)
{
    $("input#edit_tab_action").val(action);
    $("input#edit_tab_parent").val(parent);
    $("input#edit_tab_id").val(tid);
    $("input#edit_tab_name").val(name);
    $("input#edit_tab_rank").val(rank);
    $("input#edit_tab_title").val(title);
    $("textarea#edit_tab_desc").val(desc);
}

$(document).ready(function()
{
    $("#pe0").on('show', expandInput);
    $('#post_tb').redactor();
    $('.red_tb').redactor();
    $(".hidden_flipper").click(flip_cb);
});
