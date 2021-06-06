on('#ajax', 'click', '.u_copy_survey_list', function() {
  on_off_list_in_collections(this, "/survey/user_progs/add_list_in_collections/", "u_uncopy_survey_list", "u_copy_survey_list", "Удалить")
});
on('#ajax', 'click', '.u_uncopy_survey_list', function() {
  on_off_list_in_collections(this, "/survey/user_progs/remove_list_from_collections/", "u_copy_survey_list", "u_uncopy_survey_list", "Добавить")
});

on('#ajax', 'click', '.u_add_survey', function() {
  loader = document.getElementById("create_loader");
  open_fullscreen('/survey/user_progs/add/', loader);
});

on('#create_loader', 'click', '#need_time_end', function() {
  this.parentElement.parentElement.nextElementSibling.classList.toggle("hide")
});

on('#create_loader', 'click', '.remove_answer', function() {
  this.parentElement.parentElement.parentElement.remove()
});
on('#create_loader', 'click', '.add_answer', function() {
  container = this.parentElement.parentElement.parentElement.parentElement
  answers = container.querySelectorAll(".answer");
  answers.length > 9 ? toast_error("Допустимо не больше 10 вариантов!") :
  (div = document.createElement("div"), div.classList.add("form-group"),
  div.innerHTML = '<div class="input-group"><input type="text" name="answers" placeholder="Вариант ответа" class="form-control answer"><div class="input-group-append"><span class="input-group-text custom_color pointer remove_answer">x</span></div></div>',
  container.append(div));
});
