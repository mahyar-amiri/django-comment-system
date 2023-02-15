function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function LoadComment(urlhash, settings_slug) {
    $(`#comment-${urlhash}`).load(
        `/comment/detail?urlhash=${urlhash}&settings_slug=${settings_slug}`
    );
}

function LoadCommentList(page = 1, at_start = false) {
    let app_name = $("#form-comment-create [name='app_name']").val();
    let model_name = $("#form-comment-create [name='model_name']").val();
    let object_id = $("#form-comment-create [name='object_id']").val();
    let settings_slug = $("#form-comment-create [name='settings_slug']").val();
    let comment_list = $("#comment-list")
    comment_list.load(
        `/comment/list?app_name=${app_name}&model_name=${model_name}&object_id=${object_id}&page=${page}&settings_slug=${settings_slug}`
    );

    // scroll to top when turned page
    if (!at_start) {
        $('html, body').animate({
            scrollTop: comment_list.offset().top
        }, 700);
    }
}

function LoadDeleteCommentForm(urlhash) {
    $("#comment-modal").load(
        `/comment/delete/${urlhash}`
    );
}

function LoadCommentReactions(urlhash) {
    $(`#form-comment-react-${urlhash} #comment-react-list`).load(
        `/comment/react?urlhash=${urlhash}`
    );
}

function ResetCreateCommentForm() {
    $(`#form-comment-create [name='content']`).val('').height('124px');
    $(`#form-comment-create [name='is_spoiler']`).prop('checked', false);
}

function ResetEditCommentForm(form_id, content, is_spoiler) {
    let form = $(`#${form_id}`);
    form.find('textarea').val(content).removeClass('animate-[pulse_500ms_linear_infinite] border-textarea-border-empty-light dark:border-textarea-border-empty-dark').addClass('border-textarea-bg-light dark:border-textarea-bg-dark');
    if (is_spoiler === 'True') {
        form.find("[name='is_spoiler']").prop('checked', true);
    } else {
        form.find("[name='is_spoiler']").prop('checked', false);
    }
}

function ResetDeleteCommentForm() {
    $(`#comment-modal`).html('');
}

function CreateComment(form_id) {
    let form = $(`#${form_id}`);
    let method = form.prop('method');
    let action = form.prop('action');
    let formData = {
        //OBJECT INPUTS
        app_name: $("#form-comment-create [name='app_name']").val(),
        model_name: $("#form-comment-create [name='model_name']").val(),
        content_type: $("#form-comment-create [name='content_type']").val(),
        object_id: $("#form-comment-create [name='object_id']").val(),
        settings_slug: $("#form-comment-create [name='settings_slug']").val(),
        //FORM INPUTS
        content: $(`#${form_id} [name='content']`).val(),
        is_spoiler: $(`#${form_id} [name='is_spoiler']`).is(':checked'),
        parent_id: $(`#${form_id} [name='parent_id']`).val(),
    };
    $.ajax({
        type: method,
        url: action,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: formData,
        success: function () {
            if (formData.parent_id) {
                let page = $(`#form-comment-reply-${formData.parent_id} [name='page']`).val();
                LoadCommentList(page);
            } else {
                ResetCreateCommentForm();
                LoadCommentList();
            }
        },
        error: function () {
            let textarea = $(`#${form_id} textarea`);
            if (textarea.val().trim() !== '') {
                alert('ERROR in Creating Comment!')
            }
        }
    });
}

function CheckEditTextarea(form_id) {
    let textarea = $(`#${form_id} textarea`)
    if (textarea.val().trim() === '') {
        textarea.removeClass('border-textarea-bg-light dark:border-textarea-bg-dark').addClass('border-textarea-border-empty-light dark:border-textarea-border-empty-dark');
    } else {
        textarea.removeClass('border-textarea-border-empty-light dark:border-textarea-border-empty-dark animate-[pulse_500ms_linear_infinite]').addClass('border-textarea-bg-light dark:border-textarea-bg-dark');
    }
}

function EditComment(form_id, settings_slug) {
    let form = $(`#${form_id}`);
    let method = form.prop('method');
    let action = form.prop('action');
    let formData = {
        //FORM INPUTS
        content: $(`#${form_id} [name='content']`).val(),
        is_spoiler: $(`#${form_id} [name='is_spoiler']`).is(':checked'),
        urlhash: form_id.replace('form-comment-edit-', ''),
    };
    $.ajax({
        type: method,
        url: action,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: formData,
        success: function (data) {
            if (data.urlhash) {
                LoadComment(data.urlhash, settings_slug);
            }
        },
        error: function () {
            let textarea = $(`#${form_id} textarea`);
            if (textarea.val().trim() === '') {
                textarea.removeClass('border-textarea-bg-light dark:border-textarea-bg-dark').addClass('animate-[pulse_500ms_linear_infinite] border-textarea-border-empty-light dark:border-textarea-border-empty-dark');
            } else {
                alert('ERROR in Creating Comment!')
            }
        }
    });
}

function DeleteComment(urlhash) {
    let form = $(`#form-comment-delete-${urlhash}`);
    let method = form.prop('method');
    let action = form.prop('action');
    $.ajax({
        type: method,
        url: action,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function () {
            ResetDeleteCommentForm();
            LoadCommentList();
        },
        error: function () {
            alert('ERROR in Deleting Comment!')
        }
    });
}

function ReactComment(urlhash, react_slug) {
    let form = $(`#form-comment-react-${urlhash}`);
    let method = form.prop('method');
    let action = form.prop('action');
    $.ajax({
        type: method,
        url: action,
        data: {
            urlhash,
            react_slug
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function () {
            LoadCommentReactions(urlhash);
        }
    });
}

$(document).ready(function () {
    // setTimeout(function () {
    LoadCommentList(undefined, true);
    // }, 100);
});
