function generateInputs() {
    let num = parseInt($('#num_people').val());
    let html = '';
    for (let i = 1; i <= num; i++) {
        html += `
            <div class="form-row">
                <label>Person ${i} balance:</label>
                <input type="number" class="payment" step="0.01">
            </div>
        `;
    }
    $('#payments').html(html);
}


function solve() {
    let num = parseInt($('#num_people').val());
    let payments = [];
    $('.payment').each(function() {
        payments.push(parseFloat($(this).val()) || 0);
    });

    $.ajax({
        url: '/solve',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ num_people: num, payments: payments }),
        success: function(data) {
            let html = '';
            if (data.transactions.length === 0) {
                html = 'No transactions needed.';
            } else {
                data.transactions.forEach(t => {
                    html += `Person ${t.from} pays Person ${t.to} $${t.amount}<br>`;
                });
            }
            $('#results').html(html);
        }
    });
}