variable "api_scopes" {
  description = "The list of scopes to grant to the client for the API"
  type        = list(string)
  default     = ["read:data", "read:messages", "write:data"]
}

variable "client_id" {
  description = "The client ID of the application"
  type        = string
}

variable "name" {
  description = "The name of the Auth0 client"
  type        = string
  default     = "ai-baseball-coach"
}

variable "identifier" {
  description = "List of callback domains"
  type        = string
  default     = "ai-baseball-coach"
}

variable "pre_fix" {
  description = "Prefix for the Auth0 client"
  type        = string
  default     = "test"
}

variable "scopes" {
  description = "The list of permissions for the resource server"
  type = list(object({
    name        = string
    description = string
  }))
  default = [
    {
      name        = "read:data",
      description = "Read data"
    },
    {
      name        = "read:messages",
      description = "Read messages"
    }
  ]
}
