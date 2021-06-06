on('#ajax', 'click', '.c_copy_survey_list', function() {
  on_off_list_in_collections(this, "/survey/community_progs/add_list_in_collections/", "c_uncopy_survey_list", "c_copy_survey_list", "Удалить")
});
on('#ajax', 'click', '.c_uncopy_survey_list', function() {
  on_off_list_in_collections(this, "/survey/community_progs/remove_list_from_collections/", "c_copy_survey_list", "c_uncopy_survey_list", "Добавить")
});

on('#ajax', 'click', '.u_add_survey', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen('/survey/user_progs/add/', loader);
});
