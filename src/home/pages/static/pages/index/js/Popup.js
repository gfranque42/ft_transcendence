const modal = document.getElementById("myModal");
const openModalBtn = document.getElementById("openModalBtn");
const closeModalBtn = document.getElementById("closeModalBtn");
const content = document.querySelector(".content");

// Function to open the modal
openModalBtn.onclick = function() {
    modal.style.display = "flex";
    content.classList.add("blur");
};

// Function to close the modal
closeModalBtn.onclick = function() {
    modal.style.display = "none";
    content.classList.remove("blur");
};

// Close the modal if the user clicks outside of the modal content
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
        content.classList.remove("blur");
    }
};