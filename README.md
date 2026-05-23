# Café Nimbus — AWS Cloud Infrastructure Case Study

### Five-Phase AWS Architecture · From One Broken Server to a Self-Operating Cloud

**Md Rahat Islam Anik · Self-Directed Case Study · 2025**

[![Live Case Study](https://img.shields.io/badge/Live%20Case%20Study-View%20Now-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://rahatislamanik-spec.github.io/Cafe-Nimbus)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-rahatislamanik-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/rahatislamanik)
[![GitHub](https://img.shields.io/badge/GitHub-rahatislamanik--spec-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rahatislamanik-spec)

---

| 5 Phases | 13 AWS Services | Multi-AZ | 0 Manual Steps |
|:---:|:---:|:---:|:---:|

---

> *"Café Nimbus came to me with one broken server and no plan for growth. I left them with an infrastructure that scales automatically, recovers from failures without human intervention, and reports on itself every morning — without anyone touching a keyboard."*

---

## The Engagement

Café Nimbus is a growing café brand preparing for national expansion. When this engagement began, their entire online presence ran on a single EC2 instance — no redundancy, no backups, no plan for what happens when traffic spikes during a promotion. One bad day and the whole operation goes dark.

The mandate: build an AWS infrastructure that could grow with the business, survive failures automatically, and operate with as little manual intervention as possible.

What followed was a five-phase architectural engagement. Each phase solved a specific business problem. Each phase made the next one possible.

---

## Five Phases

### Phase 01 — Get Online
**Amazon S3 · Versioning · Lifecycle Policies · Cross-Region Replication**

**The Problem:** Café Nimbus had no web presence. Customers were finding competitors instead. The site needed to be fast, cheap to run, and impossible to accidentally break during a content update.

**What Was Built:** Static website on Amazon S3 with public access controlled entirely through bucket policy. S3 versioning enabled from day one. Lifecycle policies to transition older versions to S3-IA after 30 days. Cross-region replication as a day-one non-negotiable.

**Validated:**
- Site live via S3 endpoint
- 403 confirmed before policy — access correctly blocked
- File deleted and restored in under 60 seconds
- Replication: object in destination bucket within 30 seconds

> **The principle:** Replication from day one, not after the first outage. The cost of preventing a disaster is always lower than the cost of recovering from one.

---

### Phase 02 — Get Dynamic
**EC2 · LAMP Stack · AMI Golden Image · Multi-Region Deployment**

**The Problem:** A static site can display a menu. It cannot take orders, manage inventory, or run a real application. Café Nimbus needed a backend — and one that could be reproduced exactly if it ever had to be rebuilt.

**What Was Built:** EC2 running a full LAMP stack — Linux, Apache, MySQL, PHP. After validating end-to-end (menu, order placement, data persistence), a golden AMI was created before touching anything else. From that AMI, an identical instance was launched in a second region in minutes.

**Validated:**
- LAMP stack deployed, Apache accessible
- Menu items loading correctly, orders persisted to database
- AMI created from configured instance
- Second instance from AMI in alternate region — identical

> **The principle:** A manually configured server is a liability. An AMI is an asset. The cost of creating it is an hour. The cost of not having it is a full rebuild under pressure.

---

### Phase 03 — Get Secure
**Custom VPC · Bastion Host · NAT Gateway · Network ACLs**

**The Problem:** The platform was going public with no meaningful network boundaries — everything was reachable from everywhere. Security had to be layered. A single misconfigured security group should not be enough to expose the entire backend.

**What Was Built:** Custom VPC with /16 CIDR. Public subnet for ALB and bastion only. Private subnet for all application servers and the database — no public IPs, ever. NAT Gateway for outbound-only private traffic. Network ACLs as a stateless second layer of defence on top of security groups.

**Validated:**
- Private instances unreachable via direct connection
- Bastion SSH confirmed as only entry path
- NAT Gateway routing confirmed for private outbound
- NACL deny rules blocked traffic as expected

> **The principle:** No backend resource ever gets a public IP. A single misconfigured security group without NACLs as a backstop is one mistake from a complete exposure.

---

### Phase 04 — Get Scalable
**Application Load Balancer · Auto Scaling Group · Multi-AZ**

**The Problem:** A single EC2 instance — no matter how well configured — is a single point of failure. When traffic spikes during a promotion, the site goes down. When the instance fails, the business goes dark. Neither is acceptable for a company preparing for national expansion.

**What Was Built:** Application Load Balancer across two Availability Zones. Auto Scaling Group triggered by CPU utilization — not a schedule. Minimum instances maintained at all times, scale-out on threshold breach, scale-in when load drops. Health checks replace failed instances automatically.

**Validated:**
- ALB distributing traffic across both AZs
- Load simulation triggered scale-out within 90 seconds
- Instance manually terminated mid-test — no visible service interruption
- ASG replaced terminated instance automatically
- Scale-in confirmed when load dropped

> **The principle:** Multi-AZ is not a luxury. A single-AZ deployment with ten instances is still a single point of failure. Two AZs with two instances each is genuinely resilient.

---

### Phase 05 — Get Autonomous
**AWS Lambda · Amazon SNS · Amazon EventBridge**

**The Problem:** Every morning, the operations team spent 45 minutes manually pulling the previous day's sales data and emailing it to management. Error-prone, time-consuming, and entirely unnecessary.

**What Was Built:** Two Lambda functions — `DataExtractor` (queries RDS inside the VPC) and `SalesAnalysisReport` (formats and delivers the report). SNS email topic for the operations distribution list. EventBridge rule fires at 8AM daily — no human involved, no idle compute.

**Validated:**
- DataExtractor confirmed connecting to RDS within VPC
- Sales data pulled and formatted correctly
- SNS subscription confirmed active
- Lambda manually triggered — email delivered within 30 seconds
- EventBridge scheduled execution confirmed

> **The principle:** Lambda, not a cron job on EC2. Lambda runs only when triggered — monthly cost at this workload is effectively zero. An EC2-based cron costs $15–30/month to idle 24/7 for a task that executes once per day. Serverless is not always the right answer. Here, it is the only answer.

---

## Architecture Decision Log

| Decision | Chosen | Rejected | Rationale |
|---|---|---|---|
| Static hosting | S3 + bucket policy | EC2-hosted static site | No reason to run compute for files that never change |
| Content protection | S3 versioning day one | No versioning | Accidental overwrites have no recovery path without it |
| Regional resilience | Cross-region replication | Single-region only | One regional outage = total web presence loss |
| Server reproducibility | AMI before second deploy | Manual reconfiguration | A manually built server cannot be rebuilt reliably under pressure |
| Backend access | Bastion host only | Direct SSH + public IP | No backend resource should ever have a direct public route |
| Outbound private traffic | NAT Gateway | Public subnet for EC2s | Private isolation requires outbound-only — not bidirectional |
| Network defence | SGs + NACLs combined | Security groups alone | One misconfigured SG without NACLs = open door |
| Scaling trigger | CPU utilization | Scheduled scaling | Traffic is demand-driven, not time-predictable |
| AZ strategy | Multi-AZ ALB + ASG | Single-AZ more instances | Single AZ is a single point of failure regardless of instance count |
| Reporting automation | Lambda + EventBridge | Cron job on EC2 | Idle compute 24/7 for a 30-second daily task |

---

## Tech Stack

| Service | Role |
|---|---|
| Amazon S3 | Static hosting, versioning, lifecycle policies, cross-region replication |
| Amazon EC2 | Application compute, LAMP stack, bastion host |
| Amazon VPC | Network isolation, public/private subnet segmentation |
| Internet Gateway | Public subnet internet access |
| NAT Gateway | Outbound-only internet access for private subnet |
| Network ACLs | Stateless subnet-level traffic control |
| Application Load Balancer | Traffic distribution across AZs, health checking |
| Auto Scaling Group | Demand-based compute scaling, auto instance replacement |
| AWS Lambda | Serverless data extraction and report generation |
| Amazon RDS | Managed MySQL database for application data |
| Amazon SNS | Email notification delivery for sales reports |
| Amazon EventBridge | Scheduled Lambda trigger — 8AM daily |
| AWS AMI | Golden image capture for reproducible deployments |

---

## What I'd Add in Production

**AWS WAF on ALB** — The load balancer is publicly exposed. Without a Web Application Firewall, SQL injection and XSS have no automated defence at the network edge.

**RDS + Secrets Manager** — In a hardened environment, RDS credentials would be rotated automatically through Secrets Manager — no application code would contain a hardcoded password.

**CloudTrail — All Regions** — Every API call in the account should be logged. Without CloudTrail, there is no audit trail if something goes wrong.

**VPC Endpoints for S3** — Traffic between EC2 and S3 currently routes through NAT Gateway. VPC Endpoints keep that traffic on the AWS private network and eliminate the NAT cost.

**CloudWatch Dashboard** — ALB request count, ASG instance count, Lambda errors, and RDS connections — all visible in one place, with SNS alarms on threshold breach.

**WAF + Shield** — For a nationally expanding brand, DDoS protection at the ALB layer moves from a nice-to-have to a business continuity requirement.

---

## Skills Demonstrated

`Amazon S3` · `EC2` · `VPC Design` · `Subnetting` · `Bastion Host` · `NAT Gateway` · `Network ACLs` · `Security Groups` · `Application Load Balancer` · `Auto Scaling` · `Multi-AZ Architecture` · `AWS Lambda` · `Amazon RDS` · `Amazon SNS` · `Amazon EventBridge` · `AMI` · `LAMP Stack` · `Cross-Region Replication` · `Serverless Architecture` · `Infrastructure Design`

---

## The Result

- **Serves static content globally** from S3 with automatic regional failover — no server, no maintenance
- **Runs a dynamic application** on compute that rebuilds itself from a golden image — reproducible by design
- **Isolates every backend resource** behind a secure network boundary — no public IPs, no direct routes, two layers of control
- **Scales automatically** in response to real traffic — not a schedule someone set and forgot
- **Reports on itself every morning at 8AM** without a single manual step — Lambda, SNS, EventBridge, working while no one is watching

The infrastructure does not need a human to survive a failure. It does not need a human to handle a traffic spike. And it does not need a human to send the morning sales report. **That was the mandate. That is the result.**

---

## Live Case Study

The full interactive case study — with architecture diagrams, per-phase documentation, and the complete decision log — is published at:

**[rahatislamanik-spec.github.io/Cafe-Nimbus](https://rahatislamanik-spec.github.io/Cafe-Nimbus)**

---

## Author

**Md Rahat Islam Anik**
Cloud Computing & Network Administration · George Brown College · May 2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/rahatislamanik)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?style=flat&logo=github)](https://github.com/rahatislamanik-spec)
