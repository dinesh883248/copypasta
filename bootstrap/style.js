"use strict";

// Select all nav-link elements inside nav-pills
const navItems = document.querySelectorAll('.nav-pills .nav-item .nav-link:not(.active)');

// Function to set background color on hover
function makeActive(element) {
    element.classList.add("active", "bg-primary-subtle", "text-bg-light");
}

function makeInActive(element) {
    element.classList.remove("active", "bg-primary-subtle", "text-bg-light");
}

// Add event listeners to each nav-item
navItems.forEach(item => {
    item.addEventListener('mouseover', () => makeActive(item)); // Set your desired background color
    item.addEventListener('mouseout', () => makeInActive(item)); // Reset to default on mouse out
});
