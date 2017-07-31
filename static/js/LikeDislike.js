(function (){
    'use strict';
    $(document).ready(function(){

        $('.like-message').click(function(){
        alert("Pressed a like button");

        var request = $.ajax({
            url: "http://127.0.0.1:8000/like/",
            method: "POST",
            data: {
            id: $(this).attr("data-messageid"),
            like: 1
            }
        });

        var button = $(this);
        request.done(function(){
            alert("SUCCES");

            if (button.attr.style == "color:green"){
            button.attr("style","color:none");
            } else {
            button.attr("style","color:green");
            }
        });

        request.fail(function(){
            alert("FAILLLL");
        });
        });





        $('.dislike-message').click(function(){
        alert("Pressed a dislike button");

        var request = $.ajax({
            url: "http://127.0.0.1:8000/like/",
            method: "POST",
            data: {
            id: $(this).attr("data-messageid"),
            like: 0
            }
        });


        var button = $(this);
        request.done(function(){
            alert("SUCCES");

            if (button.attr.style == "color:red"){
            button.attr("style","color:none");
            } else {
            button.attr("style","color:red");
            }

        });

        request.fail(function(){
            alert("FAILLLL");
        });

        });

    });
})();