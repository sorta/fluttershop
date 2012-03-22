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

        <!-- MODALS -->
        <div class="modal hide fade" id="login_modal">
            <div class="modal-header">
                <a class="close" data-dismiss="modal">×</a>
                <h3>Please Login</h3>
            </div>
            <div class="modal-body">
                <form action="/login" class="form-vertical" method="post">
                    <label>Label name</label>
                    <input id="login_username" name="login_username" type="text" class="span3" placeholder="Email" />
                    <input id="login_pass" name="login_pass" type="text" class="span3" placeholder="Password" />

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
            </div>
            <div class="modal-footer">
                    <a class="btn" data-dismiss="modal">Close</a>
                    <input class="btn btn-primary" type="submit" value="Login" />
                </form>
            </div>
        </div>

        <!-- NAVBAR -->
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container-fluid">
                    <!-- LEFT -->
                    <ul class="nav pull-left">

                        <li><a class="brand" href="/">{{ get('site_name', 'Unnamed Site') }}</a></li>
                        %for link in manelinks:
                            %if defined('selected_mane') and selected_mane == link.name:
                                <li class="active">
                            %else:
                                <li>
                            %end
                            <a href="/{{ link.name }}">{{ link['mane_name'] }}</a></li>
                        %end
                        %if logged_in:
                            <li><form action="/addmane" method="post">
                                <div class="btn-group">
                                    <a class="btn dropdown-toggle" data-toggle="dropdown"><i class="icon-plus"></i></a>
                                    <ul class="dropdown-menu">
                                        <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                                        <li><input name="mane_name" type="text" /></li>
                                        <li><input type="submit" class='btn' value="Submit" /></li>
                                    </ul>
                                </div>
                            </form></li>
                        %end

                    </ul>
                    <!-- Right -->
                    <ul class="nav pull-right">
                        %if logged_in:
                            <li>
                                <div class="btn-group">
                                    <a class="btn btn-info dropdown-toggle" data-toggle="dropdown"><i class="icon-cog"></i>Options<span class="caret"></span></a>
                                    <ul class="dropdown-menu">
                                        <li><a href="">Set Username</a></li>
                                        <li class="divider"></li>

                                        <form action="/logout" method="post">
                                            <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                                            <li><input type="submit" class='btn' value="Log Out" /></li>
                                        </form>
                                    </ul>
                                </div>
                            </li>
                        %else:
                            <li><a data-toggle="modal" href="#login_modal" ><span class="label label-info"><i class="icon-user"></i></span></a></li>
                        %end
                    </ul>

                </div>
            </div>
        </div>

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
            </ul>
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
