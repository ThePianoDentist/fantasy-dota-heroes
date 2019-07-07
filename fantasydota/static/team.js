var userCanTransfer;
var lateEntry;
var teamUrl;
var players;
var currentIndex;
var tableContainer = $("#tableContainer");
var gridContainer = $("#gridContainer");
var playerDataCache = new Map();

var rightClick = function rightClick(event){
    var newCards = $(".newCard")
    if (currentIndex >= newCards.length -1){return}
    var oldSelected = $(newCards[currentIndex]);
    var oldSelectedZ = parseInt(oldSelected.css('z-index'));
    var newSelected = $(newCards[currentIndex+1]);
    newSelected.css('z-index', oldSelectedZ + 1);
    currentIndex += 1;
};
var leftClick = function leftClick(event){
    if (currentIndex == 0){return}
    var newCards = $(".newCard")
    var oldSelected = $(newCards[currentIndex])
    var oldSelectedZ = parseInt(oldSelected.css('z-index'));
    oldSelected.css('z-index', oldSelectedZ - (2 * currentIndex));
    currentIndex -= 1;
};
$(document).on('click', "#leftClick", leftClick);
$(document).on('click', "#rightClick", rightClick);

$("#updateNameButton").click(updateNameOnclick);
$("#confirmNameButton").click(confirmNameOnclick);
signup();
getLeagueInfo(false, false, false, false).then(getCards);
$("#filterCards").click(function (){
    var teamFilter = $("#cardTeamFilter").val().toLowerCase();
    var playerFilter = $("#cardPlayerFilter").val().toLowerCase();
    var cards = $(".playerCard");
    $.each(cards, function(i, card) {
        var elem = $(this);
        var show = true;
        if (teamFilter && !elem.find(".teamName").text().toLowerCase().includes(teamFilter)) show = false;
        if (show && playerFilter && !elem.find(".playerName").text().toLowerCase().includes(playerFilter)) show = false;
        if (show && !document.getElementById("goldFilter").checked && elem.hasClass("rarity-gold")) show = false;
        if (show && !document.getElementById("silverFilter").checked  && elem.hasClass("rarity-silver")) show = false;
        if (show && !document.getElementById("bronzeFilter").checked  && elem.hasClass("rarity-bronze")) show = false;
        if (show){
            elem.removeClass("invisible");
        } else{
            elem.addClass("invisible");
        }
    })
});
//$.ajax({url: apiBaseUrl + "leagues/" + leagueId,
//    dataType: "json",
//    type: "GET",
//    success: function(data){
//        league = data;
//        console.log(league)
//    }
//}).then(getPickees)

function drawBonus(bonuses, p, j, makeWhite){

    $.each(bonuses, function(bkey, bonus){
        p[++j] = '<p><i><span ';
        if (makeWhite) p[++j] = 'class="bonus-rarity-text" ';
        if (bonus.description){
            p[++j] = 'title="';
            p[++j] = bonus.description;
            p[++j] = '"';
        }
        p[++j] = '>→';
        p[++j] = bonus.name;
        p[++j] = ' x';
        p[++j] = bonus.multiplier;
        p[++j] = '</span></i></p>';
    })
    return j
}

function cardHtml(p, j, player){
    playerDataCache.set(player.cardId, player);
                            p[++j] = '<div style="height: 420px;" class="card col s3 playerCard rounded bottomRightParent rarity-';
                            p[++j] = player.colour.toLowerCase();
                            p[++j] = '"><div class="card-content"><span class="card-title"><h6><p><span class="playerName centre"><strong>';
                            p[++j] = player.name;
                            p[++j] = '</strong></span></p><p><span class="teamName centre">';
                            p[++j] = player.limitTypes.club;
                            p[++j] = '</span></p></h6></span><p><span class="left">';
                            p[++j] = player.limitTypes.position;
                            p[++j] = '</span><span class="right"><button name="buyPlayer" id="addTeam-';
                            p[++j] = player.cardId;
                            p[++j] = '" type="submit" class="btn waves-effect waves-light addTeam" data-cardId="';
                            p[++j] = player.cardId;
                            p[++j] ='">Add</button></span></p>';
                            p[++j] = '</p><div class="card-image"><img src="/static/images/football/placeholder.png"></div><p>';
                            j = drawBonus(player.bonuses, p, j, true);
                            p[++j] = '<button name="recyclePlayer" title="Recycle card for ' + league.recycleValue + ' credits" id="recyclePlayer-';
                            p[++j] = player.cardId;
                            p[++j] = '" type="submit" class="btn waves-effect waves-light recyclePlayer bottomRight" data-cardId="';
                            p[++j] = player.cardId;
                            p[++j] ='">Recycle</button>';
                            p[++j] = '</div></div>';
    return [p, j]
}

