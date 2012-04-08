<!DOCTYPE html>
<html>

    <head>
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.css" type="text/css" />
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap-responsive.css" type="text/css" />
        <link rel="stylesheet" href="/static/css/ws1.css" type="text/css" />
        <script language="javascript" src="/static/js/jquery-1.7.1.min.js"></script>
        <script language="javascript" src="/static/js/ws1.js"></script>
        <script language="javascript" src="/static/bootstrap/js/bootstrap.js"></script>
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

        %include modals.tpl selected_route=selected_route, selected_mane=get('selected_mane', '/')

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

                            <li><a class="brand" href="/">{{ get('site_name', 'Unnamed Site') }}</a></li>
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


                                <a href="/{{ link['mane_name'] }}">{{ link['display'] }}</a></li>
                                %if logged_in:
                                    <li>
                                        <form class="form-inline" action="/deletemane" method="post">
                                            <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                                            <input name="mane_name" type="hidden" value="{{ link['mane_name'] }}" />
                                            <li><button type="submit" class='label label-info'><b class="icon-eject"></b></button></li>
                                        </form>
                                    </li>
                                %end
                            %end
                            %if logged_in:
                                <li><a data-toggle="modal" href="#add_mane_modal" class="badge badge-info"><i class="icon-plus-sign"></i></a></li>
                            %end

                        </ul>
                        <!-- Right -->
                        <ul class="nav pull-right">
                            %if logged_in:
                                <li>
                                    <div class="btn-group">
                                        <button class="btn btn-info dropdown-toggle" data-toggle="dropdown"><i class="icon-cog"></i><span class="caret"></span></button>
                                        <ul class="dropdown-menu">
                                            <li><a href="">Set Username</a></li>
                                        </ul>
                                    </div>
                                </li>
                                <li class="divider-vertical"></li>
                                <li class="dropdown">
                                    <a class="dropdown-toggle" data-toggle="dropdown">{{ user.get("username", "User") }}<b class="caret"></b></a>
                                    <ul class="dropdown-menu">

                                        <form action="/logout" method="post" id="logoutForm">
                                            <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                                            <li><input type="submit" class='btn' value="Log Out" /></li>
                                        </form>
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
                    <a href="/{{ link.name }}">{{ link['tail_name'] }}</a></li>
                %end
                %if logged_in:
                    <li><a data-toggle="modal" href="#add_tail_modal" class="badge badge-info"><i class="icon-plus-sign"></i></a></li>
                %end
            </ul>
            <!-- CONTENT -->
            <div class="tab-content">
                <div style="height: 19px"></div>
                <div class="tab-pane active" id="ActiveTab" click="loadTab()">
                    <div class="container-fluid">
                        %include content.tpl rows=get('rows', [])
                    </div>
                </div>
            </div>
        </div>
    </body>

</html>
