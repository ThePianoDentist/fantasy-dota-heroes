<%inherit file="layout.mako"/>

<%def name="title()">
    Account Settings
</%def>

<%def name="meta_keywords()">
    Account settings, Dota, fantasy, points, game
</%def>

<%def name="meta_description()">
    Account settings page for fantasy brood war game.
</%def>

<div>
    % if message:
        <div>
            <div id=${"successMessage" if message_type == 'success' else "message"}>
                ${message}
            </div>
        <div>
    % endif
    <h5>Email settings</h5>
        <form id="emailSettings" action='/updateEmailSettings'>
            <input type="email" name="email" placeholder="${'Email...' if not user.email else ''}" class="email"
             value=${user.email if user.email else ''}></br>
            <input type="checkbox" name="emailContact" ${"checked" if user.contactable else ""}>
            Do you want emailing about upcoming tournaments/news?<br>
            <button type="submit" id="change_email_but">Update email settings</button>
        </form>
    </div>


    <div>
    <h5>Update password</h5>
        <form id="updatePassword" action='/changePassword'>
            <input type="password" name="old_password" placeholder="Current password" class="pwd">
            <input type="password" name="new_password" placeholder="New password" class="pwd">
            <input type="password" name="confirm_new_password" placeholder="Confirm new password">
            <button type="submit" id="change_pwd_but">Change my password</button>
        </form>
    </div>

    <div>
    <h5>Game settings</h5>
        <form id="gameSettings" action='/gameSettings'>
            <input type="checkbox" name="autofillTeam" ${"checked" if user.autofill_team else ""}>
            Automatically pick random team to enter battlecups if none chosen
            <button type="submit" id="change_pwd_but">Update game settings</button>
        </form>
    </div>
</div>