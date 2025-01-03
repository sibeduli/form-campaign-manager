document.addEventListener('DOMContentLoaded', function() {
    $('#guest-campaign-form').submit(function (e){
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData.entries());
        const uuid = $('#uuid').val();
        $.ajax({
            url: '/api/campaign?guest_submission=true',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                if (response.status === 'success') {
                    window.location.href = `/guest-status/${uuid}`;
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                alert('Error: ' + error);
            }
        });
    });
}); 