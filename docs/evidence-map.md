# Cafe Nimbus Evidence and Validation Map

Cafe Nimbus is currently presented as an AWS architecture and production-readiness case study. This repository does not include retained AWS console screenshots, infrastructure-as-code, Lambda source code, CloudWatch metrics, or load-test output.

## Evidence Status

| Area | Current repo evidence | What would strengthen it |
|---|---|---|
| Architecture overview | Inline architecture diagram in `index.html` | Exported diagram under `assets/diagrams/` |
| S3 static hosting | README and live case-study narrative | S3 bucket, versioning, lifecycle, and replication screenshots |
| EC2 LAMP and AMI | README and live case-study narrative | EC2 instance, Apache/PHP test, AMI, and launch-from-AMI screenshots |
| VPC segmentation | README and live case-study narrative | VPC, subnet, route table, security group, NACL, and bastion screenshots |
| ALB and Auto Scaling | README and live case-study narrative | ALB target group, ASG policy, health check, and scaling event screenshots |
| Lambda/SNS/EventBridge reporting | README and live case-study narrative | Lambda code, EventBridge rule, SNS subscription, and delivered-report screenshots |
| Production hardening | Production gaps documented | WAF, CloudTrail, Secrets Manager, VPC endpoint, and CloudWatch dashboard evidence |

## Validation Plan

| Phase | Validation to capture |
|---|---|
| Phase 01 - Static hosting | Confirm site access, pre-policy access denial, object version restore, and cross-region replication |
| Phase 02 - Dynamic application | Confirm Apache/PHP availability, database persistence, AMI creation, and launch-from-AMI consistency |
| Phase 03 - Network segmentation | Confirm private instances have no direct internet ingress, bastion or Session Manager access, NAT egress, and NACL behavior |
| Phase 04 - Scaling and availability | Confirm ALB target health, cross-AZ routing, controlled scale-out, instance replacement, and scale-in |
| Phase 05 - Reporting automation | Confirm Lambda invocation, report generation, SNS delivery, and EventBridge scheduled run |

## Current Presentation Guidance

Until these artifacts are added, Cafe Nimbus should be described as:

- AWS infrastructure architecture case study
- production-readiness review
- service-selection and tradeoff documentation
- validation plan for a future implementation

It should not be described as a fully evidenced AWS deployment unless implementation artifacts are added.

