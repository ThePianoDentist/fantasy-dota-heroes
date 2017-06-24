<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboard: ${league.name}
</%def>

<%def name="meta_keywords()">
    Leaderboard, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Leaderboard page for fantasy dota game.
</%def>

<%def name="rank_by_fn(x, player, for_user)">
    % if x == "points":
        % if for_user:
            ${player.points_rank}
        % else:
            <% rounded_points = round(player.points, 1) %>
            ${int(rounded_points) if rounded_points.is_integer() else rounded_points}
        % endif
    % elif x == "wins":
        % if for_user:
            ${player.wins_rank}
        % else:
            ${player.wins}
        % endif
    % elif x == "picks":
        % if for_user:
            ${player.picks_rank}
        % else:
            ${player.picks}
        % endif
    % elif x == "bans":
        % if for_user:
            ${player.bans_rank}
        % else:
            ${player.bans}
        % endif
    % endif
</%def>

<%def name="friendOrGlobal(switch_to)">
${"showGlobal=kek" if switch_to == "friend" else "showFriend=kek"}
</%def>

<%def name="getTime(period)">
${"period=%s" % period}
</%def>

<%def name="progress_arrow(i, player, x)">
    % if x == "points":
        <% old = player.old_points_rank %>
    % elif x == "wins":
        <% old = player.old_wins_rank %>
    % elif x == "picks":
        <% old = player.old_picks_rank %>
    % elif x == "bans":
        <% old = player.old_bans_rank %>
    % endif
    % if old:
        <% diff = i + 1 - old %>
        % if diff == 0:
            <span>&#8660;</span>
        % elif diff < -5:
            <span class="upMyArrow">&#8657;</span>
        % elif diff > 5:
            <span class="downMyArrow">&#8659;</span>
        % elif diff < 0:
            <span class="supMyArrow">&#8663;</span>
        % else:
            <span class="sdownMyArrow">&#8664;</span>
        % endif
    % endif
</%def>

<div class="row">
    <h2>${rank_by.title()} (${period.title() if period == "tournament" else "Day %d" % (int(period) + 1)})
        <a class="right" href="${league.url}" target="_blank">${league.name}</a></h2>
</div>
<div class="row">
<div id="leaderboardBlock" class="col s7">
    <nav>
    <div class="nav-wrapper teal darken-2">
        <ul class="left">
            <li class=${"active" if rank_by=="points" else ""}>
                <a id="pointsBtn" href="/daily?rank_by=points&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Points
                </a>
            </li>
            <li class=${"active" if rank_by=="wins" else ""}>
                <a id="winsBtn" href="/daily?rank_by=wins&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Wins
                </a>
            </li>
            <li class=${"active" if rank_by=="picks" else ""}>
                <a id="picksBtn" href="/daily?rank_by=picks&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Picks
                </a>
            </li>
            <li class=${"active" if rank_by=="bans" else ""}>
                <a id="bansBtn" href="/daily?rank_by=bans&${friendOrGlobal(switch_to)}&${getTime(period)}">
                    Bans
                </a>
            </li>
            <li><a id="friendsGlobalBtn" href="/daily?rank_by=${rank_by}&${"showFriend=kek" if switch_to == "friend" else "showGlobal=kek"}&${getTime(period)}">
                ${switch_to.title()}
                </a>
            </li>
            <li>
                <a class="dropdown-button" data-beloworigin="true" href="" data-activates="periodDropdown">Period<i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
                <li><a href="/leaderboard?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=tournament">Tournament</a></li>
                <li class="divider"></li>
                % for i in range(league.current_day + 1):
                    <li><a href="/daily?rank_by=${rank_by}&${friendOrGlobal(switch_to)}&period=${i}">Day ${i+1}</a></li>
                % endfor
            </ul>
        </ul>
    </div>
    </nav>

    <div id="tableContainer">
        <table id="leaderboardTable" class="card-table striped centered">
            <tr>
                <th class="positionHeader">Position</th>
                <th class="playerHeader">Player</th>
                <th class="rankingHeader">${rank_by.title()}</th>
            </tr>
            % for i, player in enumerate(players):
                <tr class=${"playerRow" if not user or player.username != user.username else "userRow"}>
                    <td class="positionEntry">${i+1} ${progress_arrow(i, player, rank_by) if period == "tournament" else ""}
                    </td>
                    <td class="heroEntry">
                        % if player.username == "seni":
                        <img src="/static/images/trophy.png"/>
                        % endif
                        ${player.username}
                    %if len(player_heroes) > i and not league.transfer_open:
                        <span class="hero_images">
                        % for hero in player_heroes[i]:
                            <img src="/static/images/${hero.replace(" ", "_")}_icon.png" title="${hero}" />
                        % endfor
                        </span>
                    %endif
                    </td>
                    <td class="rankingEntry">${rank_by_fn(rank_by, player, False)}</td>
                </tr>
            % endfor
            % if user and switch_to == "friend":
            <tr class="userRow outsideRanks">
                <td class="userRank">${rank_by_fn(rank_by, user, True)}</td>
                <td class="heroEntry">${user.username}</td>
                <td class="rankingEntry">${rank_by_fn(rank_by, user, False)}</td>
            </tr>
            % endif
        </table>
    </div>
