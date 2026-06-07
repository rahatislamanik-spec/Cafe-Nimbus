# Evidence Note

The original AWS console screenshots from the initial Cafe-Nimbus build are not currently available.

This repository contains the architecture documentation, design rationale, and sample automation code that formed the basis of the case study. The Lambda function, design decisions, and architecture diagram reflect the actual infrastructure pattern that was built.

AWS console screenshots will be added when the environment is safely rebuilt in a trial account. All resources will be deployed in a single region with a strict budget alert, documented, screenshotted, and then fully decommissioned to avoid ongoing cost.

Current artifacts in this repository:
- Full case study documentation in README.md
- Architecture diagram (Mermaid, embedded in README)
- Design decisions rationale (DESIGN-DECISIONS.md)
- Lambda order notification function (lambda/order_notification.py)

*Cafe-Nimbus is a fictional portfolio case study.*
