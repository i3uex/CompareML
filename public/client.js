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

function submitFile() {
    var reader = new FileReader();
    reader.onload = function () {
        console.log(reader.result);
        populateTargetSelect(reader.result.split('\n')[0]);

        // Upload file
        $.ajax({
            type: "POST",
            url: "/load_csv",
            data: {
                csv: reader.result
            },
            success: function (result) {
                console.log('done');
            },
            error: function (result) {
                alert('fail');
            }
        });
    };
    reader.readAsText($("#file")[0].files[0]);
};

function submitOptions() {

    var providers = [];
    $.each($("input[name='providers']:checked"), function () {
        providers.push($(this).val());
    });
    var algorithms = [];
    $.each($("input[name='algorithms']:checked"), function () {
        algorithms.push($(this).val());
    });

    var options = JSON.stringify({
        providers: providers,
        algorithms: algorithms
    })

    $.ajax({
        type: "POST",
        url: "/set_options",
        data: {
            options
        },
        success: function (result) {
            console.log('options setted')
        },
        error: function (result) {
            alert('fail');
        }
    });
};

// POPULATE METHODS:
function populateTargetSelect(features) {

    features.split(',').forEach(feature => {
        $('<option />', {
                text: feature,
                id: feature
            })
            .appendTo("#target_select");
    });
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
