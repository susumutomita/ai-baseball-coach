resource "auth0_client" "application" {
  name        = "${var.client_name}-${var.pre_fix}"
  description = var.client_description
  app_type    = var.client_app_type
}
