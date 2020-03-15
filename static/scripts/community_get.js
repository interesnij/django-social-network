$('#ajax').on('click', '.c_fullscreen', function() {item = $(this).parent();pk = item.attr("community-id");uuid = item.attr("item-id");$('#item_loader').html('').load("/communities/item/" + pk + "/" + uuid + "/"); $('.item_fullscreen').show();console.log("item community open")});

$('#ajax').on('click', '.show_staff_window', function() {btn = $(this).parents(".list-group-item");pk = btn.data("pk");uuid = btn.data("uuid");$('#load_staff_window').html('').load("/communities/manage/staff_window/" + pk + "/" + uuid + "/");$('.manage_window_fullscreen').show();console.log("community staff open");});

$('body').on('click', '.c_all_likes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_like/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("likes community open")});
$('body').on('click', '.c_all_dislikes', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_dislike/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("dislikes community open")});
$('body').on('click', '.c_all_reposts', function() {var btn = $(this); item = $(this).parents('.infinite-item');pk = item.attr("community-id");uuid = item.attr("item-id");$('#votes_loader').html('').load("/window/all_community_reposts/" + uuid + "/" + pk + "/"); $('.votes_fullscreen').show();console.log("reposts community open")});
$('#ajax').on('click', '#community_add', function() {$('#community_loader').html('').load("/communities/progs/add/");$('.community_fullscreen').show();console.log("add community open")})
$('#ajax').on('click', '#community_article_add', function() {btn = $(this);pk = btn.data('pk');$('#article_loader').html('').load("/article/add_community/" + pk + "/");$('.article_fullscreen').show();console.log("add community article open")})

on('#ajax', 'click', '.community_fullscreen_hide', function() {document.querySelector(".community_fullscreen").style.display = "none";document.getElementById("community_loader").innerHTML=""});
on('#ajax', 'click', '.community_manage_fullscreen_hide', function() {document.querySelector(".manage_window_fullscreen").style.display = "none";document.getElementById("load_staff_window").innerHTML=""});

$('body').on('click', '.c_comment.comments_close', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var uuid = item.attr("item-id"); var pk = item.attr("community-id"); var container = item.find(".load_comments");$.ajax({url: "/community/comment/" + uuid + "/" + pk + "/", data: {'uuid': uuid}, cache: false,beforeSend: function() {item.find(".load_comments").html("<span style='display:flex;justify-content: center;'><img src='/static/images/loading.gif'></span>");},success:function(data){container.html(data.comments);btn.addClass("comments_open").removeClass("comments_close");console.log("show comments community")}}); return false;});

$('body').on('click', '.c_comment.comments_open', function() {var btn = $(this); var item = btn.closest(".infinite-item"); var container = item.find(".load_comments");container.empty(); btn.removeClass('comments_open').addClass("comments_close");console.log("hide comments community")});


on('#ajax', 'click', '.c_article_detail', function() {
  parent = this.parentElement; parent2 = parent.parentElement;
  console.log(parent2);
  pk = parent2.attr("community-id");
  uuid = e.attr("item-id");
  loader = document.getElementById("article_loader");
  url = "/article/read/" + pk + "/" + uuid + "/"
  list_load(loader, url);
  loader.style.display = "block";
});
