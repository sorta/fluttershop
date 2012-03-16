<!DOCTYPE html>

    <head>
        <link rel="stylesheet" href="/static/bootstrap/css/bootstrap.css" type="text/css" />
        <link rel="stylesheet" href="/static/css/ws1.css" type="text/css" />
        <script language="javascript" src="/static/js/jquery-1.7.1.min.js"></script>
        <script language="javascript" src="/static/bootstrap/js/bootstrap.js"></script>
    </head>

    <body style="padding-top: 40px;">

        <!-- NAVBAR -->
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <ul class="nav">

                        <li><a class="brand" href="/">{{ get('site_name', 'Unnamed Site') }}</a></li>
                        %for link in get('manelinks', ['Home', 'home']):
                            %if defined('selected_mane') and selected_mane == link[1]:
                                <li class="active">
                            %else:
                                <li>
                            %end
                            <a href="/{{ link[1] }}">{{ link[0] }}</a></li>
                        %end

                    </ul>
                </div>
            </div>
        </div>

        <div class="sidebar-container">
            <div class="sidebar-nav-fixed">
                <ul class="nav nav-tabs nav-stacked">
                    %for link in get('taillinks', []):
                        %if defined('selected_tail') and selected_tail == link[0].lower():
                            <li class="active">
                        %else:
                            <li>
                        %end
                        <a href="/{{ link[1] }}">{{ link[0] }}</a></li>
                    %end
                </ul>
            </div>
        </div>

        <div class="container-fluid sidebar-offset">
            <div class="row-fluid">

                <div class="span10">
                    %for a in range(0, 50):
                        {{ data }} <p />
                    %end
                </div>
            </div>
        </div>
    </body>

</html>
