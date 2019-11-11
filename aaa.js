$(document).ready(function() {
  $('#form_album_add').bootstrapValidator({
      fields: {
          title: {
              validators: {
                      stringLength: {
                      min: 2,
                  },
                      notEmpty: {
                      message: 'Придумайте название альбома'
                  }
              }
          }
        }
});
      .on('success.form.bv', function(e) {
          $('#contact_form').data('bootstrapValidator').resetForm();
          e.preventDefault();

          var $form = $(e.target);

          var bv = $form.data('bootstrapValidator');

          $.post($form.attr('action'), $form.serialize(), function(result) {
              console.log(result);
          }, 'json');
});
