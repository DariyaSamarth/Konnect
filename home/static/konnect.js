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


let UpvoteBtn = document.getElementsByClassName('upvoter')
for(let i =0;i<UpvoteBtn.length;i++){
    let post_id = UpvoteBtn[i].id
    UpvoteBtn[i].addEventListener('click',()=>{
        Upvoter(post_id,UpvoteBtn[i])
    });
}

function Upvoter(post_id,button){
    console.log(button.innerHTML)
    console.log(post_id)
    console.log('clicked upvo9te button')
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
            
            console.log('PUT request successful');
            let obj = JSON.parse(xhr.response)
            console.log(obj['upvotes']);
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