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

$(function() {
    $(document).on("change", ":checkbox", function() {
        var checked = $("input:checked").length;
        if (checked > 0) {
            $("#start_button").removeClass("disabled");
        } else {
            $("#start_button").addClass("disabled");
        }
    });
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
            showResults(providers, algorithms, JSON.parse(result));
        },
        error: function (result) {
            alert('fail');
        }
    });
};

function showResults(providers, algorithms, result_json) {
    var resultData = Object.entries(result_json)
    $("#result_row").empty();
    for (var algorithm of algorithms) {
        var table = $("<table>");
        table.addClass("table");
        var tableHeader = $("<thead>");
        tableHeader.addClass("thead-light");
        var tableHeaderRow = $("<tr>");
        tableHeaderRow.append($("<th>").text(algorithm));
        var tableBody = $("<tbody>");
        var accuracyRow = $("<tr>");
        accuracyRow.append($("<th>").attr("scope", "row").text("Accuracy"));
        var precisionRow = $("<tr>");
        precisionRow.append($("<th>").attr("scope", "row").text("Precision"));
        var recallRow = $("<tr>");
        recallRow.append($("<th>").attr("scope", "row").text("Recall (Sensitivity"));
        var confusionMatrixRow = $("<tr>");
        confusionMatrixRow.append($("<th>").attr("scope", "row").text("Confusion Matrix"));
        var rawDataRow = $("<tr>");
        rawDataRow.append($("<th>").attr("scope", "row").text("Raw Data"));
        for (var provider of providers) {
            var accuracy = getAccuracy(provider, algorithm, resultData);
            var precision = getPrecision(provider, algorithm, resultData);
            var recall = getRecall(provider, algorithm, resultData);
            var confusionMatrix = getConfusionMatrix(provider, algorithm, resultData);
            var rawData = getRawData(provider, algorithm, resultData);
            tableHeaderRow.append($("<th>").text(provider));
            accuracyRow.append($("<td>").text(accuracy));
            precisionRow.append($("<td>").text(precision));
            recallRow.append($("<td>").text(recall));
            confusionMatrixRow.append($("<td>").append($("<pre>").text(confusionMatrix)));
            rawDataRow.append($("<td>").append($("<pre>").text(rawData)));
        }
        tableHeader.append(tableHeaderRow);
        tableBody.append(accuracyRow);
        tableBody.append(precisionRow);
        tableBody.append(recallRow);
        tableBody.append(confusionMatrixRow);
        tableBody.append(rawDataRow);
        table.append(tableHeader);
        table.append(tableBody);
        var divCol = $('<div align="center"/>').addClass("col align-items-center");
        divCol.append(table);
        $('#result_row').append(divCol);
    }
}

const ProviderName = {
    Turi: "Turi Create",
    Scikit: "Scikit-learn",
    R: "R"
}

function getAccuracy(providerName, algorithmName, resultData) {
    var accuracy = "";
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] == providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
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
    }
    return accuracy;
}

function getPrecision(providerName, algorithmName, resultData) {
    var precision = "";
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] == providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
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
    }
    return precision;
}

function getRecall(providerName, algorithmName, resultData) {
    var recall = "";
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] == providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
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
    }
    return recall;
}

function getConfusionMatrix(providerName, algorithmName, resultData) {
    var confusionMatrix = ""
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] == providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
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
    }
    return confusionMatrix;
}

function getRawData(providerName, algorithmName, resultData) {
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] == providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
        var algorithmData = providerData[algorithmName];
        rawData = JSON.stringify(algorithmData, null, 2)
        rawData = rawData.replace(/\\n/g, "\n    ");
    }
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
            html: '<b>' + type + '</b><br/>',
            id: type.toLowerCase() + '_checks_div'
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
