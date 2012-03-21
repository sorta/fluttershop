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
            <div class="modal hide fade" id="login_modal">
                <div class="modal-header">
                    <a class="close" data-dismiss="modal">×</a>
                    <h3>Modal header</h3>
                </div>
                <div class="modal-body">
                    <p>This is example text, see?</p>
                </div>
                <div class="modal-footer">
                    <a href="#" class="btn">Close</a>
                    <a href="#" class="btn btn-primary">Save changes</a>
                </div>
            </div>

        <!-- NAVBAR -->
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container-fluid">
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
                    </ul>
                    <ul class="nav pull-right">
                        <li><a class="pull-right" data-toggle="modal" href="#login_modal" ><span class="label label-info"><i class="icon-user"></i></span></a></li>
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