</div>

<script>
$( document ).ready(function() {
    console.log("ready");
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });

    /*$.getJSON("/matches", {"day": ${period}}).done(
        function( data ){

        }
    )*/
})
</script>
<div id="matchesBlock" class="col s5">
    <div class="card">
    <div class="card-content" id="matchesCard">
        <h2>Matches</h2>
        % for match in match_data:
        <div class="section">
        <div class="row">
            <!--<img src="/static/images/trophy.png" class=${"hide" if not match["radiant_win"] else ""} />-->
            <span class="radiantTeam">
                % if match["radiant_win"]:
                <strong>${match["radiant"]}</strong>
                % else:
                ${match["radiant"]}
                % endif
            </span>
            <span class="direTeam right">
                % if not match["radiant_win"]:
                <strong>${match["dire"]}</strong>
                % else:
                ${match["dire"]}
                % endif
            </span>
        </div>
        <div class="row" style="margin-bottom: 0px">
            <div class="left">
                % for hero in match["radiant_picks"]:
                    <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                        ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                    </span>
                % endfor
            </div>
            <div class="right">
                % for hero in match["dire_picks"]:
                    <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                        ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                    </span>
                % endfor
            </div>
        </div>
        <div class="row">
            <div class="left">
                % for hero in match["radiant_picks"]:
                    <img src="/static/images/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}" />
                % endfor
            </div>
            <div class="right">
                % for hero in match["dire_picks"]:
                    <img src="/static/images/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}"/>
                % endfor
            </div>
        </div>
        <div class="row" style="margin-bottom: 0px">
            <div class="left">
                % for hero in match["radiant_bans"]:
                    <img src="/static/images/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}" style="filter: grayscale(100%)"/>
                % endfor
            </div>
            <div class="right">
                % for hero in match["dire_bans"]:
                    <img src="/static/images/${hero['hero'].replace(' ', '_')}_icon.png" title="${hero['hero']}" style="filter: grayscale(100%)"/>
                % endfor
            </div>
        </div>
        <div class="row">
            <div class="left">
                % for hero in match["radiant_bans"]:
                    <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                        ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                    </span>
                % endfor
            </div>
            <div class="right">
                % for hero in match["dire_bans"]:
                    <span class="${'positive' if hero['points'] >= 0 else 'negative'}" style="display: inline-block; width: 32px; text-align: center;">
                        ${'+' if hero["points"] >= 0 else '-'}${hero["points"]}
                    </span>
                % endfor
            </div>
        </div>
        </div>
        <div class="divider"></div>
        % endfor

    </div>
    </div>
</div>
</div>
