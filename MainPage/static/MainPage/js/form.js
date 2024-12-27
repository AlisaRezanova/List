export function open(item = null){
    const TaskForm = document.getElementById("Form");
    const titleInput = document.getElementById("Title");
    const fullTextInput = document.getElementById("TitleNote");
    const ratingInput = document.getElementById("TitleRating");
    TaskForm.style.display = 'flex';

    if (item.id){
        currentItemId = item.id;
        titleInput = item.title;
        fullTextInput = item.note;
        ratingInput = item.own_rating;
    } else {
        currentItemId = null;
        titleInput = "";
        fullTextInput = "";
        ratingInput = "";
    }
    isFormOpen = true;
}