const API = "http://127.0.0.1:5000";
const socket = io(API);

function loadProducts() {
    fetch(API + "/products")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("productTable");
            if (!table) return;

            table.innerHTML = "";
            data.forEach(p => {
                table.innerHTML += `
                    <tr>
                        <td>${p.id}</td>
                        <td>${p.name}</td>
                        <td>${p.price}</td>
                        <td>${p.quantity}</td>
                    </tr>
                `;
            });
        });
}

function addProduct() {
    fetch(API + "/add-product", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("name").value,
            price: document.getElementById("price").value,
            quantity: document.getElementById("qty").value
        })
    }).then(() => {
        alert("Product Added");
        loadProducts();
    });
}

socket.on("inventory_updated", () => {
    loadProducts();
});

loadProducts();
