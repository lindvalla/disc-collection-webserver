// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const dataTableBody = document.querySelector('#data-table tbody');

    function updateTable(data) {
        dataTableBody.innerHTML = ''; // Clear current table content
        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="${document.querySelectorAll('#data-table thead th').length}">No results found.</td>`;
            dataTableBody.appendChild(row);
            return;
        }

        data.forEach(item => {
            const row = document.createElement('tr');
            item.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                row.appendChild(td);
            });
            dataTableBody.appendChild(row);
        });
    }

    searchInput.addEventListener('keyup', function() {
        const query = searchInput.value;
        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                updateTable(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    });
});

