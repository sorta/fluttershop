
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
                                <h2 class="inl">{{ post['title'] }}</h2>
                            %end

                            %if post['show_date']:
                                <em class="pull-right fawn">Posted: {{ post['date_created'].strftime('%B %d, %Y %H:%M %Z %x %X') }}</em>
                            %end

                            %if logged_in:
                                <a class="pull-right" href="#edit_post_form" onclick='setEditPost("edit", "{{ post["_id"] }}", {{ dumps(post["title"]) }}, {{ dumps(post["post_content"]) }}, {{ dumps(post["show_title"]) }}, {{ dumps(post["show_date"]) }}, {{ post["rank"] }}, "{{ post["alignment"] }}", {{ post["width"] }});'><i class="icon-edit"></i></a>
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
        </div>
    %end
    </div>
%end
