# Cafe-Nimbus — Design Decisions

> Architectural rationale for the AWS infrastructure choices made in this case study.

---

## Application Load Balancer (ALB) — Public Subnet

**Decision:** Place the ALB in public subnets across two Availability Zones.

**Rationale:** The ALB is the only internet-facing entry point for the application. Placing it in public subnets allows it to receive inbound traffic from Route 53 while keeping all EC2 instances and the database in private subnets with no public IPs. This is the standard AWS pattern for web applications — the load balancer absorbs the public exposure so nothing behind it has to.

**Alternative considered:** CloudFront in front of the ALB. Rejected for this scale — CloudFront adds latency optimization and DDoS protection but introduces unnecessary complexity for a single-region café web application.

---

## Auto Scaling Group — Demand-Based Scaling

**Decision:** CPU utilization trigger, not a schedule.

**Rationale:** Café traffic is promotion-driven, not time-predictable. A scheduled scale-out at 12PM assumes lunch rush happens on a schedule — it doesn't. CPU-based scaling responds to actual demand: when a promotional post goes viral at 9AM on a Tuesday, the ASG responds within 90 seconds. A schedule would miss it.

**Minimum instances:** 2 (one per AZ) maintained at all times. A single-instance minimum is a single point of failure regardless of how many AZs are configured.

---

## S3 — Static Asset Hosting

**Decision:** Serve all static assets (images, CSS, JS) from S3, not from EC2.

**Rationale:** EC2 instances should process application logic, not serve files. Moving static assets to S3 reduces EC2 CPU load, eliminates per-request compute cost for assets that never change, and provides automatic redundancy. S3 versioning enables instant rollback if a bad asset deployment goes out.

---

## RDS — Private Subnet Only

**Decision:** RDS deployed in private subnets with no public accessibility.

**Rationale:** A database with a public IP is an attack surface. RDS in a private subnet is only reachable from within the VPC — specifically from the EC2 security group. Even if every other security control fails, the database is not reachable from the internet. This is non-negotiable for any application handling customer data.

---

## Lambda + EventBridge — Serverless Reporting

**Decision:** Lambda triggered by EventBridge for daily order reporting, not a cron job on EC2.

**Rationale:** A cron job on EC2 runs 24/7 to execute a task that takes 30 seconds once per day. Lambda runs only when triggered — at this workload, the monthly cost is effectively zero. EC2-based cron also dies when the instance is terminated or replaced by the ASG. EventBridge + Lambda is stateless, independently scalable, and decoupled from the compute layer entirely.

---

## SNS — Notification Delivery

**Decision:** SNS for order notification delivery, not SES directly from Lambda.

**Rationale:** SNS allows multiple subscribers — email, SMS, SQS, Lambda — from a single publish call. Starting with SNS means notification channels can be expanded without changing the Lambda function. SES would lock the notification pipeline to email only.

---

## CloudWatch — Centralized Monitoring

**Decision:** CloudWatch for all logs and metrics across ALB, EC2, RDS, and Lambda.

**Rationale:** A single observability platform for the entire stack. ALB access logs, EC2 application logs, RDS performance insights, and Lambda execution logs all flow to CloudWatch. A single dashboard shows the full operational picture — no tool-switching required during an incident.

---

## VPC Public/Private Subnet Separation

**Decision:** Public subnets for ALB and NAT Gateways only. Private subnets for EC2, RDS, and all application components.

**Rationale:** Defense in depth. Even if the ALB is compromised, the application layer has no public IPs and cannot be reached directly. Even if an EC2 instance is compromised, the database can only be reached from the EC2 security group — not from the compromised instance's public address. Each layer can only be reached through the layer above it.

**NAT Gateways:** One per AZ for outbound-only internet access from private subnets (OS updates, package installs, API calls). NAT Gateway ensures private resources can initiate outbound connections without accepting inbound ones.

---

*Cafe-Nimbus is a fictional portfolio case study. Architecture decisions reflect real-world AWS best practices.*
