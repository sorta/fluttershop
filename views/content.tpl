
%for row in rows:
    <div class="row-fluid">
    %for post in row:
        %if post['offset'] > 0:
            <div class="span{{ post['offset'] }}"><br /></div>
        %end
        <div class="span{{ post['width'] }}">
            <table class="table table-bordered table-striped">
                <tbody>
                    <tr>
                        <td>
                            <h1 style="display:inline;">{{ post['title'] }}</h1>
                            <em> Posted: {{ post['date'].strftime('%B %d, %Y %H:%M %Z %x %X') }}</em>
                        </td>
                    </tr>
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
