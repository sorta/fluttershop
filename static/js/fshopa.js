

function collapseInput()
{
    if (localStorage['post_shown'] == "true")
    {
        $("#pe0").collapse("hide");
        $("#pe_title").collapse("hide");
        $("#pe_details").collapse("hide");
        $("#pe_post_buttons").collapse("hide");
    }

    localStorage['post_shown'] = "false";
}

function expandInput()
{
    if (localStorage['post_shown'] == "false")
    {
        $("#pe_title").collapse("show");
        $("#pe_details").collapse("show");
        $("#pe_post_buttons").collapse("show");
    }

    localStorage['post_shown'] = "true";
}

function flip_cb()
{
    var thisid = "#" + this.id + "_c";
    var pst_cb = $(thisid);
    pst_cb.attr('checked', !pst_cb.attr('checked'));
}

function setButtonAndCb(base_id, value)
{
    base_id = "#" + base_id;
    var cb_id = base_id + "_c";

    $(base_id).val(value);
    $(base_id).removeClass("active");
    if (value) { $(base_id).addClass("active"); }
    $(cb_id).attr('checked', value);
}

function setDeleteTab(id, name)
{
    $("input#delete_tab_id").val(id);
    $("input#delete_tab_name").val(name);
    $("span#delete_tab_label").text(name);
}

function setEditTab(action, parent, name, rank, title, desc, tid, ppp)
{
    $("input#edit_tab_action").val(action);
    $("span#tab_action").text(action);
    $("input#edit_tab_parent").val(parent);
    $("input#edit_tab_id").val(tid);
    $("input#edit_tab_name").val(name);
    $("input#edit_tab_rank").val(rank);
    $("input#edit_tab_title").val(title);
    $("textarea#edit_tab_desc").val(desc);
    $("input#edit_tab_ppp").val(ppp);
}

function setEditPost(action, pid, title, content, showtitle, showdate, rank, alignment, width, collapse)
{
    if (collapse === true)
        collapseInput();
    else
        expandInput();
    var actionLabel = action + " post";
    $("#edit_post_action").val(action);
    $("span#post_action").text(actionLabel);
    $("#edit_post_id").val(pid);
    $("#edit_post_title").val(title);
    $("#edit_post_content").setCode(content);
    $("#edit_post_content").setFocus();

    setButtonAndCb("edit_post_showtitle", showtitle);
    setButtonAndCb("edit_post_showdate", showdate);

    $("#edit_post_rank").val(rank);
    $("#edit_post_alignment").val(alignment);
    $("#edit_post_width").val(width);
}

function setDeletePost(post_id, title)
{
    $("input#delete_post_id").val(post_id);
    $("span#delete_post_label").text(title);
}

$(document).ready(function()
{
    $("#edit_post_title").on('focus', expandInput);
    localStorage['post_shown'] = "false";
    $('#edit_post_content').redactor();
    $(".hidden_flipper").click(flip_cb);
});
