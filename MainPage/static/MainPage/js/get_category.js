let isFormOpen = false;
import { open } from './form.js'
let currentCategory = null;

document.addEventListener('DOMContentLoaded', function () {
    const dropdownContent = document.getElementById("categories-list");
    const itemList = document.getElementById("item-list");
    const dropdownButton = document.querySelector(".dropdown-btn");

    fetch("/get_all_category")
        .then(response => response.json())
        .then(data => {
            const categories = data.content_types;
            dropdownContent.innerHTML = '';
            categories.forEach(category => {
                const categoryItem = document.createElement("a");
                categoryItem.href = "#";
                categoryItem.classList.add("category-item");
                categoryItem.dataset.id = category.id;
                categoryItem.textContent = category.name;
                dropdownContent.appendChild(categoryItem);
            });
        })
        .catch(() => {
            const errorItem = document.createElement("a");
            errorItem.href = "#";
            errorItem.textContent = "Ошибка при загрузке категорий";
            dropdownContent.appendChild(errorItem);
        });

    document.addEventListener("click", function (e) {
        const img = document.getElementById('img1');
        if (e.target && e.target.matches(".category-item")) {
            e.preventDefault();
            if (img) {
                img.style.display = "none";
            }

            currentCategory = e.target.textContent;
            dropdownButton.textContent = currentCategory;

            const categoryId = e.target.dataset.id;
            fetch(`/get_all_list_in_category/${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    itemList.innerHTML = '';
                    const items = data.items;
                    if (items.length > 0) {
                        items.forEach(item => {
                            const itemDiv = document.createElement("div");
                            itemDiv.classList.add("item");
                            const itemName = document.createElement("h3");
                            itemName.textContent = item.title;
                            itemDiv.appendChild(itemName);
                            const itemImg = document.createElement("img");
                            itemImg.src = item.img;
                            itemImg.alt = item.title;
                            itemImg.classList.add("item-image");
                            itemDiv.appendChild(itemImg);
                            const itemRating = document.createElement("p");
                            itemRating.textContent = `Моя оценка: ${item.own_rating}`;
                            itemDiv.appendChild(itemRating);

                            const Rating = document.createElement("p");
                            Rating.textContent = `Рейтинг: ${item.rating}`;
                            itemDiv.appendChild(Rating);

                            itemDiv.addEventListener('click', () =>{

                                open(item, currentCategory);
                            });

                            itemList.appendChild(itemDiv);



                        });
                    } else {
                        const noItemsMessage = document.createElement("h2");
                        noItemsMessage.textContent = "Здесь пока пусто";
                        itemList.appendChild(noItemsMessage);
                    }
                })
                .catch(() => {
                    const errorMessage = document.createElement("p");
                    errorMessage.textContent = "Ошибка при загрузке";
                    itemList.appendChild(errorMessage);
                })
                .finally(() => {
                    const addButton = document.createElement("button");
                    addButton.innerHTML = "&#43;";
                    addButton.id = "add-title-button";
                    addButton.className = "btn btn-add";
                    addButton.addEventListener("click", () => {
                        open(null, currentCategory);
                    });
                    if (!document.getElementById("add-title-button")) {
                        itemList.appendChild(addButton);
                    }
                });
        }
    });
});