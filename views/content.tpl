
%for row in rows:
    <div class="row-fluid">
    %for post in row:
        %if post['offset'] > 0:
            <div class="span{{ post['offset'] }}"><br /></div>
        %end
        <div class="span{{ post['width'] }}">
            <table class="table table-bordered table-striped">
                <tbody>
                    %if post['show_title'] or post['show_date']:
                    <tr>
                        <td>
                            %if post['show_title']:
                                <h2 style="display:inline;">{{ post['title'] }}</h2>
                            %end

                            %if post['show_date']:
                                <em class="pull-right"> Posted: {{ post['date_created'].strftime('%B %d, %Y %H:%M %Z %x %X') }}</em>
                            %end
                        </td>
                    </tr>
                    %end
                    <tr>
                        <td>
                            %for part in post['parts']:
                                <p>{{ part['body'] }}</p>
                            %end
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    %end
    </div>
%end
