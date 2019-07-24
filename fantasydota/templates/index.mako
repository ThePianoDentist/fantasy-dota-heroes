<%inherit file="fantasydota:templates/layout.mako"/>

<%def name="title()">
    Fantasy DotA Cards
</%def>

<%def name="meta_keywords()">
    Fantasy DotA Cards, Home
</%def>

<%def name="meta_description()">
    Home page for Fantasy DotA Cards
</%def>

<%def name="custom_css()">
</%def>

<div class="row">
    <div class="card-panel">
        <h3>A free-to-play, open-source, fantasy DotA league; with card packs and stat bonuses (minus the pay-2-win)</h3>
        <h1>1. <a href="/login">Login</a> with steam, google, or site account</h1>
        <h1>2. Click <a href="/team">Team</a></h1>
        <h1>3. Buy some card packs (5 credits each. 50 starting credits). Gold and silver cards have stat multipliers for greater points hauls</h1>
        <img style="max-width:100%;" src="/static/images/football/cardpackexample.png" />
        <h1>4. Make a team of 2 cores, 2 supports, 1 offlaner from your best cards</h1>
        <img style="max-width:100%;" src="/static/images/football/cardselectexample.png" />
        <img style="max-width:100%;" src="/static/images/football/teamexample.png" />
        <h1>5. Earn (or lose) points based on regular fantasy league criteria:
         <a href="/rules">Scoring</a></h1>
        <h1>6. Go to <a href="/predictions">Predictions</a> to earn credits for more/better cards by predicting correct series scores</h1>
        <img src="/static/images/football/predictionsexample.png" />
    </div>
</div>