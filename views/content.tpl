
%for row in rows:
    <div class="row">
    %for post in row:
        %if post['offset'] > 0:
            <div class="span{{ post['offset'] }}"><br /></div>
        %end
        <div class="span{{ post['width'] }}">
            <table class="table table-bordered">
                %if post['show_title'] or post['show_date'] or logged_in:
                <thead>
                    <tr>
                        <th>
                            %if post['show_title']:
                                <h2 style="display:inline;">{{ post['title'] }}</h2>
                            %end

                            %if post['show_date']:
                                <em class="pull-right" style="font-weight: normal;">Posted: {{ post['date_created'].strftime('%B %d, %Y %H:%M %Z %x %X') }}</em>
                            %end

                            %if logged_in:
                                <a style="float: right;" href="#" data-toggle="collapse" data-target="#edit_post_{{ post['post_id'] }}"><i class="icon-edit"></i></a>
                            %end
                        </th>
                    </tr>
                </thead>
                %end
                <tbody>
                    <tr>
                        <td>
                            {{! post['post_content'] }}
                        </td>
                    </tr>
                </tbody>
            </table>

            %if logged_in:
                %st_class = ""
                %sd_class = ""
                %if post['show_title']:
                    %st_class = "active"
                %end
                %if post['show_date']:
                    %sd_class = "active"
                %end

                <div class="collapse fakeTable" id="edit_post_{{ post['post_id'] }}">
                    <div>
                        <h3>Edit Post</h3>
                        <form class="form-vertical" action="/_sitefuncs_/editpost" method="post">
                            <input name="selected_tab" type="hidden" value="{{ selected_tab['_id'] }}" />
                            <input name="post_id" type="hidden" value="{{ post['post_id'] }}" />

                            <label>Title</label>
                            <input name="post_title" type="text" class="span12" placeholder="Post something..." value="{{ post['title'] }}"></input>

                            <label>Post Content*</label>
                            <textarea name="post_content" class="span12 red_tb">{{! post['post_content'] }}</textarea>

                            <div class="row-fluid">
                                <div class="span2">
                                    <label>Show</label>
                                    <div class="btn-group" data-toggle="buttons-checkbox">
                                        <button type="button" id="pstb_{{ post['post_id'] }}" class="btn hidden_flipper {{ st_class }}">Title</button>
                                        <button type="button" id="psdb_{{ post['post_id'] }}" class="btn hidden_flipper {{ sd_class }}">Date</button>
                                    </div>
                                    <input type="checkbox" id="pstb_{{ post['post_id'] }}_c" class="hide" name="post_show_title"
                                        %if post['show_title']:
                                            checked="true"
                                        %end
                                        />
                                    <input type="checkbox" id="psdb_{{ post['post_id'] }}_c" class="hide" name="post_show_date"
                                        %if post['show_date']:
                                            checked="true"
                                        %end
                                        />
                                </div>

                                <div class="span3">
                                    <label>Rank</label>
                                    <input name="post_rank" type="text" class="span12" value="{{ post['rank'] }}" ></input>
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
                                <button style="display: inline; margin-bottom: 10px;" type="submit" class="btn btn-primary pull-right"><i class="icon-edit"></i>Save</Button>
                            </div>
                        </form>
                    </div>
                </div>
            %end
        </div>
    %end
    </div>
%end
