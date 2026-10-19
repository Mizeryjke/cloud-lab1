output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "alb_public_url" {
  value = "http://${aws_lb.alb.dns_name}"
}