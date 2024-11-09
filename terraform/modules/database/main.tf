resource "azurerm_network_interface" "db" {
  name                = "${var.resource_prefix}-db-nic"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id         = azurerm_public_ip.db.id
  }
}

resource "azurerm_network_security_group" "db" {
  name                = "${var.resource_prefix}-db-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name

  security_rule {
    name                       = "PostgreSQL"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range         = "*"
    destination_port_range    = "5432"
    source_address_prefix     = "*"  # Tighten this in production
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "SSH"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range         = "*"
    destination_port_range    = "22"
    source_address_prefix     = "*"  # Tighten this in production
    destination_address_prefix = "*"
  }
}

resource "azurerm_linux_virtual_machine" "db" {
  name                = "${var.resource_prefix}-db-vm"
  location            = var.location
  resource_group_name = var.resource_group_name
  size                = var.vm_size
  admin_username      = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.db.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  custom_data = base64encode(<<-EOF
              #!/bin/bash
              
              # Update and install packages
              apt-get update
              apt-get install -y docker.io docker-compose git
              
              # Start and enable Docker
              systemctl start docker
              systemctl enable docker
              
              # Add azureuser to docker group
              usermod -aG docker azureuser
              
              # Create directory for PostgreSQL data
              mkdir -p /home/azureuser/postgres-data
              chown -R 999:999 /home/azureuser/postgres-data
              
              # Clone specific branch
              git clone -b feature/deploydatabase https://github.com/ukendt-gruppe/wiki-scraper.git /home/azureuser/wiki-scraper
              chown -R azureuser:azureuser /home/azureuser/wiki-scraper
              
              # Start PostgreSQL
              cd /home/azureuser/wiki-scraper/docker
              docker-compose -f docker-compose.prod.yml up -d
              EOF
  )
}

resource "azurerm_public_ip" "db" {
  name                = "${var.resource_prefix}-db-ip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                = "Standard"
}

resource "azurerm_network_interface_security_group_association" "db" {
  network_interface_id      = azurerm_network_interface.db.id
  network_security_group_id = azurerm_network_security_group.db.id
}