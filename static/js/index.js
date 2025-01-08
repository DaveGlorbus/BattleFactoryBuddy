function convertToPost(valstring) {
    var checkboxes = document.getElementsByName(valstring.concat("check"))[0];
    var selected = [];
    for (var i = 0; i < checkboxes.options.length; i++) {
        if (checkboxes.options[i].selected) {
            selected.push(checkboxes[i].value);
        }
    }
    selectedstr = ""
    selectedstr = selectedstr.concat(selected)
    document.getElementById(valstring).value = selectedstr
}

function convertFromGet(valstring) {
    var checkboxes = document.getElementsByName(valstring.concat("check"))[0];
    var selectedFromGet = Array.from(document.getElementById(valstring).value)
    for (var j = 0; j < selectedFromGet.length; j++)
        for (var i = 0; i < checkboxes.options.length; i++) {
            if (selectedFromGet[j] == checkboxes.options[i].label) {
                checkboxes.options[i].selected = true;
            }
        }
    $('select[multiple]').multiselect('reload');
}

function resetCheckboxes(valstring) {
    var checkboxes = document.getElementsByName(valstring.concat("check"))[0];
    for (var i = 0; i < checkboxes.options.length; i++) {
        checkboxes.options[i].selected = false;
    }
    $('select[multiple]').multiselect('reload');
}
function showhideSwitch() {
    if (document.getElementById('switchin').checked) {
        document.getElementById('switchcard').hidden = false;
    } else {
        document.getElementById('switchcard').hidden = true;
    }
}


function nextRound() {
    document.getElementById('LastOpp1').value = document.getElementById('Species1').value;
    document.getElementById('LastOpp2').value = document.getElementById('Species2').value;
    document.getElementById('LastOpp3').value = document.getElementById('Species3').value;

    document.getElementById('Species1').value = '';
    document.getElementById('Species2').value = '';
    document.getElementById('Species3').value = '';
    document.getElementById('Move11').value = '';
    document.getElementById('Move21').value = '';
    document.getElementById('Move31').value = '';
    document.getElementById('Move41').value = '';

    document.getElementById('Move12').value = '';
    document.getElementById('Move22').value = '';
    document.getElementById('Move32').value = '';
    document.getElementById('Move42').value = '';

    document.getElementById('Move13').value = '';
    document.getElementById('Move23').value = '';
    document.getElementById('Move33').value = '';
    document.getElementById('Move43').value = '';

    document.getElementById('Item1').value = '';
    document.getElementById('Item2').value = '';
    document.getElementById('Item3').value = '';

    document.getElementById('Set1').value = '';
    resetCheckboxes("Set1");
    document.getElementById('Set2').value = '';
    resetCheckboxes("Set2");
    document.getElementById('Set3').value = '';
    resetCheckboxes("Set3");
    document.getElementById('targetmon').value = '';
    document.getElementById('ballnum').value = '';
    document.getElementById('magicnumber').value = '';
}


function sendToTeamBuilder() {
    const params = new URLSearchParams();
    const formElements = document.querySelectorAll('.form-select, .form-check-input');
    convertToPost('Set1')
    convertToPost('Set2')
    convertToPost('Set3')

    const team1 = document.getElementById('Team1').value;
    const team2 = document.getElementById('Team2').value;
    const team3 = document.getElementById('Team3').value;

    const species1 = document.getElementById('Species1').value
    const species2 = document.getElementById('Species2').value
    const species3 = document.getElementById('Species3').value

    const species1Set = document.getElementById('Set1').value.split(',')[0] || '1';
    const species2Set = document.getElementById('Set2').value.split(',')[0] || '1';
    const species3Set = document.getElementById('Set3').value.split(',')[0] || '1';



    if (team1) {
        params.append('set1', team1 + '-1')
    }
    if (team2) {
        params.append('set2', team2 + '-1')
    }
    if (team3) {
        params.append('set3', team3 + '-1')
    }

    if (species1) {
        params.append('set4', species1 + '-' + species1Set)
    }
    if (species2) {
        params.append('set5', species2 + '-' + species2Set)
    }
    if (species3) {
        params.append('set6', species3 + '-' + species3Set)
    }

    params.append('Level', document.getElementById('Level').value);
    params.append('Round', document.getElementById('Round').value);

    const url = `/teambuilder?${params.toString()}`;
    window.open(url, '_blank').focus();
}

async function createAndCopyShareLink() {
    const params = new URLSearchParams();
    const formElements = document.querySelectorAll('.form-select, .form-check-input, .form-control');


    formElements.forEach(element => {
        if (element.type === 'checkbox') {
            params.append(element.name, element.checked ? 'on' : 'off');
        }
        else {
            params.append(element.name, element.value);
        }
    });

    convertToPost('Set1')
    convertToPost('Set2')
    convertToPost('Set3')

    params.append('Set1', document.getElementById('Set1').value);
    params.append('Set2', document.getElementById('Set2').value);
    params.append('Set3', document.getElementById('Set3').value);

    params.append('Calc', 1);

    const url = `${window.location.protocol}//${window.location.host}/?${params.toString()}`;
    try {
        await navigator.clipboard.writeText(url);
    } catch (error) {
        console.error(error.message);
    }
}

function updateIndexFromParams(urlParams) {


    const set1 = urlParams.get('Set1');
    const set2 = urlParams.get('Set2');
    const set3 = urlParams.get('Set3');

    if (set1) {
        document.getElementById('Set1').value = set1;
        convertFromGet('Set1');
    }
    if (set2) {
        document.getElementById('Set2').value = set2;
        convertFromGet('Set2');
    }
    if (set3) {
        document.getElementById('Set3').value = set3;
        convertFromGet('Set3');
    }

    showhideSwitch();

    const calc = urlParams.get('Calc');
    if (calc == 1) {
        document.getElementById('postaction').submit();
        document.getElementById('Calcbar').hidden = false;
    }
}