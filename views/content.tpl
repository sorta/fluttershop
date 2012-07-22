
%for row in rows:
    <div class="row-fluid">
    %for post in row:
        %if post['offset'] > 0:
            <div class="span{{ post['offset'] }}"><br /></div>
        %end
        <div class="span{{ post['width'] }}">
            <table class="table table-bordered">
                %if post['show_title'] or post['show_date']:
                <thead>
                    <tr>
                        <th>
                            %if post['show_title']:
                                <h2 style="display:inline;">{{ post['title'] }}</h2>
                            %end

                            %if post['show_date']:
                                <em class="pull-right" style="font-weight: normal;">Posted: {{ post['date_created'].strftime('%B %d, %Y %H:%M %Z %x %X') }}</em>
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
