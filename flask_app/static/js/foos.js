

// Button clink - > the browser will navigate back to the previous page they visited.
function goBack() {
    window.history.back();
}


// POP-UPS

function confirmPolicyDelete(policyId) {
    return confirm('Are you sure you want to delete policy ' + policyId + '?');
}

function confirmClaimDelete(claimId) {
    return confirm('Are you sure you want to delete claim ' + claimId + '?');
}
function confirmDeleteClient(clientName) {
    return confirm('Are you sure you want to delete client ' + clientName + '?');
}

function confirmPolicyRenew(policyId) {
    return confirm('Are you sure you want to renew policy ' + policyId + '?');
}

// drop down toogle for table
function toggleDetails(data) {
    var detailsRow = document.getElementById('details-' + data);
    if (detailsRow.style.display === 'none' || detailsRow.style.display === '') {
        detailsRow.style.display = 'table-row';
    } else {
        detailsRow.style.display = 'none';
    }
}

// drop down toogle for table
function toggleExpired(clientID) {
    var expiredRow = document.getElementById('expired-' + clientID);
    if (expiredRow.style.display === 'none') {
        expiredRow.style.display = '';
    } else {
        expiredRow.style.display = 'none';
    }
}

// adds a click event listener to each row in a table with the class and redirects to details
document.addEventListener('DOMContentLoaded', function() {
    var rows = document.querySelectorAll('.custom-table tbody tr');
    rows.forEach(function(row) {
        row.addEventListener('click', function() {
            window.location = row.getAttribute('data-href');
        });
    });
});