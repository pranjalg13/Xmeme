// Script for posting meme through api and ajax

const alertBox = document.getElementById("alert-box");
const form = document.getElementById("p-form");
const ownername = document.getElementById("id_name");
const caption = document.getElementById("id_caption");
const url = document.getElementById("id_url");
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const editbtn = document.getElementById("meme-edit-btn");

const submiturl = "http://127.0.0.1:8081/memes";

const handleAlerts = (type, text) => {
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                            ${text}
                        </div>`;
};

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const fd = new FormData();
    fd.append("csrfmiddlewaretoken", csrf[0].value);
    fd.append("name", ownername.value);
    fd.append("caption", caption.value);
    fd.append("url", url.value);

    $.ajax({
        type: "POST",
        url: submiturl,
        enctype: "multipart/form-data",
        data: fd,
        success: function (response) {
            $("#all-memes-container").load(
                location.href + " #all-memes-container"
            );
            const sText = `Your Meme is live now`;
            handleAlerts("success", sText);
            setTimeout(() => {
                alertBox.innerHTML = "";
                ownername.value = "";
                caption.value = "";
                url.value = "";
            }, 2500);
        },
        error: function (error) {
            if (error.statusText == "Conflict") {
                handleAlerts("danger", "Meme alerady exist");
            } else if (error.status == 400) {
                handleAlerts("danger", "URL is not valid ");
            } else if (error.statusText == "error") {
                handleAlerts("danger", "Server is down");
            }
            setTimeout(() => {
                alertBox.innerHTML = "";
            }, 1000);
        },
        cache: false,
        contentType: false,
        processData: false,
    });
});
