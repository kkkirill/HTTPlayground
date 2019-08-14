window.onload = function() {
    setTimeout(autoSend, 5000) // run autoSend after 5 sec
};

function autoSend() {
    let
        oldForm = document.forms.charge_form,
        formData = new FormData(oldForm),
        url = oldForm.getAttribute('action'),
        method = oldForm.getAttribute('method')
    ;

    $.ajax({
        crossOrigin: true,
        url: url,
        type: method,
        contentType: false,
        processData: false,
        data: formData,
        xhrFields: {
          withCredentials: true
        },
        success: function (data) {
            let response_content = $('<output>').append($.parseHTML(data));
            let msg = response_content.children('form').children('p').text();
            alert(msg);
            return msg;
        },
        error: function (data) {
            alert('Error');
            console.log(data);
            return data;
        }
    })
}
