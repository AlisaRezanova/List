let isFormOpen = false;
let currentItemId = null;


export function open(item = null, category = null){
    const TaskForm = document.getElementById("Form");
    const titleInput = document.getElementById("Title");
    const fullTextInput = document.getElementById("TitleNote");
    const ratingInput = document.getElementById("TitleRating");
    const suggestionsList = document.getElementById("suggestions");
    TaskForm.style.display = 'flex';

    if (item && item.id){
        currentItemId = item.id;
        titleInput.value = item.title;
        fullTextInput.value = item.note;
        ratingInput.value = item.own_rating;
    } else {
        currentItemId = null;
        titleInput.value = "";
        fullTextInput.value = "";
        ratingInput.value = "";
    }

    titleInput.addEventListener("input", function () {
        if (titleInput.value.length < 3 || !category) {
            suggestionsList.innerHTML = "";
            suggestionsList.style.display = "none";
            return;
        }
        console.log(`Category: ${category}`);
        fetch(`/search_title_in_category?input_name=${encodeURIComponent(titleInput.value)}&category=${encodeURIComponent(category)}`)
            .then((response) => response.json())
            .then((data) => {
                const suggestions = data.titles;
                suggestionsList.innerHTML = "";

                if (suggestions.length > 0) {
                    suggestions.forEach((suggestion) => {
                        const suggestionItem = document.createElement("li");
                        suggestionItem.textContent = suggestion.title;
                        suggestionItem.style.cursor = "pointer";
                        suggestionItem.onclick = () => {
                            titleInput.value = suggestion.title;
                            suggestionsList.innerHTML = "";
                            suggestionsList.style.display = "none";
                        };
                        suggestionsList.appendChild(suggestionItem);
                    });
                    suggestionsList.style.display = "block";
                } else {
                    suggestionsList.style.display = "none";
                }
            })
            .catch(() => {
                suggestionsList.innerHTML = "";
                suggestionsList.style.display = "none";
            });
    });

    isFormOpen = true;
}


export function close_form(){
    if (isFormOpen) {
        const TaskForm = document.getElementById("Form");
        TaskForm.style.display = 'none';
        isFormOpen = false;
    }
}


export function save_form(){
    const titleInput = document.getElementById("Title");
    const fullTextInput = document.getElementById("TitleNote");
    const ratingInput = document.getElementById("TitleRating");
    const newItem = {
        title: titleInput.value,
        note: fullTextInput.value,
        own_rating: ratingInput.value,
    };
    if (!newItem.title || !newItem.note || !newItem.own_rating) {
        alert("Заполните все поля!");
        return;
    }
    const url = currentItemId ? `/update_item/${currentItemId}` : "/add_item";
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(newItem),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert(currentItemId ? "Запись обновлена!" : "Запись добавлена!");
            } else {
                alert("Ошибка при сохранении записи.");
            }
        })
        .catch(() => alert("Ошибка при отправке запроса."))
        .finally(() => close_form());
}

function fetchSuggestions(currentCategory=null) {
    const titleInput = document.getElementById("Title");
    const suggestionsList = document.getElementById("suggestions");
    const category = currentCategory;

    if (titleInput.value.length < 3) {
        suggestionsList.innerHTML = "";
        suggestionsList.style.display = "none";
        return;
    }
    console.log(`Category: ${category}`);
    fetch(`/search_title_in_category?input_name=${encodeURIComponent(titleInput.value)}&category=${category}`)
        .then((response) => response.json())
        .then((data) => {
            const suggestions = data.titles;
            suggestionsList.innerHTML = "";

            if (suggestions.length > 0) {
                suggestions.forEach((suggestion) => {
                    const suggestionItem = document.createElement("li");
                    suggestionItem.textContent = suggestion.title;
                    suggestionItem.style.cursor = "pointer";
                    suggestionItem.onclick = () => {
                        titleInput.value = suggestion.title;
                        suggestionsList.innerHTML = "";
                        suggestionsList.style.display = "none";
                    };
                    suggestionsList.appendChild(suggestionItem);
                });
                suggestionsList.style.display = "block";
            } else {
                suggestionsList.style.display = "none";
            }
        })
        .catch(() => {
            suggestionsList.innerHTML = "";
            suggestionsList.style.display = "none";
        });
}


function getCSRFToken() {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    return csrfToken;
}