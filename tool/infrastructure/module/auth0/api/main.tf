resource "auth0_resource_server" "api" {
  name       = "${var.name}-${var.pre_fix}"
  identifier = var.identifier
}
