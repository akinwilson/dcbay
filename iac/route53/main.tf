data "aws_route53_zone" "main" {
  name = var.domain_name
}

resource "aws_route53_record" "main" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = tolist(aws_acm_certificate.main.domain_validation_options)[0].resource_record_name
  type    = tolist(aws_acm_certificate.main.domain_validation_options)[0].resource_record_type
  records = [tolist(aws_acm_certificate.main.domain_validation_options)[0].resource_record_value]
  ttl     = var.ttl
}


resource "aws_route53_record" "alb" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "A"
  alias {
    name = var.alb.dns_name
    zone_id = var.alb.zone_id
    evaluate_target_health = true
  } 
}


resource "aws_acm_certificate" "main" {
  domain_name               = var.domain_name
  subject_alternative_names = ["*.${var.domain_name}"]
  validation_method         = "DNS"

  tags = {
    Name : var.domain_name
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [aws_route53_record.main.fqdn]
}

