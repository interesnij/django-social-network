$(function () {

    $("#replyPosts").click(function () {
        $.ajax({
            url: '/posts/posts/post-comment/',
            data: $("#replyPostsForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $("#replyInput").val("");
                $("#postThreadModal").modal("hide");
            },
            error: function(data){
                alert(data.responseText);
            },
        });
    });

    $("div.stream").on("click", ".comment", function () {
        var post = $(this).closest(".card");
        var posts = $(post).closest("div").attr("posts-id");
        $("#newsThreadModal").modal("show");
        $.ajax({
            url: '/posts/get-thread/',
            data: {'posts': posts},
            cache: false,
            beforeSend: function () {
                $("#threadContent").html("<li class='loadcomment'><img src='/static/images/loading.gif'></li>");
            },
            success: function (data) {
                $("input[name=parent]").val(data.uuid)
                $("#postsContent").html(data.posts);
                $("#threadContent").html(data.thread);
            }
        });
        return false;
    });
});
