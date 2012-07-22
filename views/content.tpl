
%for row in rows:
    <div class="row-fluid">
    %for post in row:
        %if post['offset'] > 0:
            <div class="span{{ post['offset'] }}"><br /></div>
        %end
        <div class="span{{ post['width'] }}">
            <table class="table table-bordered table-striped">
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
                    %for part in post['parts']:
                        <tr>
                            <td>
                                <p>{{! part['body'] }}</p>
                                <div class="row-fluid">

                                    %if part["part_type"] == "pic":
                                        </tr></td><tr><td>
                                        <div class="span3"></div>
                                        <div class="span6">
                                            <ul class="thumbnails">
                                                <li>
                                                    <div class="thumbnail" style="text-align: center;">
                                                        <a href="{{ part['url'] }}"><img src="{{ part['url'] }}" alt="{{ part['alt_text'] }}" title="{{ part['alt_text'] }}" /></a>
                                                        <em>{{ part['caption'] }}</em>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    %elif part["part_type"] == "lnk":
                                        </tr></td><tr><td>
                                        <div style="text-align: center;">
                                            <a href="{{ part['url'] }}" title="{{ part['alt_text'] }}">{{ part['caption'] }}</a>
                                        </div>
                                    %elif part["part_type"] == "vid":
                                        </tr></td><tr><td>
                                        <div class="span2"></div>
                                        <div class="span10">
                                            <ul class="thumbnails">
                                                <li>
                                                    <iframe width="560" height="315" src="http://www.youtube.com/embed/{{ part.get('yt_id', 'FAIL') }}" frameborder="0" allowfullscreen></iframe>
                                                    <div class="thumbnail" style="text-align: center;">
                                                        <em>{{ part['caption'] }}</em>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    %end
                                </div>
                            </td>
                        </tr>
                    %end
                </tbody>
            </table>
        </div>
    %end
    </div>
%end
