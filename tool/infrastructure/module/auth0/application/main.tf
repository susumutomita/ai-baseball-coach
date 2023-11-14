resource "auth0_client" "application" {
  allowed_logout_urls = var.logout_urls
  app_type            = var.client_app_type
  callbacks           = [for domain in var.callback_domains : "${domain}${var.callback_path}"]
  description         = var.client_description
  jwt_configuration {
    alg                 = var.jwt_alg
    lifetime_in_seconds = var.jwt_lifetime_in_seconds
  }
  name            = "${var.client_name}-${var.pre_fix}"
  oidc_conformant = var.oidc_conformant
}
