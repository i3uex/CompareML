$(document).ready(function () {
    $("#upload_form").submit(function (e) {
        e.preventDefault();

        var reader = new FileReader();
        reader.onload = function () {
            console.log(reader.result)
            $.ajax({
                type: "POST",
                url: "/load_csv",
                data: {
                    csv: 'test'
                },
                success: function (result) {
                    alert('done' + result);
                },
                error: function (result) {
                    alert('fail');
                }
            });

        };
        reader.readAsText($("#file")[0].files[0]);
    });
});
