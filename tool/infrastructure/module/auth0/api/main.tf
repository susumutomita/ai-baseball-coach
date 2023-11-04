resource "auth0_resource_server" "api" {
  name       = "${var.name}-${var.pre_fix}"
  identifier = var.identifier
}

resource "auth0_resource_server_scopes" "api" {
  resource_server_identifier = auth0_resource_server.api.identifier

  dynamic "scopes" {
    for_each = var.scopes
    content {
      name        = scopes.value.name
      description = scopes.value.description
    }
  }
}
