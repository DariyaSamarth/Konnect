
$(document).ready(function() {
    console.log('Jquery loaded')
    $('.downvoter').click(function(){

        let clickedElement = $(this);

        data = {
            post_id:this.id
        }

        $.ajax({
            url: '../downvote-post/',
            method: 'PUT',
            dataType: 'json',
            data: data,
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            success: function(data) {
              // Handle the successful response
              clickedElement.html('Downvote ' + data.downvotes);
            },
            error: function(xhr, status, error) {
              // Handle errors
              console.error('AJAX request failed: ' + status + ', ' + error);
            }
          });
    })
})