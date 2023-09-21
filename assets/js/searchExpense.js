const searchField = document.querySelector('#search-field');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const pagination = document.querySelector('.pagination-container');
const tbody = document.querySelector('.table-body');

tableOutput.style.display = "none";

searchField.addEventListener('keyup', (e) => {
    pagination.style.display = 'none';
    const searchValue = e.target.value.trim(); // Trim the search value

    if (searchValue.length > 0) {
        console.log(searchValue);
        tbody.innerHTML = "";
        fetch("/search-expenses", {
                body: JSON.stringify({ searchText: searchValue }),
                method: 'POST',
            })
            .then((res) => res.json())
            .then(data => {
                console.log("data : ", data);
                tableOutput.style.display = 'block';
                appTable.style.display = 'none';

                if (data.length === 0) {
                    console.log('Fasle');
                    tableOutput.innerHTML = "No results found"
                } else {
                    console.log('true');
                    data.forEach(createTable);

                    function createTable(item) {
                        tbody.innerHTML += `
                    <tr>
                     <td>${item.amount}</td>
                     <td>${item.category}</td>
                     <td>${item.description}</td>
                     <td>${item.date}</td>
                    </tr>
                    `
                    }
                }
            });
    } else {
        appTable.style.display = 'block';
        pagination.style.display = 'block';
        tableOutput.style.display = 'none';
    }

});