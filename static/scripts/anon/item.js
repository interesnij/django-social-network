$('#ajax .stream').on('click', '.article_detail', function() {
    var item = $(this); var item_id = item.data("id");
    $('#article_loader').html('').load("/article/detail/" + item_id); $('.article_fullscreen').show();
});
$('#ajax').on('click', '.fullscreen', function() {
    var item = $(this); var item_pk = item.data("pk"); var user_uuid = item.data("uuid");
    $('#item_loader').html('').load("/users/detail/item/" + item_pk + "/" + user_uuid + "/"); $('.item_fullscreen').show();
});
$('#ajax').on('click', '.c_fullscreen', function() {
    var item = $(this); var pk = item.data("pk"); var uuid = item.data("uuid");
    $('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();
});

$('#ajax').on('click', '#R_U', function() {console.log("click"); var item = $(this); var item_id = item.data("uuid"); $('#user_item_pk').html(item_id);});

$('.user_page').on('click', '.avatar_detail', function() {
		var photo = $(this); var photo_id = photo.data("id"); var user_uuid = photo.data("uuid");
		$('#photo_loader').html('').load("/gallery/load/avatar_detail/" + photo_id + "/" + user_uuid + "/"); $('.photo_fullscreen').show();
});
$('.photo_fullscreen_hide').on('click', function() { $('.photo_fullscreen').hide(); $('#photo_loader').empty(); });
$('.item_fullscreen_hide').on('click', function() { $('.item_fullscreen').hide(); $('#item_loader').empty(); });
$('.article_fullscreen_hide').on('click', function() {$('.article_fullscreen').hide(); $('#article_loader').empty();});

$('#ajax').on('click', '.show_replies', function() { var element = $(this); element.next().toggleClass('replies_open'); });

$('#ajax').on('click', '.u_comment.comments_close', function() {
    var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = btn.data('pk'); var container = item.find(".load_comments")
    $.ajax({
        url: "/user/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,
        beforeSend: function() { item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>"); },
        success: function(data) { container.html(data.comments); btn.addClass("comments_open").removeClass("comments_close")}
    }); return false;
});
$('#ajax').on('click', '.u_comment.comments_open', function() {
  var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments"); container.empty(); btn.removeClass('comments_open').addClass("comments_close");
});
$('#ajax').on('click', '.js-textareacopybtn', function() {
  btn = $(this);
  link = btn.find('.js-copytextarea');
  link.focus();
  link.select();
  console.log(link)
try {
  var successful = document.execCommand('copy');
  var msg = successful ? 'successful' : 'unsuccessful';
  console.log('Copying text command was ' + msg);
} catch (err) {
  console.log('Oops, unable to copy');
}
});
