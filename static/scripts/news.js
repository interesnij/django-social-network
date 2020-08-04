on('#ajax', 'click', '.u_news_fullscreen', function() {
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = container.getAttribute("data-pk");
  loader = document.getElementById("item_loader");
  open_fullscreen("/users/detail/post/" + pk + "/" + uuid + "/", loader)
})

on('#ajax', 'click', '.c_news_fullscreen', function() {
  uuid = this.parentElement.getAttribute('data-uuid');
  pk = this.parentElement.getAttribute('data-pk');
  loader = document.getElementById("item_loader");
  open_fullscreen("/communities/item/" + pk + "/" + uuid + "/", loader)
}); 
