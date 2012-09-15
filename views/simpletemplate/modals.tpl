
<!-- Login -->
<div class="modal hide fade" id="login_modal">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">×</button>
        <h3>Please Login</h3>
    </div>
    <div class="modal-body">
        <form action="/_sitefuncs_/login" class="form-vertical" id="loginForm" method="post">
            <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
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

    <!-- Logout -->
    <div class="modal hide fade" id="logout_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Logout</h3>
        </div>
        <div class="modal-body">

            <form action="/_sitefuncs_/logout" method="post" id="logoutForm">
                <label>Are you sure you want to log out?</label>
            <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-primary" type="submit" value="Log Out" />
            </form>
        </div>
    </div>

    <!-- Settings -->
    <div class="modal hide fade" id="site_options_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Site Options</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/options" class="form-vertical" id="siteOptionsForm" method="post">
                <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                <input name="current_username" type="hidden" value="{{ user.get('username', 'User') }}" />
                <input name="current_email" type="hidden" value="{{ user.get('email', 'user@sortasoftware.com') }}" />

                <label>Username</label>
                <input name="new_username" type="text" class="span3" value="{{ user.get('username', 'User') }}" />

                <label>Email</label>
                <input name="new_email" type="text" class="span3" value="{{ user.get('email', 'example@email.com') }}" />

                <label>Site Name</label>
                <input name="new_site_name" type="text" class="span3" value="{{ site_name }}" />

                <label>Default Posts Per Page</label>
                <input name="default_posts_per_page" type="text" class="span3" value="{{ def_ppp['def_ppp'] }}" />
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

                <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                <input name="current_username" type="hidden" value="{{ user.get('username', 'User') }}" />

                <label>New Password</label>
                <input name="new_password" type="password" class="span3"/>

                <label>Confirm New Password</label>
                <input name="confirm_new_password" type="password" class="span3"/>
        </div>
        <div class="modal-footer">
                <div class="pull-left">Current Password<input name="current_password" type="password" class="span3" /></div>
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-danger" type="submit" value="Change Password" />
            </form>
        </div>
    </div>

    <!-- Add/Edit Tab -->
    <div class="modal hide fade" id="edit_tab_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3><span id="tab_action" class="action_span">add</span> Tab</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/edittab" class="form-vertical" id="editTab" method="post">
                <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                <input name="action" id="edit_tab_action" type="hidden" value="add" />
                <input name="tab_parent" id="edit_tab_parent" type="hidden" value="" />
                <input name="tab_id" id="edit_tab_id" type="hidden" value="" />

                <label>Name*</label>
                <input name="tab_name" id="edit_tab_name" type="text" class="span5" placeholder="Name" />
                <label>Rank*</label>
                <input name="tab_rank" id="edit_tab_rank" type="text" class="span5" value="" />
                <label>Title</label>
                <input name="tab_title" id="edit_tab_title" type="text" class="span5" placeholder="Quick basic description" />
                <label>Description</label>
                <textarea name="tab_desc" id="edit_tab_desc" class="span5" placeholder="Detailed description"></textarea>
                <label>Posts Per Page*</label>
                <input name="tab_ppp" id="edit_tab_ppp" type="text" class="span5" value="" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-primary" type="submit" value="Save" />
            </form>
        </div>
    </div>

    <!-- Delete Tab -->
    <div class="modal hide fade" id="delete_tab_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Delete Tab</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/deletetab" class="form-vertical" method="post">
                <label>Are you sure you want to delete this Tab (<span id="delete_tab_label"></span>)?</label>
                <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                <input name="tab_id" id="delete_tab_id" type="hidden" value="" />
                <input name="tab_name" id="delete_tab_name" type="hidden" value="" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-danger" type="submit" value="DESTROY!" />
            </form>
        </div>
    </div>

    <!-- Delete Post -->
    <div class="modal hide fade" id="delete_post_modal">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">×</button>
            <h3>Delete Post</h3>
        </div>
        <div class="modal-body">
            <form action="/_sitefuncs_/deletepost" class="form-vertical" method="post">
                <label>Are you sure you want to delete this Post (<span id="delete_post_label"></span>)?</label>
                <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                <input name="post_id" id="delete_post_id" type="hidden" value="" />
        </div>
        <div class="modal-footer">
                <button type="button" class="btn" data-dismiss="modal">Close</button>
                <input class="btn btn-danger" type="submit" value="HULK SMASH!" />
            </form>
        </div>
    </div>
%end
