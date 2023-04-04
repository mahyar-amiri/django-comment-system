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
    document.querySelector(`#comment-${urlhash}`).load(
        `/comment/detail?urlhash=${urlhash}&settings_slug=${settings_slug}`
    );
}

function LoadCommentList(page = 1, at_start = false) {
    let app_name = document.querySelector("#form-comment-create [name='app_name']").value;
    let model_name = document.querySelector("#form-comment-create [name='model_name']").value;
    let object_id = document.querySelector("#form-comment-create [name='object_id']").value;
    let settings_slug = document.querySelector("#form-comment-create [name='settings_slug']").value;
    let comment_list = document.querySelector("#comment-list")
    comment_list.load(
        `/comment/list?app_name=${app_name}&model_name=${model_name}&object_id=${object_id}&page=${page}&settings_slug=${settings_slug}`
    );

    // scroll to top when turned page
    if (!at_start) {
        document.querySelector('html, body').animate({
            scrollTop: comment_list.offset().top
        }, 700);
    }
}

function LoadDeleteCommentForm(urlhash) {
    document.querySelector("#comment-modal").load(
        `/comment/delete/${urlhash}`
    );
}

function LoadCommentReactions(urlhash) {
    document.querySelector(`#form-comment-react-${urlhash} #comment-react-list`).load(
        `/comment/react?urlhash=${urlhash}`
    );
}

function ResetCreateCommentForm() {
    document.querySelector(`#form-comment-create [name='content']`).val('').height('124px');
    document.querySelector(`#form-comment-create [name='is_spoiler']`).prop('checked', false);
}

function ResetEditCommentForm(form_id, content, is_spoiler) {
    let form = document.querySelector(`#${form_id}`);
    form.querySelector('textarea').val(content).classList.remove('animate-[pulse_500ms_linear_infinite] border-textarea-border-empty-light dark:border-textarea-border-empty-dark').classList.add('border-textarea-bg-light dark:border-textarea-bg-dark');
    if (is_spoiler === 'True') {
        form.querySelector("[name='is_spoiler']").prop('checked', true);
    } else {
        form.querySelector("[name='is_spoiler']").prop('checked', false);
    }
}

function ResetDeleteCommentForm() {
    document.querySelector(`#comment-modal`).html('');
}

function CreateComment(form_id) {
    let form = document.querySelector(`#${form_id}`);
    let method = form.prop('method');
    let action = form.prop('action');
    let formData = {
        //OBJECT INPUTS
        app_name: document.querySelector("#form-comment-create [name='app_name']").value,
        model_name: document.querySelector("#form-comment-create [name='model_name']").value,
        content_type: document.querySelector("#form-comment-create [name='content_type']").value,
        object_id: document.querySelector("#form-comment-create [name='object_id']").value,
        settings_slug: document.querySelector("#form-comment-create [name='settings_slug']").value,
        //FORM INPUTS
        content: document.querySelector(`#${form_id} [name='content']`).value,
        is_spoiler: document.querySelector(`#${form_id} [name='is_spoiler']`).is(':checked'),
        parent_id: document.querySelector(`#${form_id} [name='parent_id']`).value,
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
                let page = document.querySelector(`#form-comment-reply-${formData.parent_id} [name='page']`).value;
                LoadCommentList(page);
            } else {
                ResetCreateCommentForm();
                LoadCommentList();
            }
        },
        error: function () {
            let textarea = document.querySelector(`#${form_id} textarea`);
            if (textarea.value.trim() !== '') {
                alert('ERROR in Creating Comment!')
            }
        }
    });
}

function CheckEditTextarea(form_id) {
    let textarea = document.querySelector(`#${form_id} textarea`)
    if (textarea.value.trim() === '') {
        textarea.classList.remove('border-textarea-bg-light dark:border-textarea-bg-dark').classList.add('border-textarea-border-empty-light dark:border-textarea-border-empty-dark');
    } else {
        textarea.classList.remove('border-textarea-border-empty-light dark:border-textarea-border-empty-dark animate-[pulse_500ms_linear_infinite]').classList.add('border-textarea-bg-light dark:border-textarea-bg-dark');
    }
}

function EditComment(form_id, settings_slug) {
    let form = document.querySelector(`#${form_id}`);
    let method = form.prop('method');
    let action = form.prop('action');
    let formData = {
        //FORM INPUTS
        content: document.querySelector(`#${form_id} [name='content']`).value,
        is_spoiler: document.querySelector(`#${form_id} [name='is_spoiler']`).is(':checked'),
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
            let textarea = document.querySelector(`#${form_id} textarea`);
            if (textarea.value.trim() === '') {
                textarea.classList.remove('border-textarea-bg-light dark:border-textarea-bg-dark').classList.add('animate-[pulse_500ms_linear_infinite] border-textarea-border-empty-light dark:border-textarea-border-empty-dark');
            } else {
                alert('ERROR in Creating Comment!')
            }
        }
    });
}

function DeleteComment(urlhash) {
    let form = document.querySelector(`#form-comment-delete-${urlhash}`);
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
    let form = document.querySelector(`#form-comment-react-${urlhash}`);
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

document.querySelector(document).ready(function () {
    // setTimeout(function () {
    LoadCommentList(undefined, true);
    // }, 100);
});