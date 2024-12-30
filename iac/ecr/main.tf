resource "aws_ecr_repository" "main" {
  name                 = "${var.name}-mlflow-${var.environment}"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "main" {
  repository = aws_ecr_repository.main.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "keep last 1 images"
      action = {
        type = "expire"
      }
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 1
      }
    }]
  })
}

output "ecr_repo_url" {
  value = aws_ecr_repository.main.repository_url
}

output "dependency_on_ecr" {
  value = aws_ecr_repository.main
}