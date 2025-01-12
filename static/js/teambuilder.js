function sendToCalc() {
    const params = new URLSearchParams();
    params.append('Level', document.getElementById('Level').value);
    params.append('Round', document.getElementById('Round').value);


    const team1 = document.getElementById('set1').value.split('-')[0];
    const team2 = document.getElementById('set2').value.split('-')[0];
    const team3 = document.getElementById('set3').value.split('-')[0];
    const lastOpp1 = document.getElementById('set4').value.split('-')[0];
    const lastOpp2 = document.getElementById('set5').value.split('-')[0];
    const lastOpp3 = document.getElementById('set6').value.split('-')[0];

    if (team1) {
        params.append('Team1', team1);
    }
    if (team2) {
        params.append('Team2', team2);
    }
    if (team3) {
        params.append('Team3', team3);
    }
    if (lastOpp1) {
        params.append('LastOpp1', lastOpp1);
    }
    if (lastOpp2) {
        params.append('LastOpp2', lastOpp2);
    }
    if (lastOpp3) {
        params.append('LastOpp3', lastOpp3);
    }

    const url = `/?${params.toString()}`;
    window.location.href = url;
}

function showhideSwitch() {
    if (document.getElementById('SwapMode').checked) {
        document.getElementById('TeamHeader').hidden = false;
        document.getElementById('OpponentsHeader').hidden = false;
        for (let element of document.getElementsByClassName('set-title')) {
            element.hidden = true;
        }
        for (let element of document.getElementsByClassName('opp-iv')) {
            element.value = 3;
        }
    } else {
        document.getElementById('TeamHeader').hidden = true;
        document.getElementById('OpponentsHeader').hidden = true;
        document.getElementsByClassName('set-title').hidden = false;
        for (let element of document.getElementsByClassName('set-title')) {
            element.hidden = false;
        }
    }
}

function highlightMatchingTeamMembers() {
    // Build the checklist array from the selected items
    let checklist = [];
    if ($('#set1Check').is(":checked")) checklist.push($('#set1').val());
    if ($('#set2Check').is(":checked")) checklist.push($('#set2').val());
    if ($('#set3Check').is(":checked")) checklist.push($('#set3').val());
    if ($('#set4Check').is(":checked")) checklist.push($('#set4').val());
    if ($('#set5Check').is(":checked")) checklist.push($('#set5').val());
    if ($('#set6Check').is(":checked")) checklist.push($('#set6').val());

    // Highlight matching items in the accordion headers
    $('.accordion-header').each(function() {
        let headerText = $(this).text();

        // Can do === 3 for all only
        let containsAll = checklist.length >= 1 && checklist.every(function(item) {
            return headerText.includes(item);
        });
        if (containsAll) {
            $(this).addClass('highlight');
        } else {
            $(this).removeClass('highlight');
        }
    });
}

$(document).ready(function() {
    $("input.team-checkbox").change(function () {
        if ($(this).is(":checked")) {
            teamChecked.push(this.id);
            if (teamChecked.length > 3) {
                teamChecked.splice(0, 1);
            }
            $("input.team-checkbox").prop("checked", false);
            for (let i = 0; i < teamChecked.length; i++) {
                $("#" + teamChecked[i]).prop("checked", true);
            }
        } else {
            let index = teamChecked.indexOf(this.id);
            teamChecked.splice(index, 1);
        }
        highlightMatchingTeamMembers();
    });
});
