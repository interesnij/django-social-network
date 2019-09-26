
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

    $( "#post_hard" ).click(function(){
      $('#post_create').html('').load("/posts/add_hard/");
    })

    $( "#post_medium" ).click(function(){
      $('#post_create').html('').load("/posts/add_medium/");
    })

    $( "#post_lite" ).click(function(){
      $('#post_create').html('').load("/posts/add_lite/");
    });

      function like() {
          var like = $(this);
          var post = $('.infinite-item').attr("posts-id");
          var type = like.data('type');
          var pk = like.data('id');
          var action  = like.data('action');
          var dislike = like.next().next();
          payload = {
              'post': post,
              'csrf_token': csrftoken
            }
          $.ajax({
              url: "/posts/like/" + pk + "/",
              type: 'POST',
              cache: false,
              data: payload,
              success: function(data) {
                  like.find("[data-count='like']").text(data.like_count);
                  dislike.find("[data-count='dislike']").text(data.dislike_count);
                  $(like).addClass("text-success");

                  $(dislike).removeClass("text-danger");
                  $(like).siblings('.like_window').html('').load("/posts/like_window/" + pk + "/");
                  $(dislike).siblings('.dislike_window').html('').load("/posts/dislike_window/" + pk + "/")
              }
          });
          return false;
      }
      function dislike() {
          var dislike = $(this);
          var post = $('.infinite-item').attr("posts-id");
          var type = dislike.data('type');
          var pk = dislike.data('id');
          var action = dislike.data('action');
          var like = dislike.prev().prev();
          payload = {
              'post': post,
              'csrf_token': csrftoken
            }
          $.ajax({
              url: "/posts/dislike/" + pk + "/",
              type: 'POST',
              cache: false,
              data: payload,
              success: function(data) {
                  dislike.find("[data-count='dislike']").text(data.dislike_count);
                  like.find("[data-count='like']").text(data.like_count);
                  $(dislike).addClass("text-danger");
                  $(like).removeClass("text-success");
                  $(like).siblings('.like_window').html('').load("/posts/like_window/" + pk + "/");
                  $(dislike).siblings('.dislike_window').html('').load("/posts/dislike_window/" + pk + "/")
              }
          });
          return false;
      }
      // Подключение обработчиков
      $('[data-action="like"]').click(like);
      $('[data-action="dislike"]').click(dislike);

  function remove() {
    var remove = $(this);
    var pk = remove.data('id');
    var type = remove.data('type');

  $.ajax({
      url: "/posts/delete/" + pk + "/",
      success: function (data) {
        $(remove).parents('.card').hide();
        $.toast({
            heading: '{{ request.user.first_name }}',
            text: type + ' успешно удален!',
            showHideTransition: 'fade',
            icon: 'error'
        })
      },
      error: function(data) {
      }
  });
  };

  $('[data-action="remove"]').click(remove);

  $(".comment").on("click", function () {
      var post = $(this).closest(".card").attr("posts-id");
      var posts = $(post).closest("li").attr("posts-id");
      $("#postThreadModal").modal("show");
      console.log(post);
      $.ajax({
          url: '/posts/get-thread/',
          data: {'post': post},
          cache: false,
          beforeSend: function () {
              $("#threadContent").html("<li class='loadcomment'><img src='/static/images/loading.gif'></li>");
          },
          success: function (data) {
              $("input[name=parent]").val(data.uuid)
              $("#postsContent").html(data.post);
              $("#threadContent").html(data.thread);
          }
      });
      return false;
  });
