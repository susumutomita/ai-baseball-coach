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
