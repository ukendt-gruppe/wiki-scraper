variable "project_name" {
  type    = string
  default = "wiki-scraper"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "location" {
  type    = string
  default = "northeurope" 
}

variable "vm_size" {
  type    = string
  default = "Standard_B1s" 
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "ssh_public_key" {
  type = string
  # You'll provide this when running Terraform
}