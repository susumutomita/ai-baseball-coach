# # terraform module creating auth0 resources
module "auth0-app" {
  source                  = "./module/auth0/application"
  client_name             = var.client_name
  client_description      = var.client_description
  client_app_type         = var.client_app_type
  callback_domains        = var.callback_domains
  callback_path           = var.callback_path
  oidc_conformant         = var.oidc_conformant
  pre_fix                 = var.pre_fix
  jwt_alg                 = var.jwt_alg
  jwt_lifetime_in_seconds = var.jwt_lifetime_in_seconds
}

module "auth0-api" {
  source = "./module/auth0/api"
  name   = var.client_name
}