function getCards(){
var nextPeriodValue = league.currentPeriod ? league.currentPeriod.value + 1: 1
teamUrl = apiBaseUrl + "leagues/" + leagueId + "/users/" + userId + "?team&stats&period=" + nextPeriodValue;
    $("#leagueLink").attr('href', league.url);
    $("#leagueLink").text(league.name);
    if (!league.started) $('#confirmTransfers').addClass('invisible');
    if (userId != null){
    $.ajax({url: apiBaseUrl + "teams/league/" + leagueId + "/user/" + userId + "/cards?lastXPeriodStats=1&overallStats&period=" + nextPeriodValue,
                type: "GET",
                dataType: "json",
                success: function(data){
                    $.each(["Goalkeeper", "Defender", "Midfielder", "Forward"], function(key, position){
                        var positionLowerCase = position.toLowerCase()
                        var positionDiv = $("#" + positionLowerCase);
                        var p = [], j = -1;
                        $.each(data.filter(function(e){return e.limitTypes.position == position}), function(i, player) {
                            var out = cardHtml(p, j, player);
                            p = out[0];
                            j = out[1];
                        })
                    $("#" + positionLowerCase + "s").html(p.join(''));
                    })
                },
                error: function(jqxhr, textStatus, errorThrown){
                    if (jqxhr.responseText.startsWith("Invalid User ID")){
                        pleaseLogInClick();
                    }
                    else{
                    Swal.fire("Something went wrong. oops!", '', 'error');
                    }
                }
            }).then(getTeamThenSetup);
        }
    else{
        $("#pleaseLogIn").css('display', 'initial');
        $("#myTeamBlock").addClass('invisible');
        undisableButtons();
        $('button[name=buyPlayer]').each(function (key, btn){
            $(this).click(pleaseLogInClick);
        });
        $('#confirmTransfers').click(pleaseLogInClick);
        $('#newCardPack').click(pleaseLogInClick);
    }
    }

function addPlayerHtmlArray(player, r, j){
                    r[++j] = '<tr class="teamRow toSell ';
                    r[++j] = player.limitTypes.position;
                    r[++j] = '" id="';
                    r[++j] = player.cardId;
                    r[++j] = 'TeamRow"><td class="playerImg" sorttable_customkey="';
                    r[++j] = player.name;
                    r[++j] = '">';
                    r[++j] = '</td><td class="playerEntry"><strong>';
                    r[++j] = player.name;
                    r[++j] = '</strong></td><td class="positionEntry">';
                    r[++j] = player.limitTypes.position;
                    r[++j] = '</td><td class="clubEntry">';
                    r[++j] = player.limitTypes.club;
                    r[++j] = '</td><td class="playerPointsEntry">';
                    var card = playerDataCache.get(player.cardId);
                    r[++j] = card.overallStats.points;
                    if (card.recentPeriodStats && card.recentPeriodStats.length > 0){
                    r[++j] = ' ('
                    r[++j] = card.recentPeriodStats.find(function(x){return x.period == (league.currentPeriod.value - 1)}).stats.points;
                    //r[++j] = player.stats.points;
                    r[++j] = ')';
                    }
                    r[++j] = '</td><td class="bonusesEntry">';
                    j = drawBonus(player.bonuses, r, j, false);
                    r[++j] = '</td><td class="tradeEntry">';
                    r[++j] = '<button type="submit" name="sellPlayer" class="btn waves-effect waves-light" disabled="true" data-cardId="';
                    r[++j] = player.cardId;
                    r[++j] = '">Remove</button>';
                    r[++j] = '</td></tr>';
        return r, j
}

function getTeamThenSetup(){
    $.ajax({url: teamUrl,
            dataType: "json",
            type: "GET",
            success: function(data){
                userCanTransfer = (league.transferOpen);
                //lateEntry = (league.currentPeriod && league.currentPeriod.start )
                $(".userCredits").text(data.user.money);
                $(".userPoints").text(data.stats.points);
                var r = new Array(), j = -1;
                $.each(data.team.sort(positionNameSort), function(key, player) {
                r, j = addPlayerHtmlArray(player, r, j);
                })
                $("#teamTable").find("tbody").html(r.join(''));
            },
            error: function(jqxhr, textStatus, errorThrown){
                if (jqxhr.responseText.startsWith("User does not exist on api")){
                    // need to add user first
                     $.ajax({url: apiBaseUrl + "users/",
                            dataType: "json",
                            type: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({"username": username, "userId": userId}),
                            }).then(getTeamThenSetup)  // this time the call should work
                }
                else{
                    Swal.fire("Something went wrong. oops!", '', 'error');
                    }
            }
        }).then(setup);
}

