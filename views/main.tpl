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
    <body>

        %setdefault('def_ppp', 10)

        %from json import dumps

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
                            %mane_count = 0
                            %for mane in tabs[0]:
                                %if mane['nav_display']:
                                    %mane_count += 1
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
                                            <a data-toggle="modal" href="#delete_tab_modal" onclick='setDeleteTab("{{ mane["_id"] }}", {{ dumps(mane["display"]) }});' class="mane_funcs">
                                                <i class="icon-remove icon-white"></i>
                                            </a>
                                            <a data-toggle="modal" href="#edit_tab_modal"
                                                onclick='setEditTab("edit", "{{ mane.get("parent", None) }}", {{ dumps(mane["display"]) }}, {{ mane["rank"] }}, {{ dumps(mane["title"]) }}, {{ dumps(mane["desc"]) }}, "{{ mane["_id"] }}");' class="mane_funcs">
                                                    <i class="icon-edit icon-white"></i>
                                            </a>
                                        </li>
                                    %end
                                %end

                            %end
                            %if logged_in:
                                <li><a data-toggle="modal" href="#edit_tab_modal" onclick="setEditTab('add', null, null, {{ mane_count }});" class="badge badge-info"><i class="icon-plus"></i></a></li>
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
        <div class="navbar_scooter"></div>
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
                                    <a data-toggle="modal" href="#delete_tab_modal" onclick='setDeleteTab("{{ tab["_id"] }}", {{ dumps(tab["display"]) }});' class="tail_funcs">
                                        <i class="icon-remove"></i>
                                    </a>
                                    <a data-toggle="modal" href="#edit_tab_modal"
                                        onclick='setEditTab("edit", "{{ tab.get("parent", None) }}", {{ dumps(tab["display"]) }}, "{{ tab["rank"] }}", {{ dumps(tab["title"]) }}, {{ dumps(tab["desc"]) }}, "{{ tab["_id"] }}");' class="tail_funcs">
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
                <div class="tab_content_divider"></div>
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
                                                    <form id="edit_post_form" class="form-vertical" action="/_sitefuncs_/editpost" method="post">
                                                        <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                                                        <input name="post_action" id="edit_post_action" type="hidden" value="add" />
                                                        <input name="post_id" id="edit_post_id" type="hidden" value="" />

                                                        <div id="pe_title" class="collapse">
                                                            <h2><span id="post_action" class="action_span">add post</span></h2>
                                                            <label>Title</label>
                                                        </div>

                                                        <input name="post_title" id="edit_post_title" type="text" class="span12" placeholder="Post something..." data-toggle="collapse" data-target="#pe0"></input>

                                                        <div id="pe0" class="collapse"></div>
                                                        <div id="pe1" class="collapse"></div>

                                                        <div id="pe_details" class="collapse">
                                                            <label>Post Content*</label>
                                                            <textarea name="post_content" id="edit_post_content" class="span12"></textarea>
                                                        </div>

                                                        <div id="pe_post_buttons" class="collapse">
                                                            <div class="row-fluid">
                                                                <div class="span2">
                                                                    <label>Show</label>
                                                                    <div class="btn-group" data-toggle="buttons-checkbox">
                                                                        <button type="button" id="edit_post_showtitle" class="btn hidden_flipper active">Title</button>
                                                                        <button type="button" id="edit_post_showdate" class="btn hidden_flipper active">Date</button>
                                                                    </div>
                                                                    <input type="checkbox" id="edit_post_showtitle_c" class="hide" name="post_showtitle" checked="true"/>
                                                                    <input type="checkbox" id="edit_post_showdate_c" class="hide" name="post_showdate" checked="true"/>
                                                                </div>

                                                                <div class="span3">
                                                                    <label>Rank</label>
                                                                    <input name="post_rank" id="edit_post_rank" type="text" class="span12" value="{{ next_post_rank }}" ></input>
                                                                </div>

                                                                <div class="span3">
                                                                    <label>Alignment</label>
                                                                    <select class="span10" name="post_alignment" id="edit_post_alignment">
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
                                                                    <select class="span10" name="post_width" id="edit_post_width">
                                                                        %for num in range(12, 0, -1):
                                                                            <option>{{ num }}</option>
                                                                        %end
                                                                    </select>
                                                                </div>
                                                            </div>

                                                            <div>
                                                                <button class="inl" type="submit" class="btn btn-primary pull-right"><i class="icon-plus"></i>Save</Button>
                                                                <button class="inl scoot_left" type="button" onclick="setEditPost('add', '', '', '', true, true, '{{ next_post_rank }}', 'left', 12);" class="btn pull-right">Cancel</Button>
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

                        %include content.tpl rows=get('rows', []), logged_in=logged_in, selected_tab=selected_tab, dumps=dumps
                    </div>
                </div>
            </div>
        </div>
    </body>

</html>
