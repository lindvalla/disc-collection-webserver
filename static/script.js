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

async function autoUploadFile() {
    const fileInput = document.getElementById('fileInput');
    const uploadLabel = document.getElementById('uploadLabel');
    const spinner = document.getElementById('loadingSpinner');

    const file = fileInput.files[0]; // Get the selected file

    if (!file) return; // Exit if user cancels file selection

    // 1. UI Changes: Show spinner and disable the button click
    spinner.style.display = 'flex';
    uploadLabel.style.pointerEvents = 'none';
    uploadLabel.style.opacity = '0.5';

    // Prepare form data
    const formData = new FormData();
    formData.append('data_file', file);

    try {
        // Send file to Flask backend
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            // Success message from backend
            alert(`Success: ${result.message}`);
            window.location.reload(); // Reloads page on clicking OK
        } else {
            // Failure message from backend (e.g., parsing error)
            alert(`Error: ${result.message}`);
            resetUI();
        }
    } catch (error) {
        // Network or server connection error
        alert('An unexpected error occurred during upload.');
        console.error(error);
        resetUI();
    }
    // Helper function to restore the UI if the upload fails
    function resetUI() {
        spinner.style.display = 'none';
        uploadLabel.style.pointerEvents = 'auto';
        uploadLabel.style.opacity = '1';
        fileInput.value = ''; // Clear file so it can be re-selected
    }
}

