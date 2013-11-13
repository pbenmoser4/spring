function sendQuery(send_val) {
    $.ajax({
        type:"POST",
        url: $('#return').attr('function-url'), // add post url
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            item: send_val
        },
        success: function(data){
            // if the post function executes correctly, views.py will return a JSON encoded
            // string containing the return from the sarch query. Here we decode it and post
            // it to the appropriate place in the site.
            for(var i=0; i<10; i++){
                if (data[i]['thumbnail_link'] == null) {
                    addRedditNoThumb(data[i]['link'],data[i]['title']);
                } else {
                    addRedditThumb(data[i]['link'],data[i]['thumbnail_link'],data[i]['title']);
                }
            }
        },
        error: function(xhr, textStatus, errorThrown){
            alert("There's been an error in the request: " + errorThrown + textStatus + xhr)
        }
    });
}

function addRedditNoThumb(link, title){
    retval = '<div class="rnt redd">';
    retval = retval + '<a href="' + link + '" target="_blank">' + title + '</a>';
    retval = retval + '</div>';
    $('#return').append(retval);
}

function addRedditThumb(link, thumb, title){
    var retval = '<div class="rt redd">';
    retval = retval + '<a href="' + link + '" target="_blank" class="rtl"><img src="' + thumb + '"></a>';
    retval = retval + '<div class="rtt">';
    retval = retval + '<a href="' + link + '" target="_blank">' + title + '</a>';
    retval = retval + '</div></div>';
    $('#return').append(retval);
}