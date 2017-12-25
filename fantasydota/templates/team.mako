<%inherit file="layout.mako"/>

<%def name="title()">
    League Team: ${league.name}
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy dota game.
</%def>

% if game.code == 'DOTA':
    <div class="row" id="myTeamBlock">
    <span class="left"><h2>Team (Credits: <span class="userCredits">${round(userq.money, 1)}</span>)</h2></span>
    <span class="right"><h2>Points: <span class="teamPoints">${userq.points}</span></h2></span>
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader extra">Picks</th>
                <th class="bansHeader extra">Bans</th>
                <th class="winsHeader extra">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">${"Sell" if transfer_open else "Swap"}</th>

            </tr>
            % for hero in team:
                <tr class="teamRow ${'toSwap' if not hero[1].active and not transfer_open else ''}" id="${hero[0].id}TeamRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/dota/${hero[0].name.replace(" ", "_")}_icon.png" title="${hero[0].name}"/></td>
                    <td class="heroEntry">${'=> ' if not hero[1].active and not transfer_open else ''}${hero[0].name}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry extra">${hero[0].picks}</td>
                    <td class="bansEntry extra">${hero[0].bans}</td>
                    <td class="winsEntry extra">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <input type="hidden" value="0" name="tradeReserve"/>
                            <button type="submit" name=${"sellHero" if transfer_open else "swapOutHero"} class="btn waves-effect waves-light">${"Sell" if transfer_open else "Swap"}</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>

<div class="row" id="myReserveBlock">
    % if transfer_open:
        <span class="left"><h2>Reserves (Credits: <span class="userReserveCredits">${round(userq.reserve_money, 1)}</span>)</h2></span>
        % if userq.late_start == 1:
            <span class="right"><button type="submit" id="confirmTransfers" class="btn waves-effect waves-light">Confirm Team!</button></span>
        % endif
    % else:
        <span class="left"><h2>Reserves</h2></span>
        <span class="right"><button type="submit" id="confirmSwaps" class="btn waves-effect waves-light">Confirm Swaps!</button></span>
    % endif
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="reserveTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader extra">Picks</th>
                <th class="bansHeader extra">Bans</th>
                <th class="winsHeader extra">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">${"Sell" if transfer_open else "Swap"}</th>
            </tr>
            % for hero in reserve_team:
                <tr class="reserveRow ${'toSwap' if hero[1].active and not transfer_open else ''}" id="${hero[0].id}ReserveRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/dota/${hero[0].name.replace(" ", "_")}_icon.png" title="${hero[0].name}"/></td>
                    <td class="heroEntry">${'<= ' if hero[1].active and not transfer_open else ''}${hero[0].name}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="picksEntry extra">${hero[0].picks}</td>
                    <td class="bansEntry extra">${hero[0].bans}</td>
                    <td class="winsEntry extra">${hero[0].wins}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <input type="hidden" value="1" name="tradeReserve"/>
                            <button type="submit" name=${"sellHero" if transfer_open else "swapInHero"} class="btn waves-effect waves-light">${"Sell" if transfer_open else "Swap"}</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>

<div class="card row">
    <div class="card-content">
        % if transfer_open:
            <p>50 Credits to pick Main team of 5 heroes (Points penalties for under 5). 40 credits for up to 4 Reserves</strong>
        <p><strong>Reserves score 0 points</strong>. However they can be swapped with main heroes any time during the week</p>
            % if userq.late_start:
                <span class="messageTransClosed">
                    <strong><p>Transfer window closed for this week</p></strong>
                </span>
                <span>
                    <p>You may still build a team and compete this week</p>
                    <p>But it will not earn achievements, full-XP, or main leaderboard positions</p>
                    <p>Transfer window for <a href="/team?league=${league.id + 1}">next week</a> is already open</p>
                </span>
            % else:
                <span class="messageTransOpen">
                    <p>Transfer window currently open</p>
                </span>
                <p>It closes Monday 6AM GMT when week becomes active and points start being earned</p>
            % endif
        % else:
            % if not userq.swap_tstamp:
                <p><strong>
                    There is a 12 hour delay between confirmation of swaps and their processing.
                </strong></p>
                <p>Further swaps are disabled during this 12 hour period</p>
            % else:
                <span class="messageTransClosed"><p><strong>
                    Due to recent changes you are in swap cooldown for ${int(time_until_swap[0])} hours, ${int(time_until_swap[1])} minutes.
                </strong></p></span>
            % endif
        % endif
        <p><strong><a href="/rules">Detailed Rules</a></strong></p>
        <span>
            <p>Tables are sortable (click table headers)</p>
        </span>
    </div>
</div>
<div id="heroesBlock" class="row">
    % if transfer_open:
        <h2>Heroes (Credits Available: <span class="userCredits">${round(userq.money, 1)}</span>, Reserve Credits: <span class="userReserveCredits">${round(userq.reserve_money, 1)}</span>)</h2>
    % else:
        <h2>Heroes</h2>
    % endif
    <div id="tableContainer">
        <table class="sortable card-table striped centered">
            <tr style="cursor: pointer">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader">Points</th>
                <th class="picksHeader extra">Picks</th>
                <th class="bansHeader extra">Bans</th>
                <th class="winsHeader extra">Wins</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">Buy</th>
                <th class="sellHeader">Reserve</th>
            </tr>
            % for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroImg" sorttable_customkey="${hero.name}"><img src="/static/images/dota/${hero.name.replace(" ", "_")}_icon.png" title="${hero.name}"/></td>
                    <td class="heroEntry">${hero.name}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="picksEntry extra">${hero.picks}</td>
                    <td class="bansEntry extra">${hero.bans}</td>
                    <td class="winsEntry extra">${hero.wins}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <input type="hidden" value="0" name="tradeReserve"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Buy</button>
                        </form>
                    </td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <input type="hidden" value="1" name="tradeReserve"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Res</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
