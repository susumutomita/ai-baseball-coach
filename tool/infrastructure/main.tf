resource "auth0_client" "application" {
  name            = "${var.client_name}-${var.pre_fix}"
  description     = var.client_description
  app_type        = var.client_app_type
  callbacks       = [for domain in var.callback_domains : "${domain}${var.callback_path}"]
  oidc_conformant = var.oidc_conformant

  jwt_configuration {
    alg                 = var.jwt_alg
    lifetime_in_seconds = var.jwt_lifetime_in_seconds
  }
}
