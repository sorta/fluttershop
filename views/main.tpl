<!DOCTYPE html>
<html>

    <head>
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.css" type="text/css" />
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap-responsive.css" type="text/css" />
        <link rel="stylesheet" href="/static/css/ws1.css" type="text/css" />

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js"></script>
        <script language="javascript" src="/static/bootstrap/js/bootstrap.js"></script>

        %if logged_in:
            <link rel="stylesheet" href="/static/js/redactor/css/redactor.css" />

            <script src="/static/js/redactor/redactor.js"></script>
            <script language="javascript" src="/static/js/fshopa.js"></script>
        %end
        <title>{{ page_title }}</title>
        <meta name="description" content="{{ page_desc }}" />
    </head>
    <body style="padding-top: 40px;">

        %setdefault('def_ppp', 10)

        %include modals.tpl selected_tab=selected_tab, logged_in=logged_in, user=get('user', {}), site_name=site_name, def_ppp=def_ppp

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
                            %for mane in tabs[0]:
                                %if mane['nav_display']:
                                    %class_str = ""
                                    %if selected_tab['_id'] == mane['_id']:
                                        %class_str += "active"
                                    %end

                                    %if class_str != "":
                                        <li class="{{class_str}}">
                                    %else:
                                        <li>
                                    %end

                                    <a href="{{ mane['path'] }}">{{ mane['display'] }}</a></li>
                                    %if logged_in:
                                        <li>
                                            <a data-toggle="modal" href="#delete_tab_modal" onclick="setDeleteTab('{{ mane['_id'] }}', '{{ mane['name'] }}');" class="mane_funcs">
                                                <i class="icon-remove icon-white"></i>
                                            </a>
                                            <a data-toggle="modal" href="#edit_tab_modal"
                                                onclick="setEditTab('edit', '{{ mane.get('parent', None) }}', '{{ mane['name'] }}', '{{ mane['rank'] }}', '{{ mane['title'] }}', '{{ mane['desc'] }}', '{{ mane['_id'] }}');" class="mane_funcs">
                                                    <i class="icon-edit icon-white"></i>
                                            </a>
                                        </li>
                                    %end
                                %end

                            %end
                            %if logged_in:
                                <li><a data-toggle="modal" href="#edit_tab_modal" onclick="setEditTab('add', null, null, {{ len(tabs[0]) }});" class="badge badge-info"><i class="icon-plus"></i></a></li>
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
        <div class="tabbable">
            %for (counter, tab_row) in enumerate(tabs):
                %if counter != 0 and (logged_in or len(tab_row) > 0):
                    %example_parent = "'{0}'".format(selected_tab['_id'])
                    <ul class="nav nav-tabs no_bottom">
                        %for tab in tab_row:
                            %if selected_tab['_id'] == tab['_id']:
                                <li class="active">
                            %else:
                                <li>
                            %end
                            %if tab['parent']:
                                %example_parent = "'{0}'".format(tab['parent'])
                            %end

                            <a href="{{ tab['path'] }}">{{ tab['display'] }}</a>
                            </li>
                            <li>
                            %if logged_in:
                                <div class="tail_funcs">
                                    <a data-toggle="modal" href="#delete_tab_modal" onclick="setDeleteTab('{{ tab['_id'] }}', '{{ tab['name'] }}');" class="tail_funcs">
                                        <i class="icon-remove"></i>
                                    </a>
                                    <a data-toggle="modal" href="#edit_tab_modal"
                                        onclick="setEditTab('edit', '{{ tab.get('parent', None) }}', '{{ tab['name'] }}', '{{ tab['rank'] }}', '{{ tab['title'] }}', '{{ tab['desc'] }}', '{{ tab['_id'] }}');" class="tail_funcs">
                                            <i class="icon-edit"></i>
                                    </a>
                                </div>

                            %end
                            </li>
                        %end
                        %if logged_in:
                            <li>
                                <a data-toggle="modal" href="#edit_tab_modal" onclick="setEditTab('add', {{ example_parent }}, null, {{ len(tab_row) }});" class="badge badge-info"><i class="icon-plus"></i></a>
                            </li>
                        %end
                    </ul>
                %end
            %end
            <!-- CONTENT -->
            <div class="tab-content">
                <div style="height: 19px"></div>
                <div class="tab-pane active" id="ActiveTab">
                    <div class="container">

                        %for msg in flash_alerts:
                            <div class="alert alert-block fade in {{ msg['msg_classes'] }}">
                                <button type="button" class="close" data-dismiss="alert">×</button>
                                %if msg['title']:
                                    <h4 class="alert-heading">{{ msg['title'] }}</h4>
                                %end
                                {{ msg['message'] }}
                            </div>
                        %end

                        %if logged_in:
                            <div class="row-fluid">
                                <div class="span12">
                                    <table class="table table-bordered">
                                        <tbody>
                                            <tr>
                                                <td>
                                                    <form class="form-vertical" action="/_sitefuncs_/addpost" method="post">
                                                        <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />

                                                        <div id="pe_title" class="collapse">
                                                            <label>Title</label>
                                                        </div>

                                                        <input name="post_title" id="post_title" type="text" class="span12" placeholder="Post something..." data-toggle="collapse" data-target="#pe0"></input>

                                                        <div id="pe0" class="collapse"></div>

                                                        <div id="pe_details" class="collapse">
                                                            <label>Post Content*</label>
                                                            <textarea name="post_content" id="post_tb" class="span12"></textarea>
                                                        </div>

                                                        <div id="pe_post_buttons" class="collapse">
                                                            <div class="row-fluid">
                                                                <div class="span2">
                                                                    <label>Show</label>
                                                                    <div class="btn-group" data-toggle="buttons-checkbox">
                                                                        <button type="button" id="pst_button" class="btn hidden_flipper active">Title</button>
                                                                        <button type="button" id="psd_button" class="btn hidden_flipper active">Date</button>
                                                                    </div>
                                                                    <input type="checkbox" id="pst_button_c" class="hide" name="post_show_title" checked="true"/>
                                                                    <input type="checkbox" id="psd_button_c" class="hide" name="post_show_date" checked="true"/>
                                                                </div>

                                                                <div class="span3">
                                                                    <label>Rank</label>
                                                                    <input name="post_rank" type="text" class="span12" value="{{ next_post_rank }}" ></input>
                                                                </div>

                                                                <div class="span3">
                                                                    <label>Alignment</label>
                                                                    <select class="span10" name="post_alignment">
                                                                        <option>Left</option>
                                                                        <option>Right</option>
                                                                        <option>Center</option>
                                                                        %for num in range(1, 12):
                                                                            <option>{{ num }}</option>
                                                                        %end
                                                                    </select>
                                                                </div>

                                                                <div class="span3">
                                                                    <label>Width</label>
                                                                    <select class="span10" name="post_width">
                                                                        %for num in range(12, 0, -1):
                                                                            <option>{{ num }}</option>
                                                                        %end
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

                        %include content.tpl rows=get('rows', []), logged_in=logged_in, selected_tab=selected_tab
                    </div>
                </div>
            </div>
        </div>
    </body>

</html>
