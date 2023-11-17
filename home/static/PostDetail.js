console.log("JS file connected")

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


let UpvoteBtn = document.getElementsByClassName('postupvoter')
for(let i =0;i<UpvoteBtn.length;i++){
    let post_id = UpvoteBtn[i].id
    UpvoteBtn[i].addEventListener('click',()=>{
        Upvoter(post_id,UpvoteBtn[i])
    });
}

function Upvoter(post_id,button){
    
    let xhr = new XMLHttpRequest()

    xhr.open('PUT','../upvote-post/',true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader("x-csrftoken", getCookie('csrftoken'));
    let data = {
        post_id: post_id,
    };


    
    let jsonData = JSON.stringify(data);

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            
            let obj = JSON.parse(xhr.response)
            button.innerHTML = "Upvote "+obj['upvotes']
        } else {
            console.error('PUT request failed with status:', xhr.status);
        }
    };
    
    xhr.onerror = function () {
        console.error('Network error occurred');
    };
    

    xhr.send(jsonData);
}


$(document).ready(function() {
    console.log('Jquery loaded')

    $('.postdownvoter').click(function(){

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

    $('.commentdownvoter').click(function(){

        let clickedElement = $(this);

        data = {
            comment_id:this.id
        }

        $.ajax({
            url: '../downvote-comment/',
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

    $('.commentupvoter').click(function(){

        let clickedElement = $(this);

        data = {
            comment_id:this.id
        }

        $.ajax({
            url: '../upvote-comment/',
            method: 'PUT',
            dataType: 'json',
            data: data,
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            success: function(data) {
              // Handle the successful response
              clickedElement.html('Upvote ' + data.upvotes);
            },
            error: function(xhr, status, error) {
              // Handle errors
              console.error('AJAX request failed: ' + status + ', ' + error);
            }
          });
    })

})