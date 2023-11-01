variable "client_name" {
  description = "The name of the Auth0 client"
  type        = string
  default     = "ai-baseball-coach"
}

variable "client_description" {
  description = "The description of the Auth0 client"
  type        = string
  default     = "ai-baseball-coach"
}

variable "client_app_type" {
  description = "The type of the Auth0 client app"
  type        = string
  default     = "regular_web"
}

variable "callback_domains" {
  description = "List of callback domains"
  type        = list(string)
  default     = ["http://127.0.0.1:8080", "http://localhost:8080"]
}

variable "callback_path" {
  description = "Callback path"
  type        = string
  default     = "/callback"
}

variable "jwt_alg" {
  description = "The algorithm used to sign the JWT"
  type        = string
  default     = "RS256"
}

variable "jwt_lifetime_in_seconds" {
  description = "The lifetime of the JWT in seconds"
  type        = number
  default     = 36000
}

variable "oidc_conformant" {
  description = "Specify if the client is OIDC Conformant"
  type        = bool
  default     = true
}

variable "pre_fix" {
  description = "Prefix for the Auth0 client"
  type        = string
  default     = "test"
}
