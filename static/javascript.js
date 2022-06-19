document.addEventListener('DOMContentLoaded', function() {
    let type = document.querySelector('#type');
    let other = document.querySelector('#type-other');
    type.addEventListener('change', async function() {
        if (type.value === "그 외") {
            other.removeAttribute("readonly", "")
        }
        else {
            other.setAttribute("readonly", "")
        }
    })
    let building_type = document.querySelector("#building");
    let price_2 = document.querySelector("#price_2");
    building_type.addEventListener('change', async function() {
        if (building_type.value === "월세") {
            price_2.removeAttribute("readonly", "")
        }
        else {
            price_2.setAttribute("readonly", "")
        }
    })
});

function sendLink() {
    console.log("Yes");
}