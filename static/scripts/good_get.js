on('#ajax', 'click', '.u_good_detail', function() {
  var container, uuid, pk, loader;
  container = this.parentElement;
  uuid = container.getAttribute('data-uuid');
  pk = this.getAttribute('data-id');
  loader = document.getElementById("good_loader");
  open_fullscreen('/goods/user/good/' + pk + '/' + uuid + '/', loader)
});

$('#ajax').on('click', '#c_good_add', function() {
  $('#good_add_loader').html('').load("{% url 'good_add_community' pk=user.pk %}");
  $('.good_add_fullscreen').show();
})
on('#ajax', 'click', '#c_good_add', function() {
  var container, pk, loader;
  container = this.parentElement;
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("good_add_loader");
  open_fullscreen('/goods/community/add/' + pk + '/', loader)
});
on('#ajax', 'click', '#u_good_add', function() {
  var container, pk, loader;
  container = this.parentElement;
  pk = this.getAttribute('data-pk');
  loader = document.getElementById("good_add_loader");
  open_fullscreen('/goods/user/add/' + pk + '/', loader)
});
