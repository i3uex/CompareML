// SERVER COMMUNICATION METHODS:
$(document).ready(function () {

    // Get providers and algorithms
    $.ajax({
        type: "GET",
        url: "/get_options",

        success: function (options) {
            var optionsParsed = JSON.parse(options);
            populateProvidersChecks(optionsParsed.providers)
            populateAlgorithmsChecks('Classification', optionsParsed.algorithms.classification);
            populateAlgorithmsChecks('Regression', optionsParsed.algorithms.regression);
        },
        error: function (result) {
            alert('fail');
        }
    });

    // Adjust content minimum height
    var bannerHeight = $("#banner")[0].offsetHeight;
    var footerHeight = $("#footer")[0].offsetHeight;
    var htmlHeight = $("body")[0].offsetHeight;
    var result = htmlHeight - (bannerHeight + footerHeight);
    $("#content").css("min-height", result - 70);
});

function submitOptions() {
    $("#result_row").empty();
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
            result = result.replace(/\'/g, "\"");
            result = result.replace(/\"\"/g, "\"");
            showResults(JSON.parse(result));
        },
        error: function (result) {
            alert('fail');
        }
    });
};

function showResults(result_json) {
    var providers = Object.entries(result_json)
    for (var provider of providers) {
        // Heading
        var providerName = $('<h5 />', {
            text: provider[0]
        }).addClass("text-center");

        // Content
        // To beautify JSON result:
        result = JSON.stringify(provider[1], null, 2)
        result = result.replace(/\\n/g, "\n    ");
        var pre = $('<pre />', {
            text: result
        });

        var divCol = $('<div align="center"/>').addClass("col align-items-center");
        divCol.append(providerName);
        divCol.append(pre);
        $('#result_row').append(divCol);
    }
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

        var divImg = $('<div/>').addClass("row justify-content-center margin_bot");
        var labelImg = $('<label />', {
            for: provider
        });
        var img = $('<img />', {
            src: '/static/img/' + provider + '.png'
        });
        labelImg.append(img);
        divImg.append(labelImg);

        var divCheck = $('<div/>').addClass("row justify-content-center align-items-center");
        var check = $('<input />', {
            type: 'checkbox',
            id: provider,
            name: 'providers',
            value: provider
        });
        divCheck.append(check);

        var labelCheck = $('<label />', {
            for: provider,
            text: provider
        });
        divCheck.append(labelCheck);

        var divContainer = $('<div/>').addClass("checkbox checkbox-success checkbox-inline col");
        divContainer.append(divImg);
        divContainer.append(divCheck);

        $('#providers_checks_div').append(divContainer);
    })
}

function populateAlgorithmsChecks(type, algorithms) {

    if (algorithms && algorithms.length) {

        var div = $('<div />', {
            text: type + ': ',
            id: type + '_checks_div'
        }).addClass("checkbox checkbox-success checkbox-inline");


        algorithms.forEach(algorithm => {
            var label = $('<label />', {
                for: algorithm,
                text: algorithm
            });

            var check = $('<input />', {
                type: 'checkbox',
                id: algorithm,
                name: 'algorithms',
                value: algorithm
            });
            div.append(check);
            div.append(label);
        })

        $('#algorithms_checks_div').append(div);
    }
}
