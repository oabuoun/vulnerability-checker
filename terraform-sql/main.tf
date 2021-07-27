terraform {
  required_providers {
    aws = {
     source = "hashicorp/aws"
     version = "~>3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_default_vpc" "Eng88_sql_server_vpc_tf" {

}

data "aws_subnet_ids" "Eng88_sql_server_subnet_tf"{
  vpc_id = aws_default_vpc.Eng88_sql_server_vpc_tf.id
}

resource "aws_security_group" "Eng88_sql_server_security_group_tf" {
  name = "Eng88_sql_server_security_group"

  vpc_id = aws_default_vpc.Eng88_sql_server_vpc_tf.id


  ingress {
    from_port = 8099
    to_port = 8099
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol= -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "aws_private_key" {
  default = "/home/kali/.ssh/cyber-jenkins-key.pem"
}


resource "aws_instance" "Eng88_sql_server_instance_tf" {
  ami                         = "ami-0f89681a05a3a9de7"
  instance_type               = "t2.micro"
  subnet_id                   = tolist(data.aws_subnet_ids.Eng88_sql_server_subnet_tf.ids)[0]
  associate_public_ip_address = true
  key_name                    = "cyber-jenkins-key"
  vpc_security_group_ids      = [aws_security_group.Eng88_sql_server_security_group_tf.id]

  connection {
    type = "ssh"
    host = self.public_ip
    user = "ec2-user"
    private_key = file("/home/kali/.ssh/cyber-jenkins-key.pem")

  }

  provisioner "file" {
    source = "../init-scripts"
    destination = "/tmp/init-scripts"
  }
  provisioner "file" {
    source = "../.my_sql_password"
    destination = "/tmp/.my_sql_password"
  }
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init-scripts/docker_install.sh",
      "/tmp/init-scripts/docker_install.sh",
    ]
  }
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init-scripts/my_sql_install.sh",
      "/tmp/init-scripts/my_sql_install.sh",
    ]
  }
  provisioner "file" {
    source = "../init-sql"
    destination = "/tmp"
  }
  provisioner "remote-exec" {
    when = destroy
    inline = [
      "chmod +x /tmp/init-scripts/stop.sh",
      "/tmp/init-scripts/stop.sh",
    ]
  }
}

resource "aws_volume_attachment" "Eng88_sql_server_db_volume_attachment_tf" {
  device_name = "/dev/xvdz"
  volume_id = "vol-0e32e0dd6a7e660f4"
  instance_id = aws_instance.Eng88_sql_server_instance_tf.id
  skip_destroy = true

  connection {
    type = "ssh"
    host = aws_instance.Eng88_sql_server_instance_tf.public_ip
    user = "ec2-user"
    private_key = file(var.aws_private_key)
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init-scripts/mount.sh",
      "/tmp/init-scripts/mount.sh"
    ]
  }
  provisioner "remote-exec" {
    inline = [
      "cd /tmp/init-scripts/",
      "chmod +x launch.sh",
      "./launch.sh"
    ]
  }
}
