<%inherit file="layout.mako"/>

<%def name="title()">
    Leaderboard
</%def>

<%def name="meta_keywords()">
    Leaderboard, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Leaderboard page for fantasy DotA cards game.
</%def>

<%def name="custom_css()">
    <link href="/static/dotateams.css?v=1.0" rel="stylesheet"/>
</%def>

<div class="row">
    <span class="left">
    <h2>Predictions: <a id="leagueLink" target="_blank"></a></h2>
    </span>
    <ul class="right">
            <li>
                <a id="predictionPeriodDropdown" class="dropdown-trigger btn" data-hover="true" data-beloworigin="true" href="" data-activates="periodDropdown">
                <i class="material-icons right">arrow_drop_down</i></a>
            </li>
            <ul id="periodDropdown" class="dropdown-content">
            </ul>
        </ul>
</div>
<div class="row">
<div id="predictionsBlock" class="col s12">
    <button type="submit" id="predictBtn" class="btn waves-effect waves-light">Update predictions</button>
    <span><strong>Predictions can be updated up until match start time.</strong></span>
    <span>Correct predictions will award <span id="predictionWinMoney"></span> credits towards new packs</span>
    <div id="predictionsContainer">
    <div class="row" id="predictionsTable">
    </div>
    </div>
</div>

<script>
var period = ${period};

$( document ).ready(function() {
    $('.dropdown-trigger').dropdown();
    $(".dropdown-button").dropdown({
        "belowOrigin": true,
        "hover": true
    });
})
</script>
<script src="/static/predictions.js?v=1.0"></script>
