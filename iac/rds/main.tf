resource "aws_db_subnet_group" "main" {
  description = "private subnet group for $rds"
  subnet_ids  = var.private_subnet.*.id
  tags = {
    Name        = "${var.name}-private-subnet-group-${var.environment}"
    Environment = var.environment
  }
}


resource "aws_db_instance" "main" {
  allocated_storage      = 10
  name                   = var.db_name
  engine                 = "postgres"
  engine_version         = "14.1"
  instance_class         = "db.t3.micro"
  username               = var.db_user # "root"
  password               = var.db_pw   # "rootrootroot"
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = var.sg
  skip_final_snapshot    = true
  tags = {
    Name        = "${var.name}-db-instance-${var.environment}"
    Environment = var.environment
  }
}


output "db_host" {
  value = aws_db_instance.main.endpoint
}

output "db_port" {
  value = aws_db_instance.main.port
}
