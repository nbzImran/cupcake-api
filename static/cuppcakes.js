const Base_url = "/api/cupcakes";


// Fetch and display all cupcakes

async function fethcCupcakes() {
    const response = await axios.get(Base_url);
    const cupcakes = response.data.cupcakes;

    for (let cupcake of cupcakes) {
        appendCupcakeToList(cupcake);
    }
}




// Add a cupcakes to the list
function appendCupcakeToList(cupcake) {
    const image = cupcake.image || "https://via.placeholder.com/150";

    const $cupcake = $(`
    <li>
        <img src="${cupcake.image}" alt="${cupcake.flavor}" width="100">
        ${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}/5
    </li>
    `);
    $("#cupcake-list").append($cupcake);
}


// Handle form submission
$(document).ready(function () {
    $("#new-cupcake-form").on("submit", async function (e) {
    e.preventDefault();

        const flavor = $("#flavor").val().trim();
        const size = $("#size").val().trim();
        const rating = $("#rating").val().trim();
        const image = $("#image").val().trim() || "https://tinyurl.com/demo-cupcake";


        const data = { flavor, size, rating, image };
    

        try {
            const response = await axios.post(Base_url, data);

            const newCupcake = response.data.cupcake;
            appendCupcakeToList(newCupcake);
        
            $("#new-cupcake-form")[0].reset();
        } catch (err) {
        }

    })
})
fethcCupcakes();
