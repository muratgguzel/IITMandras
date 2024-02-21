terraform {
  required_version = ">= 0.12.26"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "test-vpc" {
    cidr_block = "10.0.0.0/16"
    enable_dns_support = "true" #gives you an internal domain name
    enable_dns_hostnames = "true" #gives you an internal host name
    enable_classiclink = "false"
    instance_tenancy = "default"    
    
    tags =  {
        Name = "test-vpc"
    }
}

resource "aws_subnet" "public-subnet1" {
    vpc_id = "${aws_vpc.test-vpc.id}"
    cidr_block = "10.0.1.0/24"
    map_public_ip_on_launch = "true" //it makes this a public subnet
    availability_zone = "us-east-1a"
    tags = {
        Name = "public-subnet1"
    }
}

resource "aws_subnet" "public-subnet2" {
    vpc_id = "${aws_vpc.test-vpc.id}"
    cidr_block = "10.0.2.0/24"
    map_public_ip_on_launch = "true" //it makes this a public subnet
    availability_zone = "us-east-1b"
    tags = {
        Name = "public-subnet2"
    }
}

resource "aws_internet_gateway" "test-igw" {
    vpc_id = "${aws_vpc.test-vpc.id}"
    tags = {
        Name = "test-igw"
    }
}

resource "aws_route_table" "public-rt" {
    vpc_id = "${aws_vpc.test-vpc.id}"
    
    route {
        cidr_block = "0.0.0.0/0" 
        gateway_id = "${aws_internet_gateway.test-igw.id}" 
    }
    
    tags = {
        Name = "public-rt"
    }
}

resource "aws_route_table_association" "crta-public-subnet-1"{
    subnet_id = "${aws_subnet.public-subnet1.id}"
    route_table_id = "${aws_route_table.public-rt.id}"
}

resource "aws_route_table_association" "crta-public-subnet-2"{
    subnet_id = "${aws_subnet.public-subnet2.id}"
    route_table_id = "${aws_route_table.public-rt.id}"
}



resource "aws_instance" "frontend1" {
  ami                    = "ami-0747bdcabd34c712a"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]
  subnet_id = "${aws_subnet.public-subnet1.id}"
  key_name = "kp-dev-server"

  tags = {
    Name = "frontend1"
  }
}

resource "aws_instance" "backend1" {
  # Ubuntu Server 18.04 LTS (HVM), SSD Volume Type in us-east-1
  ami                    = "ami-0747bdcabd34c712a"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]
  subnet_id = "${aws_subnet.public-subnet1.id}"
  key_name = "kp-dev-server"

  tags = {
    Name = "backend1"
  }
}

resource "aws_instance" "frontend2" {
  # Ubuntu Server 18.04 LTS (HVM), SSD Volume Type in us-east-1
  ami                    = "ami-0747bdcabd34c712a"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]
  subnet_id = "${aws_subnet.public-subnet2.id}"
  key_name = "kp-dev-server"

  tags = {
    Name = "frontend2"
  }
}

resource "aws_instance" "backend2" {
  # Ubuntu Server 18.04 LTS (HVM), SSD Volume Type in us-east-1
  ami                    = "ami-0747bdcabd34c712a"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]
  subnet_id = "${aws_subnet.public-subnet2.id}"
  key_name = "kp-dev-server"

  tags = {
    Name = "backend2"
  }
}

resource "aws_security_group" "instance" {
  name = "terraform-example-instance"
  vpc_id = "${aws_vpc.test-vpc.id}"


  egress {
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound HTTP from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_lb" "test" {
  name               = "test-lb-tf"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.instance.id]
  subnets            = [aws_subnet.public-subnet1.id,aws_subnet.public-subnet2.id]

  tags = {
    Name = "test"
  }
}


resource "aws_dynamodb_table" "test-dynamodb-table" {
  name           = "Test-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "UserId"
  range_key      = "GameTitle"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "GameTitle"
    type = "S"
  }

  attribute {
    name = "TopScore"
    type = "N"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  global_secondary_index {
    name               = "GameTitleIndex"
    hash_key           = "GameTitle"
    range_key          = "TopScore"
    write_capacity     = 10
    read_capacity      = 10
    projection_type    = "INCLUDE"
    non_key_attributes = ["UserId"]
  }

  tags = {
    Name        = "Test-table"
  }
}
