# terraform module creating auth0 resources
module "auth0" {
  source = "./module/auth0"
  client_name = var.client_name
  client_description = var.client_description
  client_app_type = var.client_app_type
  client_id = var.client_id
  client_secret = var.client_secret
  callback_domains = var.callback_domains
  callback_path = var.callback_path
  domain = var.domain
  jwt_alg = var.jwt_alg
  jwt_lifetime_in_seconds = var.jwt_lifetime_in_seconds
}
