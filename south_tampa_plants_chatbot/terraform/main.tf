terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
}


resource "aws_security_group" "allow_ssh_http" {
  name        = "allow_ssh_http"
  description = "Allow SSH and HTTP inbound traffic"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # ⚠️ Allow SSH from anywhere — OK for testing only
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "app_server" {
  ami           = "ami-0c101f26f147fa7fd"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]  # 🔥 Attach the security group

  user_data = <<-EOF
    #!/bin/bash
    set -ex
    sudo touch TESTFILE
    sudo yum update -y
    sudo yum install docker -y
    sudo yum install git -y
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker
    [ -d south-tampa-plants-chatbot ] || git clone https://github.com/michaelthegreat/south-tampa-plants-chatbot
    cd south-tampa-plants-chatbot/south_tampa_plants_chatbot
    git pull
    sudo docker-compose -f docker-compose.local.yml build
    sudo docker-compose -f docker-compose.local.yml up -d
  EOF


  tags = {
    Name = "ExampleAppServerInstance"
  }
}
