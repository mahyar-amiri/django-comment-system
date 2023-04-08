function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function load(element, url) {
    let xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === XMLHttpRequest.DONE) {
            if (xmlhttp.status === 200) {
                element.innerHTML = xmlhttp.responseText;
                const allScripts = element.getElementsByTagName('script');
                for (let n = 0; n < allScripts.length; n++) {
                    eval(allScripts [n].innerHTML)//run script inside div generally not a good idea but these scripts are anyways intended to be executed.
                }
            } else {
                alert('Error');
            }
        }
    }

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function LoadComment(urlhash, settings_slug) {
    load(
        document.querySelector(`#comment-${urlhash}`),
        `/comment/detail?urlhash=${urlhash}&settings_slug=${settings_slug}`
    );
}

function LoadCommentList(page = 1, at_start = false) {
    let app_name = document.querySelector(`#form-comment-create [name='app_name']`).value;
    let model_name = document.querySelector(`#form-comment-create [name='model_name']`).value;
    let object_id = document.querySelector(`#form-comment-create [name='object_id']`).value;
    let settings_slug = document.querySelector(`#form-comment-create [name='settings_slug']`).value;
    let comment_list = document.querySelector('#comment-list')
    load(comment_list, `/comment/list?app_name=${app_name}&model_name=${model_name}&object_id=${object_id}&page=${page}&settings_slug=${settings_slug}`);

    // scroll to top when turned page
    if (!at_start) {
        document.querySelector('html').style.scrollBehavior = 'smooth';
        window.scroll(0, comment_list.offsetTop);
    }
}

function LoadDeleteCommentForm(urlhash) {
    load(
        document.querySelector('#comment-modal'),
        `/comment/delete/${urlhash}`
    );
}

function LoadCommentReactions(urlhash) {
    load(
        document.querySelector(`#form-comment-react-${urlhash} #comment-react-list`),
        `/comment/react?urlhash=${urlhash}`
    );
}

function ResetCreateCommentForm() {
    document.querySelector(`#form-comment-create [name='content']`).value = '';
    document.querySelector(`#form-comment-create [name='content']`).style.height = '124px';
    document.querySelector(`#form-comment-create [name='is_spoiler']`).checked = false;
}

function ResetEditCommentForm(form_id, content, is_spoiler) {
    let edit_textarea = document.querySelector(`#${form_id} textarea`);
    edit_textarea.value = content;
    edit_textarea.classList.remove('animate-[pulse_500ms_linear_infinite]', 'border-textarea-border-empty-light', 'dark:border-textarea-border-empty-dark');
    edit_textarea.classList.add('border-textarea-bg-light', 'dark:border-textarea-bg-dark');
    document.querySelector(`#${form_id} [name='is_spoiler']`).checked = is_spoiler === 'True';
}

function ResetDeleteCommentForm() {
    document.querySelector(`#comment-modal`).innerHTML = '';
}

function CreateComment(form_id, statusCheck) {
    let status_check = statusCheck === 'True'
    let form = document.querySelector(`#${form_id}`);
    let method = form.getAttribute('method');
    let action = form.getAttribute('action');
    let data = {
        //OBJECT INPUTS
        app_name: document.querySelector(`#form-comment-create [name='app_name']`).value,
        model_name: document.querySelector(`#form-comment-create [name='model_name']`).value,
        content_type: document.querySelector(`#form-comment-create [name='content_type']`).value,
        object_id: document.querySelector(`#form-comment-create [name='object_id']`).value,
        settings_slug: document.querySelector(`#form-comment-create [name='settings_slug']`).value,
        //FORM INPUTS
        content: document.querySelector(`#${form_id} [name='content']`).value,
        is_spoiler: document.querySelector(`#${form_id} [name='is_spoiler']`).matches(':checked'),
        parent_id: document.querySelector(`#${form_id} [name='parent_id']`) ? (document.querySelector(`#${form_id} [name='parent_id']`).value) : null,
    };

    // AJAX
    let http = new XMLHttpRequest();
    http.open(method, action, true);

    http.setRequestHeader('Content-type', 'application/json');
    http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    http.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    http.onreadystatechange = function () {
        if (http.readyState === XMLHttpRequest.DONE) {
            if (http.status === 200) {
                if (status_check) {
                    document.getElementById('toast').classList.remove('hidden');
                }
                if (data.parent_id) {
                    let page = document.querySelector(`#form-comment-reply-${data.parent_id} [name='page']`).value;
                    LoadCommentList(page);
                } else {
                    ResetCreateCommentForm();
                    LoadCommentList();
                }
            } else {
                let textarea = document.querySelector(`#${form_id} textarea`);
                if (textarea.value.trim() !== '') {
                    alert('ERROR in Creating Comment!')
                }
            }
        }
    }
    http.send(JSON.stringify(data));
}

