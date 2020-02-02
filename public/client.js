// SERVER COMMUNICATION METHODS:
$(document).ready(function () {
    // Get providers and algorithms
    $.ajax({
        type: "GET",
        url: "/get_options",

        success: function (options) {
            populateProvidersChecks(JSON.parse(options).providers)
            populateAlgorithmsChecks('Classification', JSON.parse(options).algorithms.classification);
            populateAlgorithmsChecks('Regression', JSON.parse(options).algorithms.regression);
        },
        error: function (result) {
            alert('fail');
        }
    });
});

function submitOptions() {
    var reader = new FileReader();
    reader.onload = function () {
        makeRequestSubmit(reader.result);
    };
    reader.readAsText($("#file")[0].files[0]);
};

function makeRequestSubmit(dataset) {
    var providers = [];
    $.each($("input[name='providers']:checked"), function () {
        providers.push($(this).val());
    });

    var algorithms = [];
    $.each($("input[name='algorithms']:checked"), function () {
        algorithms.push($(this).val());
    });

    var options = JSON.stringify({
        dataset: dataset,
        providers: providers,
        algorithms: algorithms,
        target: $("#target_select option:selected")[0].value
    })

    $.ajax({
        type: "POST",
        url: "/set_options",
        data: {
            options
        },
        success: function (result) {
            showResults(result);
        },
        error: function (result) {
            alert('fail');
        }
    });
};

function showResults(result) {

    result = result.replace(/\'/g, "\"");
    result = result.replace(/\"\"/g, "\"");

    // To beautify:
    resultJSON = JSON.parse(result);
    result = JSON.stringify(resultJSON, null, 2)

    result = result.replace(/\\n/g, "\n    ");

    $("#result_pre").text(result);
}

// POPULATE METHODS:
function populateTargetSelect() {
    $("#target_select").empty();
    var reader = new FileReader();
    reader.onload = function () {
        var features = reader.result.split('\n')[0];

        features.split(',').forEach(feature => {
            $('<option />', {
                    text: feature,
                    id: feature
                })
                .appendTo("#target_select");
        });
        reader.error = function () {};
    };

    if ($("#file")[0].files.length > 0) {
        reader.readAsText($("#file")[0].files[0]);
    }
}

function populateProvidersChecks(providers) {
    providers.forEach(provider => {

        $('<label />', {
                for: provider,
                text: provider
            })
            .appendTo("#providers_checks_div");

        $('<input />', {
                type: 'checkbox',
                id: provider,
                name: 'providers',
                value: provider
            })
            .appendTo("#providers_checks_div");
    })
}

function populateAlgorithmsChecks(type, algorithms) {

    if (algorithms && algorithms.length) {
        $('<div />', {
                text: type + ': ',
                id: type + '_checks_div'
            })
            .appendTo("#algorithms_checks_div");

        algorithms.forEach(algorithm => {
            $('<label />', {
                    for: algorithm,
                    text: algorithm
                })
                .appendTo("#" + type + "_checks_div");

            $('<input />', {
                    type: 'checkbox',
                    id: algorithm,
                    name: 'algorithms',
                    value: algorithm
                })
                .appendTo("#" + type + "_checks_div");
        })
    }
}
