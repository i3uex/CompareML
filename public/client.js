function submitFile(e) {
    e.preventDefault();
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
    
    return false;
};

function populateTargetSelect(features) {
    var select = $("#target_select");
    features.split(',').forEach(feature => {
        var option = document.createElement("option");
        option.text = feature;
        option.id = feature;
        select.append(option);
    });
}
