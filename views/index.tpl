<!DOCTYPE html>

    <head>
        <link rel="stylesheet" href="static/bootstrap/css/bootstrap.css" type="text/css" />
        <link rel="stylesheet" href="static/css/ws1.css" type="text/css" />
        <script language="javascript" src="static/bootstrap/js/bootstrap.js"></script>
        <script language="javascript" src="static/js/jquery-1.7.1.min.js"></script>
    </head>

    <body style="padding-top: 40px;">

        <!-- NAVBAR -->
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <ul class="nav">

                        <li><a class="brand" href="#">Sorta Software</a></li>
                        <li class="active"><a href="#">Home</a></li>
                        <li><a href="#">About</a></li>
                        <li><a href="#">Projects</a></li>

                    </ul>
                </div>
            </div>
        </div>

        <div class="sidebar-container">
            <div class="sidebar-nav-fixed">
                <ul class="nav nav-tabs nav-stacked">
                    <li class="active"><a href="#">Blog</a></li>
                    <li><a href="#">Blag</a></li>
                    <li><a href="#">Blooog</a></li>
                </ul>
            </div>
        </div>

        <div class="container-fluid sidebar-offset">
            <div class="row-fluid">

                <div class="span10">
                    %for a in range(0, 50):
                        {{data}} <p />
                    %end
                </div>
            </div>
        </div>
    </body>

</html>
