
%for row in rows:
    <div class="row-fluid">
    %for post in row:
        %if post['offset'] > 0:
            <div class="span{{ post['offset'] }}"><br /></div>
        %end
        <div class="span{{ post['width'] }}">
            <h1>{{ post['title'] }}</h1>
            <em>{{ post['date'].strftime('%B %d, %Y %H:%M %Z %x %X') }}</em>
            %for part in post['parts']:
                <p>{{ part['body'] }}</p>
            %end
        </div>
    %end
    </div>
%end
