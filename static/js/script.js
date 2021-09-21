$('#schedule').on('submit', (evt) => {
    evt.preventDefault();
    console.log('hey');

    const formData = {
        "startTime": $('[name="start_time"]').val(),
        "endTime": $('[name="end_time"]').val()
    };

    $.post("/api/reservations", formData, (res) => {
        $('#available_reservations').html("Here is the current availability:");
        for (time of res) {
            $('#available_reservations').append(
                `<form action="/reservations/book" method="POST">
                ${time} 
                <input value="${time}" name='start_time' type='submit'>
                </form>`);
        }
    })

})