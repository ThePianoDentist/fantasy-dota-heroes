<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
     Rules / Scoring
</%def>

<%def name="meta_keywords()">
    Rules, fantasy, dota
</%def>

<%def name="meta_description()">
    Rules page for fantasy dota
</%def>

<div>
    <h2>Scoring</h2>
    <div class="card-panel">
        Points are allocated in the following way:</br>
        <ul class="browser-default">
            <li>Ban       1 points</li>
            <li>Pick      2 points</li>
            <li>Win       6 points</li>
            <li>Loss     -6 points</li>
        </ul></br>
            Bonus points:</br>
            <ul class="browser-default">
            <li>2nd Phase Pick/Ban/Win +1 point</li>
            <li>3rd Phase Pick/Ban/Win +3 point</li>
            </br>
                <li>(Picks and wins stack. A 3rd phase pick will win earn 14 points total!)</li>
        </ul>
            Missing heroes penalty multiplier:</br>
            <ul class="browser-default"><li>x0.5 for every missing hero  (to prevent people abusing half-empty teams of best heroes)
            </li></ul>
            Main event multiplier:</br>
            <ul class="browser-default"><li>x2 points for main event matches
            </li>
            <li>x4 points for final day games
            </li>
            </ul>
        </p>
    </div>
    <h2>Team</h2>
    <div class="card-panel">
        <ul class="browser-default">
            <li>
                Your team can consist of up to 5 dota heroes (you are not required to use all 5, but you incur percentage penalty for each missing hero).
            </li>
            <li>
                Unlimited transfers can take place every day, between games
            </li>
            <li>
            Hero values will be slightly recalibrated every day based upon their performances
            </li>
        </ul>
    </div>
</div>
