<%inherit file="layout.mako"/>

<%def name="title()">
   Profile
</%def>

<%def name="meta_keywords()">
    Profile, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Profile page for fantasy dota game.
</%def>

<div>
    <h5>Profile: ${shown_user.username}</h5>
    <div class="row">
        <div class="col s3">
            <div class="card-panel">
                <p><strong>ePenis Size:</strong> ${user_xp.level or '-'}" inches</p>
                <p><strong>Xp:</strong> ${user_xp.xp}
                <p><strong>Highest Weekly:</strong> ${user_xp.highest_weekly_pos or '-'}
                <p><strong>Highest Daily:</strong> ${user_xp.highest_daily_pos or '-'}
                <p><strong>All time points:</strong> ${user_xp.all_time_points}
            </div>
        </div>
        <div class="col s5 card-panel">
            <div class="row achievementBlock">
            % for i, achievement in enumerate(achievements):
                <div class="col s3">
                <div class="card-image center pointerCursor">
                    % if achievement.id in user_achievements:
                    <img src="/static/images/dota/achievements/${achievement.id}.png" title="${achievement.description}"/>
                    <span class="card-title" title="${achievement.description}">
                        <i class="material-icons">info</i>${achievement.name}<i class="material-icons awardIcon">stars</i>
                    </span>
                    % else:
                    <img class="banIcon" src="/static/images/dota/achievements/${achievement.id}.png" title="${achievement.description}"/>
                    <span class="card-title" title="${achievement.description}">
                        <i class="material-icons">info</i>${achievement.name}</span>
                    % endif
                </div>
                </div>
                % if (i + 1) % 4 == 0:
                    </div>
                    <div class="row">
                % endif
            % endfor
            </div>
        </div>
    </div>
</div>

<script>
    $(".pointerCursor").each(function(){
        var elem = $(this);
        elem.click(function() {
            swal(elem.find('img').attr('title'), '', 'info')
        })
    });
</script>