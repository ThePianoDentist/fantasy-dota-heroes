<%inherit file="layout.mako"/>

<%def name="title()">
    League Team
</%def>

<%def name="meta_keywords()">
    League, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    League page for fantasy dota game.
</%def>

<div class="row" id="myTeamBlock">
    <div class="row">
    <span class="left" style="width: 33%;"><h5>Team: ${user.username if user else ""}</h5></span>
    <span class="left center-align" style="width: 33%;"><h5><a id="leagueLink" target="_blank"></a></h5></span>
    <span class="right"><h5>Points: <span class="userPoints"></span></h5></span>
    </div>
    <div id="teamTableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer" id="teamTableHeader">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader sorttable_numeric">Points</th>
                <th class="picksHeader extra sorttable_numeric">Picks</th>
                <th class="bansHeader extra sorttable_numeric">Bans</th>
                <th class="winsHeader extra sorttable_numeric">Wins</th>
                <th class="valueHeader sorttable_numeric">Value</th>
                <th class="sellHeader">Sell</th>
            </tr>
        </table>
    </div>
    <span class="left"><button type="submit" id="useWildcard" disabled="true" title="Wildcard sells entire team and resets to 50 credits" class="btn waves-effect waves-light" style="display:none">
        Use Wildcard</button></span>
    <span class="right"><button type="submit" id="confirmTransfers" disabled="true" class="btn waves-effect waves-light">Confirm Team!</button></span>
</div>

<div class="card row">
    <div class="card-content">
        <p><span id="pleaseLogIn" style="display:none" class="messageTransClosed"><strong><a href="${request.route_path('login')}">Please log in or register to pick a team</a></strong></span></p>
        <p>Pick any 5 heroes to gain points from picks, bans and wins during main event stage. <a href="/rules">Scoring details</a></p>
    </div>
</div>
<div id="heroesBlock" class="row">
    <h2>Heroes (Credits Available: <strong><span class="userCredits"></span></strong>)</h2>
      <div class="switch">
    <label>
      Table view (sortable)
      <input type="checkbox" id="gridViewBtn" onchange="switchGridTable(this);" checked autocomplete="off">
      <span class="lever"></span>
      Grid view
    </label>
  </div>
    <div id="gridContainer">
        <table class="card-table striped centered" id="heroesTableGrid">
        <tr><td></td></tr>
        </table>
    </div>
    <div id="tableContainer" style="display:none">
        <table class="sortable card-table striped centered" id="heroesTable">
            <tr style="cursor: pointer" id="heroesTableHeader">
                <th class="heroHeader">Hero</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="heroPointsHeader sorttable_numeric">Points</th>
                <th class="picksHeader extra sorttable_numeric">Picks</th>
                <th class="bansHeader extra sorttable_numeric">Bans</th>
                <th class="winsHeader extra sorttable_numeric">Wins</th>
                <th class="valueHeader sorttable_numeric">Value</th>
                <th class="sellHeader">Buy</th>
            </tr>
        </table>
    </div>
</div>
<script src="/static/trade.js?v=1.0"></script>
<script src="/static/team.js?v=1.1"></script>
