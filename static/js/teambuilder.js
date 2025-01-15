function sendToCalc() {
    const params = new URLSearchParams();
    params.append('Level', document.getElementById('Level').value);
    params.append('Round', document.getElementById('Round').value);

    const sets = [
        { id: 'set1', check: document.getElementById('set1Check').checked },
        { id: 'set2', check: document.getElementById('set2Check').checked },
        { id: 'set3', check: document.getElementById('set3Check').checked },
        { id: 'set4', check: document.getElementById('set4Check').checked },
        { id: 'set5', check: document.getElementById('set5Check').checked },
        { id: 'set6', check: document.getElementById('set6Check').checked }
    ];

    const team = [];
    const lastOpp = [];

    // Add the checked team members
    sets.forEach((set, index) => {
        const species = document.getElementById(set.id).value.split('-')[0];
        if (set.check) {
            team.push(species);
        }
    });

    // Add the remaining sets in order, if a full team has been selected
    if (team.length == 3) {
        sets.forEach((set, index) => {
            const species = document.getElementById(set.id).value.split('-')[0];
            if (!set.check) {
                lastOpp.push(species);
            }
        });
    }

    // Add the team members to the URL parameters
    if (team[0]) params.append('Team1', team[0]);
    if (team[1]) params.append('Team2', team[1]);
    if (team[2]) params.append('Team3', team[2]);

    // Add the last opponents to the URL parameters
    if (lastOpp[0]) params.append('LastOpp1', lastOpp[0]);
    if (lastOpp[1]) params.append('LastOpp2', lastOpp[1]);
    if (lastOpp[2]) params.append('LastOpp3', lastOpp[2]);

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
    // Build the array of checked sets
    let checklist = [];
    if ($('#set1Check').is(":checked")) checklist.push($('#set1').val());
    if ($('#set2Check').is(":checked")) checklist.push($('#set2').val());
    if ($('#set3Check').is(":checked")) checklist.push($('#set3').val());
    if ($('#set4Check').is(":checked")) checklist.push($('#set4').val());
    if ($('#set5Check').is(":checked")) checklist.push($('#set5').val());
    if ($('#set6Check').is(":checked")) checklist.push($('#set6').val());

    // Highlight matching items in the accordion headers
    $('.accordion-header').each(function () {
        let headerText = $(this).text();

        // Can do === 3 for all only
        // Highlight any team headers which contain all of the checked members
        // i.e 1 team if all checked, or 4 if two checked...
        let containsAll = checklist.length >= 1 && checklist.every(function (item) {
            return headerText.includes(item);
        });
        if (containsAll) {
            $(this).addClass('highlight');
        } else {
            $(this).removeClass('highlight');
        }
    });
}

$(document).ready(function () {
    // Only allow 3 checkboxes (the team) to be checked
    $("input.team-checkbox").change(function () {
        let maxChecked = 3;
        let checkedChecks = document.querySelectorAll(".team-checkbox:checked");
        if (checkedChecks.length >= maxChecked + 1) {
            this.checked = false;
            return;
        }

        highlightMatchingTeamMembers();
    });
});
