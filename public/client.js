var classificationAlgorithms = [];
var regressionAlgorithms = [];

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
            classificationAlgorithms = optionsParsed.algorithms.classification;
            populateAlgorithmsChecks('Regression', optionsParsed.algorithms.regression);
            regressionAlgorithms = optionsParsed.algorithms.regression;
            populateDefaultDatasetsSelect(optionsParsed.default_datasets)
        },
        error: function (result) {
            alert('fail');
            stopLoading();
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
        enableStartButton();
    });

    $(document).on("change", ":file", function() {
        enableStartButton();
    });

    $(document).on("change", "#default_select", function() {
        enableStartButton();
    });
});

function enableStartButton() {
    var datasetUploaded = $("#file").get(0).files.length > 0;
    var datasetSelected = $("#default_select").children("option:selected").val() !== "Make a selection";
    var providersChecked = $("#providers_checks_div input:checked").length > 0;
    var algorithmsChecked = $("#algorithms_checks_div input:checked").length > 0;

    let startButton = $("#start_button")
    if ((datasetUploaded || datasetSelected) && providersChecked && algorithmsChecked) {
        if (startButton.hasClass("disabled")) {
            startButton.removeClass("disabled");
            startButton.on("click", submitOptions)
        }
    } else {
        if (!startButton.hasClass("disabled")) {
            startButton.addClass("disabled");
            startButton.off("click");
        }
    }
}

function stopLoading() {
    $('#start_button').html('Start');
    $("#start_button").removeClass("disabled");
}

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
    if (!$('#start_button').hasClass("disabled")) {
        $('#start_button').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Processing...').addClass('disabled');
    }

    $("#patient_warning").show();

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
            $("#patient_warning").hide();
        },
        error: function (request, textStatus, errorThrown) {
            var errorMessage = request.responseText.trim();
            alert(errorMessage);
            stopLoading();
            $("#patient_warning").hide();
        }
    });
};

function getErrorMessage(html) {
    var startToken = "Error message: ";
    var endToken = "\n";
    var startPosition = html.indexOf(startToken) + startToken.length;
    var endPosition = html.indexOf(endToken, startPosition)
    var errorMessage = html.slice(startPosition, endPosition)
    return errorMessage
}

function showResults(providers, algorithms, result_json) {
    var resultData = Object.entries(result_json)
    $("#result_row").empty();
    for (var algorithm of algorithms) {
        var table;
        if (classificationAlgorithms.includes(algorithm)) {
            table = showResultsClassification(algorithm, providers, resultData)
        } else if (regressionAlgorithms.includes(algorithm)) {
            table = showResultsRegression(algorithm, providers, resultData)
        }
        var divCol = $('<div align="center"/>').addClass("col align-items-center");
        divCol.append(table);
        $('#result_row').append(divCol);
    }

    stopLoading();
}

function showResultsRegression(algorithm, providers, resultData) {
    var table = $("<table>");
    table.addClass("table");
    var tableHeader = $("<thead>");
    tableHeader.addClass("thead-light");
    var tableHeaderRow = $("<tr>");
    tableHeaderRow.append($("<th>").text(algorithm));
    var tableBody = $("<tbody>");
    var rmseRow = $("<tr>");
    rmseRow.append($("<th>").attr("scope", "row").text("RMSE"));
    var maxErrorRow = $("<tr>");
    maxErrorRow.append($("<th>").attr("scope", "row").text("Max-Error"));
    var rawDataRow = $("<tr>");
    rawDataRow.append($("<th>").attr("scope", "row").text("Raw Data"));
    for (var provider of providers) {
        var rmse = getRmse(provider, algorithm, resultData);
        var maxError = getMaxError(provider, algorithm, resultData);
        var rawData = getRawData(provider, algorithm, resultData);
        tableHeaderRow.append($("<th>").text(provider));
        rmseRow.append($("<td>").text(rmse));
        maxErrorRow.append($("<td>").text(maxError));
        rawDataRow.append($("<td>").append($("<pre>").text(rawData)));
    }
    tableHeader.append(tableHeaderRow);
    tableBody.append(rmseRow);
    tableBody.append(maxErrorRow);
    tableBody.append(rawDataRow);
    table.append(tableHeader);
    table.append(tableBody);
    return table;
}

function showResultsClassification(algorithm, providers, resultData) {
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
    recallRow.append($("<th>").attr("scope", "row").text("Recall (Sensitivity)"));
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
    return table;
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
        if (item[0] === providerName) {
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
        if (item[0] === providerName) {
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
                precision = 0
                let precisionItems = 0
                for (let key in algorithmData) {
                    if (key !== "accuracy" && key !== "confusion_matrix" && key !== "macro avg" && key !== "weighted avg") {
                        if (algorithmData.hasOwnProperty(key)) {
                            precision += algorithmData[key]["precision"]
                            precisionItems += 1
                        }
                    }
                }
                precision /= precisionItems
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
        if (item[0] === providerName) {
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
                recall = 0
                let recallItems = 0
                for (let key in algorithmData) {
                    if (key !== "accuracy" && key !== "confusion_matrix" && key !== "macro avg" && key !== "weighted avg") {
                        if (algorithmData.hasOwnProperty(key)) {
                            recall += algorithmData[key]["recall"]
                            recallItems += 1
                        }
                    }
                }
                recall /= recallItems
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
        if (item[0] === providerName) {
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

function getRmse(providerName, algorithmName, resultData) {
    var rmse = "";
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] === providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
        var algorithmData = providerData[algorithmName];
        switch(providerName) {
            case ProviderName.Turi:
                rmse = algorithmData["rmse"];
                break;
            case ProviderName.Scikit:
                rmse = algorithmData["rmse"];
                break;
            case ProviderName.R:
                rmse = algorithmData["rmse"];
                break;
        }
    }
    return rmse;
}

function getMaxError(providerName, algorithmName, resultData) {
    var maxError = "";
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] === providerName) {
            providerData = item[1];
            break;
        }
    }
    if (providerData != null) {
        var algorithmData = providerData[algorithmName];
        switch(providerName) {
            case ProviderName.Turi:
                maxError = algorithmData["max_error"];
                break;
            case ProviderName.Scikit:
                maxError = algorithmData["max_error"];
                break;
            case ProviderName.R:
                maxError = algorithmData["max_error"];
                break;
        }
    }
    return maxError;
}

function getRawData(providerName, algorithmName, resultData) {
    var providerData = null;
    for (var i in resultData) {
        item = resultData[i];
        if (item[0] === providerName) {
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
    var fileSizeLimit = 10; // MB
    var fileSize = $("#file")[0].files[0].size;
    if (fileSize > fileSizeLimit * 1024 * 1024) {
        alert("File size limit is " + fileSizeLimit + " MB.");
        $("#file").val("");
        return;
    }

    $("#target_select").empty();
    var reader = new FileReader();
    reader.onload = function () {
        var features = reader.result.split('\n')[0];

        featuresArray = features.split(',');
        populateTargetSelect(featuresArray);

        $("#target_select").prop('selectedIndex', featuresArray.length - 1);

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
            $("#target_select").prop('selectedIndex', response.headers.length - 1);
            $("#file").attr("disabled", true);
        },
        error: function (result) {
            alert('fail');
            stopLoading();
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
            src: '/static/img/' + provider.replace(" ", "_") + '.png',
            srcset: '/static/img/' + provider.replace(" ", "_") + '@2x.png 2x',
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
