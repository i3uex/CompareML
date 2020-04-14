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
            populateDefaultDatasetsSelect(optionsParsed.default_datasets)
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
    if ($("#file").is(":disabled")) {
        makeRequestSubmit(true, $("#default_select option:selected").text());

    } else if ($("#default_select").is(":disabled")) {
        var reader = new FileReader();
        reader.onload = function () {
            makeRequestSubmit(false, reader.result);
        };
        reader.readAsText($("#file")[0].files[0]);
    }

};

function makeRequestSubmit(is_default_dataset, dataset) {
    var providers = [];
    $.each($("input[name='providers']:checked"), function () {
        providers.push($(this).val());
    });

    var algorithms = [];
    $.each($("input[name='algorithms']:checked"), function () {
        algorithms.push($(this).val());
    });

    var options = JSON.stringify({
        is_default_dataset: is_default_dataset,
        dataset: dataset,
        providers: providers,
        algorithms: algorithms,
        target: $("#target_select option:selected")[0].value
    });

    $.ajax({
        type: "POST",
        url: "/set_options",
        data: {options},
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
    $("#result_row").empty();
    var providers = Object.entries(result_json)
    for (var provider of providers) {
        var providerName = provider[0];
        var providerData = provider[1];

        // Heading
        var heading = $('<h5 />', {
            text: providerName
        }).addClass("text-center");

        resultsTables = getResultsTables(providerName, providerData);

        var divCol = $('<div align="center"/>').addClass("col align-items-center");
        divCol.append(heading);
        divCol.append(resultsTables);
        $('#result_row').append(divCol);
    }
}

function getResultsTables(providerName, providerData) {
    var tables = $("<div>");

    for (var algorithmName in providerData) {
        var confusionMatrix = getConfusionMatrix(providerName, algorithmName, providerData);
        var accuracy = getAccuracy(providerName, algorithmName, providerData);
        var precision = getPrecision(providerName, algorithmName, providerData);
        var recall = getRecall(providerName, algorithmName, providerData);
        var rawData = getRawData(algorithmName, providerData);

        var table = $("<table>").addClass("table").append(
            $("<caption>").text(algorithmName),
            $("<thead>").addClass("thead-light").append(
                $("<tr>").append(
                    $("<th>").text("Output Name"),
                    $("<th>").text("Output Value")
                )
            ),
            $("<tbody>").append(
                $("<tr>").append(
                    $("<th>").attr("scope", "row").text("Accuracy"),
                    $("<td>").text(accuracy)
                ),
                $("<tr>").append(
                    $("<th>").attr("scope", "row").text("Precision"),
                    $("<td>").text(precision)
                ),
                $("<tr>").append(
                    $("<th>").attr("scope", "row").text("Recall (Sensitivity)"),
                    $("<td>").text(recall)
                ),
                $("<tr>").append(
                    $("<th>").attr("scope", "row").text("Confusion Matrix"),
                    $("<td>").append($("<pre>").text(confusionMatrix))
                ),
                $("<tr>").append(
                    $("<th>").attr("scope", "row").text("Raw Data"),
                    $("<td>").append($("<pre>").text(rawData))
                )
            )
        );

        tables.append(table);
    }

    return tables;
}

const ProviderName = {
    Turi: "Turi Graphlab",
    Scikit: "Scikit-learn",
    R: "R"
}

function getConfusionMatrix(providerName, algorithmName, providerData) {
    var confusionMatrix = ""
    var algorithmData = providerData[algorithmName];
    switch(providerName) {
        case ProviderName.Turi:
            confusionMatrix = algorithmData["confusion_matrix"];
            break;
        case ProviderName.Scikit:
            confusionMatrix = algorithmData["confusion_matrix"];
            break;
        case ProviderName.R:
            confusionMatrix = algorithmData["Confusion Matrix"];
            break;
    }
    return confusionMatrix;
}

function getAccuracy(providerName, algorithmName, providerData) {
    var accuracy = ""
    var algorithmData = providerData[algorithmName];
    switch(providerName) {
        case ProviderName.Turi:
            accuracy = algorithmData["accuracy"];
            break;
        case ProviderName.Scikit:
            accuracy = algorithmData["accuracy"];
            break;
        case ProviderName.R:
            accuracy = algorithmData["Accuracy"];
            break;
    }
    return accuracy;
}

function getPrecision(providerName, algorithmName, providerData) {
    var precision = ""
    var algorithmData = providerData[algorithmName];
    switch(providerName) {
        case ProviderName.Turi:
            precision = algorithmData["precision"];
            break;
        case ProviderName.Scikit:
            precision0 = algorithmData["0"]["precision"];
            precision1 = algorithmData["1"]["precision"];
            precision = (precision0 + precision1) / 2
            break;
        case ProviderName.R:
            precision = algorithmData["Pos Pred Value"];
            break;
    }
    return precision;
}

function getRecall(providerName, algorithmName, providerData) {
    var recall = ""
    var algorithmData = providerData[algorithmName];
    switch(providerName) {
        case ProviderName.Turi:
            recall = algorithmData["recall"];
            break;
        case ProviderName.Scikit:
            recall0 = algorithmData["0"]["recall"];
            recall1 = algorithmData["1"]["recall"];
            recall = (recall0 + recall1) / 2
            break;
        case ProviderName.R:
            recall = algorithmData["Sensitivity"]
            break;
    }
    return recall;
}

function getRawData(algorithmName, providerData) {
    var algorithmData = providerData[algorithmName];
    rawData = JSON.stringify(algorithmData, null, 2)
    rawData = rawData.replace(/\\n/g, "\n    ");
    return rawData;
}

// POPULATE METHODS:
function populateDefaultDatasetsSelect(default_datasets) {
    default_datasets.forEach(dataset => {
        $('<option />', {
                text: dataset,
                id: dataset
            })
            .appendTo("#default_select");
    });
}

function populateTargetSelect(features) {
    features.forEach(feature => {
        feature = feature.replace(/"/g, '')

        $('<option />', {
                text: feature,
                id: feature
            })
            .appendTo("#target_select");
    });
}

function populateTargetSelectWithFile() {
    $("#target_select").empty();
    var reader = new FileReader();
    reader.onload = function () {
        var features = reader.result.split('\n')[0];

        populateTargetSelect(features.split(','));
        reader.error = function () {};
    };

    if ($("#file")[0].files.length > 0) {
        reader.readAsText($("#file")[0].files[0]);
        $("#default_select").attr("disabled", true);
    } else {
        $("#default_select").attr("disabled", false);
    }
}

function populateTargetSelectWithDefault() {
    $("#target_select").empty();
    $.ajax({
        type: "GET",
        url: "/get_default_dataset_headers",
        data: {
            default_dataset_name: $("#default_select option:selected").text()
        },
        success: function (response) {
            populateTargetSelect(response.headers);
            $("#file").attr("disabled", true);
        },
        error: function (result) {
            alert('fail');
        }
    });
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
