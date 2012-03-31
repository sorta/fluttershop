
<!-- MODALS -->
<div class="modal hide fade" id="login_modal">
    <div class="modal-header">
        <a class="close" data-dismiss="modal">×</a>
        <h3>Please Login</h3>
    </div>
    <div class="modal-body">
        <form action="/login" class="form-vertical" id="loginForm" method="post">
            <input name="selected_url" type="hidden" value="{{ selected_route }}" />
            <label>User</label>
            <input id="login_username" name="login_username" type="text" class="span3 offset2" placeholder="Username" />
            <label>Password</label>
            <input id="login_pass" name="login_pass" type="password" class="span3 offset2" placeholder="Password" />
    </div>
    <div class="modal-footer">
            <a class="btn" data-dismiss="modal">Close</a>
            <input class="btn btn-primary" type="submit" value="Login" />
        </form>
    </div>
</div>

<div class="modal hide fade" id="add_mane_modal">
    <div class="modal-header">
        <a class="close" data-dismiss="modal">×</a>
        <h3>Add Mane Tab</h3>
    </div>
    <div class="modal-body">
        <form action="/addmane" class="form-vertical" id="addMane" method="post">
            <input name="selected_url" type="hidden" value="{{ selected_route }}" />

            <label>Name</label>
            <input name="mane_name" type="text" class="span3" placeholder="Tab" />
            <label>Title</label>
            <input name="mane_title" type="text" class="span3" placeholder="Tab" />
            <label>Description</label>
            <input name="mane_desc" type="textarea" class="span3" placeholder="Tab" />
    </div>
    <div class="modal-footer">
            <a class="btn" data-dismiss="modal">Close</a>
            <input class="btn btn-primary" type="submit" value="Add" />
        </form>
    </div>
</div>

