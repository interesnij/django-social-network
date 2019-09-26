$(function () {

  $('#postFormModal').on('shown.bs.modal', function () {
      $('#postInput').trigger('focus')
  });

  $('#postThreadModal').on('shown.bs.modal', function () {
      $('#replyInput').trigger('focus')
  });



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

    });
