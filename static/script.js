// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    //const hidedvdInput = document.getElementById('hidedvd');
    //const hideblurayInput = document.getElementById('hidebluray');
    //const hide4kInput = document.getElementById('hide4k');
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
                td.innerHTML = cell;
                //td.textContent = cell;
                row.appendChild(td);
            });
            dataTableBody.appendChild(row);
        });
    }

    searchInput.addEventListener('keyup', function() {
        const query = searchInput.value;
        //const hidedvd = hidedvdInput.checked;
        //const hidebluray = hideblurayInput.checked;
        //const hide4k = hide4kInput.checked;
        //fetch(`/search?query=${encodeURIComponent(query)}&hidedvd=${hidedvd}&hidebluray=${hidevbluray}&hide4k=${hide4k}`)
        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                updateTable(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    });
});