function setup(){
    console.log("in setup")
    $('ul.tabs').tabs();
    undisableButtons();
    $('button[name=buyPlayer]').add('button[name=sellPlayer]').each(function (key, btn){
        $(this).click(tradeOnclick);
    });

    $('.recyclePlayer').each(function (key, btn){
        $(this).click(recycleOnClick);
    });

    $('#confirmTransfers').click(function() {
        disableButtons()
        $.ajax({
            url: "/transfer_proxy",
            dataType: "json",
            type: "POST",
            data: {"sell": toSell, "buy": toBuy, "isCheck": false, "wildcard": wildcard},
            success: function(data){
                Swal.fire({
                 title: "Transfers locked in!",
                 text: "Note: Your new players will start scoring points starting next game week",
                  type: "success"
                }).then(function(){
                    window.location.reload(false);
                });
            },
            error: function(jqxhr, textStatus, errorThrown){
                undisableButtons();
                Swal.fire({'text': jqxhr.responseText, 'type': 'error'});
            }
        });
    });

    $('#newCardPack').click(function() {
        $.ajax({
            url: "/new_card_pack",
            dataType: "json",
            type: "GET",
            success: function(data){
            var data = data.msg;
                var userCredits = $(".userCredits");
                userCredits.text(parseFloat(userCredits.text()) - league.cardPackCost);
                var p = [], j = -1;
                var newCards = [];
                currentIndex = 0;
                p[++j] = '<span class="left"><button name="left" class="btn waves-effect amber lighten-1" id="leftClick"><i class="material-icons">chevron_left</i></button></span><span class="right"><button name="right" class="btn waves-effect amber lighten-1" id="rightClick"><i class="material-icons">chevron_right</i></button>';
                $.each(data, function(i, player){
                    var fullCardHtml = [], j2 =-1;
                    fullCardHtml, j2 = cardHtml(fullCardHtml, j2, player);
                    var newCard = $(fullCardHtml.join(""));
                    $("#" + player.limitTypes.position.toLowerCase() + "s").append(newCard);
                    newCard.find("button[name=buyPlayer]").click(tradeOnclick);
                    newCard.find("button[name=recyclePlayer]").click(recycleOnClick);
                                var positioning = (i * -10) + 110;
                p[++j] = '<div style="height: 420px; position: absolute; right:';
                p[++j] = positioning;
                p[++j] = 'px; z-index:';
                p[++j] =  6 + i * -1;
                p[++j] = ';" class="card col s9 playerCard rounded bottomRightParent newCard';
                 //if (i == 0) p[++j] = ' topCard';
                 p[++j] = ' rarity-';
                            p[++j] = player.colour.toLowerCase();
                            p[++j] = ' ';
                            p[++j] = player.limitTypes.club.split(" ").join("").toLowerCase();
                            p[++j] = '"><div class="card-content"><span class="card-title"><h6><p><span class="centre"><strong>';
                            p[++j] = player.name;
                            p[++j] = '</strong></span></p><p><span class="centre">';
                            p[++j] = player.limitTypes.club;
                            p[++j] = '</span></p></h6></span><p><span class="left">';
                            p[++j] = player.limitTypes.position;
                            p[++j] = '</span>';
                            p[++j] = '</p><div class="card-image"><img src="/static/images/football/placeholder.png"></div><p>';
                            j = drawBonus(player.bonuses, p, j, true);
                            p[++j] = '</div></div>';
                            //newCards.push(p.join(""));
                            });
                var html = p.join("");
                var div = document.createElement("div");
                div.innerHTML = html;
                div.setAttribute("class", "row");
                div.style.position = "relative";
                Swal.fire({
                 html: div,
                 heightAuto: false,
                  type: "",
                  customClass: {content: 'swal-newcards', header: 'swal-newcards-header'},
                  showConfirmButton: false,
                  showCloseButton: true,
                })
                    //window.location.reload(false);
            },
            error: function(jqxhr, textStatus, errorThrown){
                Swal.fire({'text': jqxhr.responseJSON.msg, 'type': 'error'});
            }
        });
    })
}

function updateNameOnclick(){
    var teamName = $("#teamName");
    teamName.addClass("invisible");
    $("#teamNameEdit").removeClass("invisible");
    $("#updateNameButton").addClass("invisible");
    $("#confirmNameButton").removeClass("invisible");
    }
//        $.ajax({
//            url: "/update_team_name",
//            dataType: "json",
//            type: "POST",
//            data: {"name": name},
//            success: function(data){
//                $("#teamName").text(data.team_name);
//            },
//            error: function(jqxhr, textStatus, errorThrown){
//                Swal.fire({'text': jqxhr.responseText, 'type': 'error'});
//            }
//        });

function confirmNameOnclick(){
    var teamName = $("#teamName");
    var teamNameTextField = $("#teamNameTextField");
    $.ajax({
        url: "/update_team_name",
        dataType: "json",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({"name": teamNameTextField.val()}),
        success: function(data){
            $("#teamName").text(data.team_name);
            $("#teamNameEdit").addClass("invisible");
            $("#updateNameButton").removeClass("invisible");
            $("#confirmNameButton").addClass("invisible");
            teamName.removeClass("invisible");
        },
        error: function(jqxhr, textStatus, errorThrown){
            Swal.fire({'text': jqxhr.responseJSON.msg, 'type': 'error'});
        }
    });
}