function CheckEditTextarea(form_id) {
    let textarea = document.querySelector(`#${form_id} textarea`)
    if (textarea.value.trim() === '') {
        textarea.classList.remove('border-textarea-bg-light', 'dark:border-textarea-bg-dark');
        textarea.classList.add('border-textarea-border-empty-light', 'dark:border-textarea-border-empty-dark');
    } else {
        textarea.classList.remove('border-textarea-border-empty-light', 'dark:border-textarea-border-empty-dark', 'animate-[pulse_500ms_linear_infinite]');
        textarea.classList.add('border-textarea-bg-light', 'dark:border-textarea-bg-dark');
    }
}

function EditComment(form_id, settings_slug, statusCheck) {
    let status_check = statusCheck === 'True'
    let form = document.querySelector(`#${form_id}`);
    let method = form.getAttribute('method');
    let action = form.getAttribute('action');
    let data = {
        //FORM INPUTS
        content: document.querySelector(`#${form_id} [name='content']`).value,
        is_spoiler: document.querySelector(`#${form_id} [name='is_spoiler']`).checked,
        urlhash: form_id.replace('form-comment-edit-', ''),
        settings_slug: settings_slug,
    };

    // AJAX
    let http = new XMLHttpRequest();
    http.open(method, action, true);

    http.setRequestHeader('Content-type', 'application/json');
    http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    http.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    http.onreadystatechange = function () {
        if (http.readyState === XMLHttpRequest.DONE) {
            if (http.status === 200) {
                if (status_check && http.response) {
                    document.getElementById('toast').classList.remove('hidden');
                }
                LoadComment(data.urlhash, settings_slug);
            } else {
                let textarea = document.querySelector(`#${form_id} textarea`);
                if (textarea.value.trim() === '') {
                    textarea.classList.remove('border-textarea-bg-light', 'dark:border-textarea-bg-dark');
                    textarea.classList.add('animate-[pulse_500ms_linear_infinite]', 'border-textarea-border-empty-light', 'dark:border-textarea-border-empty-dark');
                } else {
                    alert('ERROR in Creating Comment!')
                }
            }
        }
    }
    http.send(JSON.stringify(data));
}

function DeleteComment(urlhash) {
    let form = document.querySelector(`#form-comment-delete-${urlhash}`);
    let method = form.getAttribute('method');
    let action = form.getAttribute('action');

    // AJAX
    let http = new XMLHttpRequest();
    http.open(method, action, true);

    http.setRequestHeader('Content-type', 'application/json');
    http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    http.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    http.onreadystatechange = function () {
        if (http.readyState === XMLHttpRequest.DONE) {
            if (http.status === 200) {
                ResetDeleteCommentForm();
                LoadCommentList();
            } else {
                alert('ERROR in Deleting Comment!')
            }
        }
    }
    http.send();
}

function ReactComment(urlhash, react_slug) {
    let form = document.querySelector(`#form-comment-react-${urlhash}`);
    let method = form.getAttribute('method');
    let action = form.getAttribute('action');
    let data = {
        urlhash: urlhash,
        react_slug: react_slug
    }

    // AJAX
    let http = new XMLHttpRequest();
    http.open(method, action, true);

    http.setRequestHeader('Content-type', 'application/json');
    http.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    http.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    http.onreadystatechange = function () {
        if (http.readyState === XMLHttpRequest.DONE) {
            if (http.status === 200) {
                LoadCommentReactions(urlhash);
            }
        }
    }
    http.send(JSON.stringify(data));
}

function CloseToast() {
    document.getElementById('toast').classList.add('hidden');
}

document.addEventListener("DOMContentLoaded", () => {
    LoadCommentList(undefined, true);
});
