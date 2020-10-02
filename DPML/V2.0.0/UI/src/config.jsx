const server_url = `http://localhost:5001`
const dpml_config = {
  // User
  user_login_url: `${server_url}/login`,
  user_logout_url: `${server_url}/logout`,
  user_refresh_url: `${server_url}/refresh`,

  // Image processing
  img_upload_image_url: `${server_url}/upload_image`,
  img_upload_3d_image_url: `${server_url}/upload_3d_image`,
  img_get_all_unit_url: `${server_url}/get_all_unit`,

  // Log
  log_get_log_url: `${server_url}/get_log`,
  log_get_min_max_date_url: `${server_url}/get_min_max_date`,
  log_add_log_url: `${server_url}/add_log`,

  // Model management
  model_add_model_url: `${server_url}/add_model`,
  model_edit_model_url: `${server_url}/edit_model`,
  model_delete_model_url: `${server_url}/delete_model`,
  model_change_active_model_url: `${server_url}/change_active_model`,
  model_check_duplicate_name_url: `${server_url}/check_duplicate_name`,
  model_get_all_model_url: `${server_url}/get_all_model`,
  model_get_all_unit_url: `${server_url}/get_all_unit`,
};

export {dpml_config}