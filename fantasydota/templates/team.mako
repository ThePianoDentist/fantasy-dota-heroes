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

<%def name="custom_css()">
</%def>

<div class="row" id="myTeamBlock">
    <div class="row">
    <span class="left" style="width: 33%;"><h5><span class="col s3">Team: </span><span id="teamName" class="col s5">${team_name if user else ""}</span>
    <span id="teamNameEdit" class="invisible col s5">
          <input id="teamNameTextField" type="text" class="validate" value=${team_name if user else ""} />
        </span>
    <span class="col s1"><button id="updateNameButton"><i class="material-icons">edit</i></button>
    <button id="confirmNameButton" class="invisible"><i class="material-icons">check</i></button>
    </span>
    </h5></span>
    <span class="left center-align" style="width: 33%;"><h5><a id="leagueLink" target="_blank"></a></h5></span>
    <span class="right"><h5>Points: <span class="userPoints"></span></h5></span>
    </div>
    <div id="teamTableContainer">
        <table class="sortable card-table striped centered" id="teamTable">
            <tr style="cursor: pointer" id="teamTableHeader">
                <th class="heroHeader">Player</th>
                <th class="dummyHeader" colspan="0"></th>
                <th class="positionHeader sorttable_numeric">Position</th>
                <th class="clubHeader extra sorttable_numeric">Club</th>
                <th class="pointsHeader extra sorttable_numeric">Points</th>
                <th class="bonusHeader extra sorttable_numeric">Bonuses</th>
                <th class="sellHeader">Remove</th>
            </tr>
        </table>
    </div>
    <span class="left"><button type="submit" id="useWildcard" disabled="true" title="Wildcard sells entire team and resets to 50 credits" class="btn waves-effect waves-light" style="display:none">
        Use Wildcard</button></span>
    <span class="right"><button type="submit" id="confirmTransfers" disabled="true" class="btn waves-effect waves-light">Confirm Team!</button></span>
</div>
<div id="heroesBlock" class="row">
    <h2>Cards (Credits: <strong><span class="userCredits"></span></strong>)<span class="right">
    <button type="submit" id="newCardPack" title="10 credits" class="btn waves-effect waves-light">
    New pack
    </button></h2>
</div>
    <div id="cardFilters" class="row">
        <div class="col s1"><button type="button" id="filterCards" class="btn waves-effect waves-light">Filter</button></div>
        <div class="col s3">
            <label for="cardTeamFilter"><h6>Team:</h6></label>
            <input id="cardTeamFilter" type="text" class="validate" value="" />
        </div>
        <div class="col s3">
            <label for="cardPlayerFilter"><h6>Player:</h6></label>
            <input id="cardPlayerFilter" type="text" class="validate" value="" />
        </div>
        <div class="col s5">
            <input id="goldFilter" type="checkbox" class="filled-in" checked="checked" />
            <label for="goldFilter">Gold</label>
            <input id="silverFilter" type="checkbox" class="filled-in" checked="checked" />
            <label for="silverFilter">Silver</label>
            <input id="bronzeFilter" type="checkbox" class="filled-in" checked="checked" />
            <label for="bronzeFilter">Bronze</label>
        </div>
    </div>
    <div id="cardsContainer" class="row">
        <ul class = "tabs">
        <li class = "tab col s3"><a href = "#goalkeepers">Goalkeepers</a></li>
        <li class = "tab col s3"><a href = "#defenders">Defenders</a></li>
        <li class = "tab col s3"><a href = "#midfielders">Midfielders</a></li>
        <li class = "tab col s3"><a href = "#forwards">Forwards</a></li>
        </ul>
        <div id="goalkeepers" class="col s12"></div>
        <div id="defenders" class="col s12"></div>
        <div id="midfielders" class="col s12"></div>
        <div id="forwards" class="col s12"></div>
    </div>
<script src="/static/trade.js?v=1.0"></script>
<script src="/static/team.js?v=1.1"></script>
