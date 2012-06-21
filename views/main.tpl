<!DOCTYPE html>
<html>

    <head>
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.css" type="text/css" />
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap-responsive.css" type="text/css" />
        <link rel="stylesheet" href="/static/css/ws1.css" type="text/css" />
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js"></script>
        <!-- <script language="javascript" src="/static/js/jquery-1.7.1.min.js"></script> -->
        <script language="javascript" src="/static/bootstrap/js/bootstrap.js"></script>
        <script language="javascript" src="/static/js/ws1.js"></script>
    </head>
    <body style="padding-top: 40px;">

        %if get('selected_mane', None):
            %if get('selected_tail', None):
                %selected_route = "/{0}/{1}".format(selected_mane, selected_tail)
            %else:
                %selected_route = "/{0}".format(selected_mane)
            %end
        %else:
            selected_route = "/"
        %end
        <input name="selected_url" type="hidden" value="{{ selected_route }}" />

        %include modals.tpl selected_route=selected_route, selected_mane=get('selected_mane', '/'), manelinks=manelinks, taillinks=get('taillinks', []), logged_in=logged_in, user=get('user', {}), site_name=site_name

        <!-- NAVBAR -->
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container-fluid">

                    <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </a>
                    <div class="nav-collapse">
                        <!-- LEFT -->
                        <ul class="nav pull-left">

                            <li><a class="brand" href="/">{{ site_name }}</a></li>
                            %for link in manelinks:
                                %class_str = ""
                                %if defined('selected_mane') and selected_mane == link['mane_name']:
                                    %class_str += "active"
                                %end

                                %if class_str != "":
                                    <li class="{{class_str}}">
                                %else:
                                    <li>
                                %end

                                <a href="{{ link['route_name'] }}">{{ link['display'] }}</a></li>
                                %if logged_in:
                                    <li>
                                        <a data-toggle="modal" href="#delete_mane_modal_{{ link['mane_name'] }}">
                                            <i class="icon-remove icon-white"></i>
                                        </a>
                                    </li>
                                %end

                            %end
                            %if logged_in:
                                <li><a data-toggle="modal" href="#add_mane_modal" class="badge badge-info"><i class="icon-plus"></i></a></li>
                            %end

                        </ul>
                        <!-- Right -->
                        <ul class="nav pull-right">
                            <li class="divider-vertical"></li>
                            %if logged_in:
                                <li class="dropdown">
                                    <a class="dropdown-toggle" data-toggle="dropdown">{{ user.get("username", "User") }}<b class="caret"></b></a>
                                    <ul class="dropdown-menu">
                                        <li><a data-toggle="modal" href="#site_options_modal">Site Options</a></li>
                                        <li><a data-toggle="modal" href="#passchange_modal">Change Password</a></li>
                                        <li class="divider"></li>
                                        <li><a data-toggle="modal" href="#logout_modal">Log Out</a></li>
                                    </ul>
                                </li>
                            %else:
                                <li><a data-toggle="modal" href="#login_modal" ><span class="label label-info"><i class="icon-user"></i></span></a></li>
                            %end
                        </ul>

                    </div>
                </div>
            </div>
        </div>

        <!-- TABS -->
        <div class="tabbable tabs-left">
            <ul class="nav nav-tabs">
                %for link in get('taillinks', []):
                    %if defined('selected_tail') and selected_tail == link['tail_name'].lower():
                        <li class="active">
                    %else:
                        <li>
                    %end


                    %if logged_in:
                        <div class="close"><a data-toggle="modal" href="#delete_tail_modal_{{ link['tail_name'] }}">
                            <i class="icon-remove"></i>
                        </a></div>
                    %end
                    <a href="{{ link['route_name'] }}">{{ link['display'] }}</a>
                    </li>
                %end
                %if logged_in:
                    <li><a data-toggle="modal" href="#add_tail_modal" class="badge badge-info"><i class="icon-plus"></i></a></li>
                %end
            </ul>
            <!-- CONTENT -->
            <div class="tab-content">
                <div style="height: 19px"></div>
                <div class="tab-pane active" id="ActiveTab">
                    <div class="container-fluid">
                        %if logged_in:
                            <div class="row-fluid">
                                <div class="span6">
                                    <table class="table table-bordered">
                                        <tbody>
                                            <tr>
                                                <td>
                                                    <form class="form-vertical" action="/_sitefuncs_/addpost" method="post">
                                                        <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                                                        <input name="sel_post_type" id="sel_post_type" type="hidden" value="txt" />
                                                        <input name="enc_post_parts" id="enc_post_parts" type="hidden" value="" />

                                                        <div id="pe_title" class="collapse">
                                                            <label>Title</label>
                                                        </div>
                                                        <input name="post_title" type="text" class="span12" placeholder="Post something..." data-toggle="collapse" data-target="#pe0"></input>
                                                        <div id="pe0" class="collapse"></div>

                                                        <div id="pe_details" class="collapse">
                                                            <ul class="nav nav-pills" id="post_pills">
                                                                <li class="active"><a href="#pe_txt" data-toggle="pill"><i class="icon-pencil"></i></a></li>
                                                                <li><a href="#pe_pic" data-toggle="pill"><i class="icon-picture"></i></a></li>
                                                                <li><a href="#pe_lnk" data-toggle="pill"><i class="icon-globe"></i></a></li>
                                                                <li><a href="#pe_vid" data-toggle="pill"><i class="icon-film"></i></a></li>
                                                            </ul>

                                                            <div class="tab-content">
                                                                <div id="pe_txt" class="tab-pane active">
                                                                    <label>Post Text*</label>
                                                                </div>

                                                                <div id="pe_pic" class="tab-pane">
                                                                    <label>Url*</label>
                                                                    <input name="post_pic_url" type="text" class="span12"></input>
                                                                    <label>Alt-Text</label>
                                                                    <input name="post_pic_alt" type="text" class="span12"></input>
                                                                    <label>Caption</label>
                                                                    <input name="post_pic_cap" type="text" class="span12"></input>
                                                                    <label>Post Text</label>
                                                                </div>

                                                                <div name="pe_lnk" id="pe_lnk" class="tab-pane">
                                                                    <label>Url*</label>
                                                                    <input name="post_link_url" type="text" class="span12"></input>
                                                                    <label>Alt-Text</label>
                                                                    <input name="post_link_alt" type="text" class="span12"></input>
                                                                    <label>Post Text</label>
                                                                </div>

                                                                <div id="pe_vid" class="tab-pane">
                                                                    <label>Url*</label>
                                                                    <input name="post_vid_url" type="text" class="span12"></input>
                                                                    <label>Caption</label>
                                                                    <input name="post_vid_cap" type="text" class="span12"></input>
                                                                    <label>Post Text</label>
                                                                </div>
                                                                <textarea name="post_text" id="post_tb" class="span12"></textarea>
                                                            </div>
                                                        </div>
                                                        <div id="pe_post_buttons" class="collapse">
                                                            <div class="row-fluid">
                                                                <div class="span4">
                                                                    <label>Show</label>
                                                                    <div class="btn-group" data-toggle="buttons-checkbox">
                                                                        <button type="button" id="pst_button" class="btn active">Title</button>
                                                                        <button type="button" id="psd_button" class="btn active">Date</button>
                                                                        <input type="checkbox" style="display: none;" id="post_show_title" name="post_show_title" checked="true"/>
                                                                        <input type="checkbox" style="display: none;" id="post_show_date" name="post_show_date" checked="true"/>
                                                                    </div>
                                                                </div>

                                                                <div class="span4">
                                                                    <label>Alignment</label>
                                                                    <select class="span10" name="post_alignment">
                                                                        <option>Left</option>
                                                                        <option>Right</option>
                                                                        <option>Center</option>
                                                                        <option>1</option>
                                                                        <option>2</option>
                                                                        <option>3</option>
                                                                        <option>4</option>
                                                                        <option>5</option>
                                                                        <option>6</option>
                                                                        <option>7</option>
                                                                        <option>8</option>
                                                                        <option>9</option>
                                                                        <option>10</option>
                                                                        <option>11</option>
                                                                    </select>
                                                                </div>

                                                                <div class="span4">
                                                                    <label>Width</label>
                                                                    <select class="span10" name="post_width">
                                                                        <option>12</option>
                                                                        <option>11</option>
                                                                        <option>10</option>
                                                                        <option>9</option>
                                                                        <option>8</option>
                                                                        <option>7</option>
                                                                        <option>6</option>
                                                                        <option>5</option>
                                                                        <option>4</option>
                                                                        <option>3</option>
                                                                        <option>2</option>
                                                                        <option>1</option>
                                                                    </select>
                                                                </div>
                                                            </div>

                                                            <div>
                                                                <button style="display: inline;" type="submit" class="btn btn-primary pull-right"><i class="icon-plus"></i>Post</Button>
                                                            </div>
                                                        </div>
                                                    </form>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        %end
                        %include content.tpl rows=get('rows', [])
                    </div>
                </div>
            </div>
        </div>
    </body>

</html>
