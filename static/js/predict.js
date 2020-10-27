
let base64Image;
$("#image-selector").change(function () {
    let reader = new FileReader();
    reader.onload = function (e) {
        let dataURL = reader.result;

        $('#selected-image').attr("src", dataURL);
        base64Image = dataURL.replace("data:image/jpeg;base64,", "");
        console.log(base64Image);
    }
    reader.readAsDataURL($("#image-selector")[0].files[0]);
    $("#one").text("");
    $("#one-prediction").text("");
});

$("#predict-button").click(function () {
    let message = {
        image: base64Image
    }
    console.log(message);

    $.post("http://127.0.0.1:5000/predict", JSON.stringify(message), function (response) {
        $("#one").text(response.prediction.name1);
        $("#one-prediction").text(response.prediction.value1);
        console.log(response);
    });
});

$("#product-button").click(function () {
    let message = {
        image: base64Image
    }
    console.log(message);

    $.post("http://127.0.0.1:5000/predict", JSON.stringify(message), function (response) {
        //use regex to see product type then redirect.

        if (response.prediction.name1 == "running_shoe") {
            window.location.href = "templates/shoe";
        }
        if (response.prediction.name1 == "jean") {
            window.location.href = "templates/pants";
        }
        if (response.prediction.name1 == "cardigan") {
            window.location.href = "templates/cardigan";
        }
        if (response.prediction.name1 == "jersey") {
            window.location.href = "templates/tshirt";
        }
        if (response.prediction.name1 == "sweatshirt") {
            window.location.href = "templates/sweatshirt";
        }
    });
});