% elif game.code == 'PUBG':
    <div class="row" id="myTeamBlock">
    <span class="left"><h2>Team (Credits: <span class="userCredits">${round(userq.money, 1)}</span>)</h2></span>
    <span class="right"><h2>Points: <span class="teamPoints">${userq.points}</span></h2></span>
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">${game.pickee}</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="teamHeader">Team</th>
                <th class="heroPointsHeader">Points</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">${"Sell" if transfer_open else "Swap"}</th>

            </tr>
            % for hero in team:
                <tr class="teamRow" id="${hero[0].id}TeamRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/pubg/teams/${hero[0].team.replace(" ", "_")}_icon.png" title="${hero[0].team}"/></td>
                    <td class="heroEntry">${hero[0].name}</td>
                    <td class="teamEntry">${hero[0].team}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <input type="hidden" value="0" name="tradeReserve"/>
                            <button type="submit" name=${"sellHero" if transfer_open else "swapOutHero"} class="btn waves-effect waves-light">${"Sell" if transfer_open else "Swap"}</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>

<div class="row" id="myReserveBlock">
    % if transfer_open:
        <span class="left"><h2>Reserves (Credits: <span class="userReserveCredits">${round(userq.reserve_money, 1)}</span>)</h2></span>
    % else:
        <span class="left"><h2>Reserves</h2></span>
    % endif
    <div id="tableContainer">
        <table class="sortable card-table striped centered" id="reserveTable">
            <tr style="cursor: pointer">
                <th class="heroHeader">${game.pickee}</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="teamHeader">Team</th>
                <th class="heroPointsHeader">Points</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">${"Sell" if transfer_open else "Swap"}</th>
            </tr>
            % for hero in reserve_team:
                <tr class="reserveRow" id="${hero[0].id}ReserveRow">
                    <td class="heroImg" sorttable_customkey="${hero[0].name}"><img src="/static/images/pubg/teams/${hero[0].team.replace(" ", "_")}_icon.png" title="${hero[0].team}"/></td>
                    <td class="heroEntry">${hero[0].name}</td>
                    <td class="teamEntry">${hero[0].team}</td>
                    <td class="heroPointsEntry">${hero[0].points}</td>
                    <td class="valueEntry">${hero[0].value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero[0].id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero[0].id}" name="tradeHero"/>
                            <input type="hidden" value="1" name="tradeReserve"/>
                            <button type="submit" name=${"sellHero" if transfer_open else "swapInHero"} class="btn waves-effect waves-light">${"Sell" if transfer_open else "Swap"}</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>

<div class="card row">
    <div class="card-content">
        <p>Your team consists of ${game.team_size} players</p>
        <p>Only allowed <strong>one player from each team</strong></p>
        <p>Detailed rules <a href="/rules">here</a></p>
        <span class=${"messageTransOpen" if transfer_open else "messageTransClosed"}>
            % if transfer_open:
            </br><p><strong>Transfer window currently open (closes ~1 hour before games start)</strong></p>
            % else:
                <p><strong>
                Swaps between reserves and main team only available between days. When all day's games finished
                </strong></p>
            % endif
        </span>
		<p>This is independently run by me, no offiliation with either IEM Oakland</p><p>If there are bugs/problems it is my 100% fault and no reflection on IEM</p>
        <span></br>
            <p>Tables are sortable (click table headers)</p>
        </span>
    </div>
</div>
<div id="heroesBlock" class="row">
    % if transfer_open:
        <h2>${game.pickee}s (Credits Available: <span class="userCredits">${round(userq.money, 1)}</span>, Reserve Credits: <span class="userReserveCredits">${round(userq.reserve_money, 1)}</span>)</h2>
    % else:
        <h2>${game.pickee}s</h2>
    % endif
    <div id="tableContainer">
        <table class="sortable card-table striped centered">
            <tr style="cursor: pointer">
                <th class="heroHeader">${game.pickee}</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="teamHeader">Team</th>
                <th class="heroPointsHeader">Points</th>
                <th class="valueHeader">Value</th>
                <th class="sellHeader">Buy</th>
                <th class="sellHeader">Reserve</th>
            </tr>
            % for hero in heroes:
                <tr id="${hero.id}Row">
                    <td class="heroImg" sorttable_customkey="${hero.name}"><img src="/static/images/pubg/teams/${hero.team.replace(" ", "_")}_icon.png" title="${hero.team}"/></td>
                    <td class="heroEntry">${hero.name}</td>
                    <td class="teamEntry">${hero.team}</td>
                    <td class="heroPointsEntry">${hero.points}</td>
                    <td class="valueEntry">${hero.value}</td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <input type="hidden" value="0" name="tradeReserve"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Buy</button>
                        </form>
                    </td>
                    <td class="tradeEntry">
                        <form name="tradeForm" id="${hero.id}TradeForm" class="tradeForm" onsubmit="return false;">
                            <input type="hidden" value="${hero.id}" name="tradeHero"/>
                            <input type="hidden" value="1" name="tradeReserve"/>
                            <button type="submit" name="buyHero" class="btn waves-effect waves-light">Res</button>
                        </form>
                    </td>
                </tr>
            % endfor
        </table>
    </div>
</div>
% else:
    <h1>Invalid game. Please click Dota or Pubg at top</h1>
% endif

<script>
var transfers = ${'true' if transfer_open else 'false'};
var league_id = ${league.id};
var swaps = ${'true' if not transfer_open and league.swap_open and not userq.swap_tstamp else "false"}
</script>

<script src="/static/trade.js"></script>
