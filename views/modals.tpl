
<!-- MODALS -->
<div class="modal hide fade" id="login_modal">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">×</button>
        <h3>Please Login</h3>
    </div>
    <div class="modal-body">
        <form action="/_sitefuncs_/login" class="form-vertical" id="loginForm" method="post">
            <input name="selected_url" type="hidden" value="{{ selected_route }}" />
            <label>User</label>
            <input id="login_username" name="login_username" type="text" class="span3 offset2" placeholder="Username" />
            <label>Password</label>
            <input id="login_pass" name="login_pass" type="password" class="span3 offset2" placeholder="Password" />
    </div>
    <div class="modal-footer">
            <button type="button" class="btn" data-dismiss="modal">Close</button>
            <input class="btn btn-primary" type="submit" value="Login" />
        </form>
    </div>
</div>

%if logged_in:

    <div class="modal hide fade" id="logout_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Logout</h3>
        </div>
        <div class="modal-body">

            <form action="/_sitefuncs_/logout" method="post" id="logoutForm">
                <label>Are you sure you want to log out?</label>
                <input name="selected_url" type="hidden" value="{{ selected_route }}" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-primary" type="submit" value="Log Out" />
            </form>
        </div>
    </div>

    <div class="modal hide fade" id="site_options_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Site Options</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/options" class="form-vertical" id="siteOptionsForm" method="post">
                <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                <input name="current_username" type="hidden" value="{{ user.get('username', 'User') }}" />
                <input name="current_email" type="hidden" value="{{ user.get('email', 'user@sortasoftware.com') }}" />
                <input name="current_site_name" type="hidden" value="{{ site_name }}" />

                <label>Username</label>
                <input name="new_username" type="text" class="span3" value="{{ user.get('username', 'User') }}" />

                <label>Email</label>
                <input name="new_email" type="text" class="span3" value="{{ user.get('email', 'example@email.com') }}" />

                <label>Site Name</label>
                <input name="new_site_name" type="text" class="span3" value="{{ site_name }}" />
        </div>
        <div class="modal-footer">
                <div class="pull-left">Password<input name="current_password" type="password" class="span3" /></div>
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-primary" type="submit" value="Save" />
            </form>
        </div>
    </div>

    <div class="modal hide fade" id="passchange_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Change Password</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/changepassword" class="form-vertical" id="passChangeForm" method="post">

                <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                <input name="current_username" type="hidden" value="{{ user.get('username', 'User') }}" />

                <label>New Password</label>
                <input name="new_pass" type="password" class="span3"/>

                <label>Confirm New Password</label>
                <input name="confirm_new_pass" type="password" class="span3"/>
        </div>
        <div class="modal-footer">
                <div class="pull-left">Current Password<input name="current_password" type="password" class="span3" /></div>
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-danger" type="submit" value="Change Password" />
            </form>
        </div>
    </div>

    <div class="modal hide fade" id="add_mane_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Add Mane Tab</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/addmane" class="form-vertical" id="addMane" method="post">
                <input name="selected_url" type="hidden" value="{{ selected_route }}" />

                <label>Name</label>
                <input name="mane_name" type="text" class="span3" placeholder="Tab" />
                <label>Title</label>
                <input name="mane_title" type="text" class="span3" placeholder="Tab" />
                <label>Description</label>
                <input name="mane_desc" type="textarea" class="span3" placeholder="Tab" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-primary" type="submit" value="Add" />
            </form>
        </div>
    </div>

    <div class="modal hide fade" id="add_tail_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Add Tail Tab</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/addtail" class="form-vertical" id="addTail" method="post">
                <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                <input name="selected_mane" type="hidden" value="{{ selected_mane }}" />

                <label>Name</label>
                <input name="tail_name" type="text" class="span3" placeholder="Tab" />
                <label>Title</label>
                <input name="tail_title" type="text" class="span3" placeholder="Tab" />
                <label>Description</label>
                <input name="tail_desc" type="textarea" class="span3" placeholder="Tab" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-primary" type="submit" value="Add" />
            </form>
        </div>
    </div>

    %for link in manelinks:

        <div class="modal hide fade" id="delete_mane_modal_{{ link['mane_name'] }}">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">×</button>
                <h3>Delete Mane Tab</h3>
            </div>
            <div class="modal-body">
                <form action="/_sitefuncs_/deletemane" class="form-vertical" method="post">
                    <label>Are you sure you want to delete this Mane Tab ({{ link['mane_name'] }})?</label>
                    <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                    <input name="mane_name" type="hidden" value="{{ link['mane_name'] }}" />
            </div>
            <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal">Close</button>
                    <input class="btn btn-danger" type="submit" value="DESTROY!" />
                </form>
            </div>
        </div>

    %end

    %for link in taillinks:

        <div class="modal hide fade" id="delete_tail_modal_{{ link['tail_name'] }}">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">×</button>
                <h3>Delete Tail Tab</h3>
            </div>
            <div class="modal-body">
                <form action="/_sitefuncs_/deletetail" class="form-vertical" method="post">
                    <label>Are you sure you want to delete this Tail Tab ({{ link['tail_name'] }})?</label>
                    <input name="selected_url" type="hidden" value="{{ selected_route }}" />
                    <input name="mane_name" type="hidden" value="{{ link['mane_name'] }}" />
                    <input name="tail_name" type="hidden" value="{{ link['tail_name'] }}" />
            </div>
            <div class="modal-footer">
                    <button type="button" class="btn" data-dismiss="modal">Close</button>
                    <input class="btn btn-danger" type="submit" value="HULK SMASH!" />
                </form>
            </div>
        </div>

    %end
%end
