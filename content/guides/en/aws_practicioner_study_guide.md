## AWS Certified Cloud Practitioner Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![AWS Certified Cloud Practitioner study guide: about 200 questions](../../images/aws_practicioner_guide_title_img.png)

About 200 questions and short answers I used to prepare the AWS Certified Cloud Practitioner exam (CLF-C02), which I passed in October 2026. They follow the exam's four domains: cloud concepts, security and compliance, cloud technology and services, and billing, pricing and support. Open a question to see its answer, or use the filter to search the whole guide. Service details and prices change, so check the AWS documentation before relying on a number.

<!-- QA -->

### Cloud concepts

#### What is cloud computing?

The on-demand delivery of IT resources (compute, storage, databases, networking, software) over the internet with pay-as-you-go pricing. Instead of buying and running data centers, you rent capacity from a provider and release it when you no longer need it.

#### What are the six advantages of cloud computing according to AWS?

1. Trade fixed expense (capital expense) for variable expense.
2. Benefit from massive economies of scale.
3. Stop guessing capacity.
4. Increase speed and agility.
5. Stop spending money running and maintaining data centers.
6. Go global in minutes.

#### What are the different cloud deployment models supported by AWS?

- **Cloud (cloud-native):** everything runs in the public cloud.
- **On-premises (private cloud):** resources in your own data center, often with virtualization and resource-management tools. AWS Outposts brings AWS infrastructure on premises.
- **Hybrid:** cloud resources connected to on-premises infrastructure, for example during a migration or for data that must stay on site.

#### What do IaaS, PaaS and SaaS mean? Give AWS examples.

- **IaaS (Infrastructure as a Service):** you get virtual machines, storage and networks and manage the operating system and everything above it. Example: Amazon EC2.
- **PaaS (Platform as a Service):** the provider runs the infrastructure and platform, you deploy code. Example: AWS Elastic Beanstalk.
- **SaaS (Software as a Service):** a complete application used over the internet. Examples: Amazon WorkMail, Amazon Chime, Amazon QuickSight.

#### What is elasticity?

The ability to acquire resources when you need them and release them when you don't, automatically following demand. Example: an Auto Scaling group that adds EC2 instances during a traffic spike and removes them afterwards.

#### What is scalability?

The ability of a system to handle a growing load by adding resources. Scaling up (vertical) means bigger resources, scaling out (horizontal) means more resources. Elasticity is scalability that also scales back down automatically.

#### What is the difference between scaling vertically and horizontally?

Vertical scaling replaces a resource with a larger one (a bigger instance type). It is simple but has a ceiling and often needs a restart. Horizontal scaling adds more resources of the same size behind a load balancer. It has no practical ceiling and improves availability.

#### What are some advantages of using AWS instead of on-premises infrastructure?

No upfront hardware purchase, pay only for what you use, capacity in minutes instead of months, global reach, managed services that remove undifferentiated work (patching, backups), built-in security and compliance certifications, and the ability to experiment cheaply and shut down what fails.

#### What is the difference between CapEx and OpEx?

Capital expenditure (CapEx) is an upfront investment in physical assets, such as servers, depreciated over years. Operational expenditure (OpEx) is ongoing spending on services. The cloud turns most IT CapEx into OpEx.

#### What does "economies of scale" mean in the cloud?

AWS buys hardware, power and network at a scale no single customer can, so its cost per unit is lower. Part of the saving is passed on through lower prices, which AWS has reduced many times.

#### What is high availability?

The ability of a system to keep working with minimal downtime when components fail. On AWS it usually means running across several Availability Zones so the loss of one data center doesn't stop the application.

#### What is fault tolerance?

The ability to keep operating without interruption when a component fails, typically through redundant components that take over automatically. It is a stronger property than high availability, which may accept a short interruption.

#### What is disaster recovery, and what are RTO and RPO?

Disaster recovery (DR) is the set of plans for restoring a workload after a major failure. The Recovery Time Objective (RTO) is the maximum acceptable downtime. The Recovery Point Objective (RPO) is the maximum acceptable data loss, measured in time.

#### What are the four disaster recovery strategies on AWS, from cheapest to fastest?

1. **Backup and restore:** data is backed up, infrastructure is created after the disaster. Hours of RTO.
2. **Pilot light:** a minimal core (for example a replicated database) runs all the time, the rest is started on demand.
3. **Warm standby:** a scaled-down but fully working copy runs and is scaled up on failover.
4. **Multi-site active/active:** full production in two or more Regions. Near-zero RTO, highest cost.

#### What is agility in the context of the cloud?

The speed at which you can provide resources and try new ideas. Resources that took weeks to procure are available in minutes, so the cost and time of experimenting fall sharply.

#### What does "go global in minutes" mean?

You can deploy an application in AWS Regions around the world with a few clicks or API calls, giving users lower latency without building data centers in other countries.

#### What is a managed service?

A service where AWS operates the underlying infrastructure and software (provisioning, patching, backups, scaling) and you only use it. Amazon RDS is a managed database. Running a database on EC2 is not managed: you do all of that yourself.

#### What does "serverless" mean?

You run code or use a service without provisioning or managing servers. Capacity scales automatically and you pay for actual use. Examples: AWS Lambda, Amazon S3, Amazon DynamoDB, AWS Fargate, Amazon Athena.

#### What is the AWS Cloud Adoption Framework (AWS CAF)?

Guidance that helps organizations plan a cloud transformation. It groups capabilities into six perspectives: Business, People, Governance (business-focused) and Platform, Security, Operations (technical).

#### What are the 7 Rs of migration?

Retire, Retain, Rehost ("lift and shift"), Relocate (for example VMware Cloud on AWS), Repurchase (move to SaaS), Replatform ("lift, tinker and shift", such as moving to RDS) and Refactor/re-architect (rebuild as cloud-native).

### Global infrastructure and the Well-Architected Framework

#### How is AWS global infrastructure structured?

In Regions (separate geographic areas), each made of several Availability Zones (isolated groups of data centers). Edge locations and Regional edge caches serve CloudFront and Route 53 close to users. Local Zones, Wavelength Zones and Outposts extend AWS closer to users or on premises.

#### What is the difference between an AWS Region and an Availability Zone?

A Region is a geographic area, such as eu-west-3 (Paris), that contains several Availability Zones. An Availability Zone (AZ) is one or more discrete data centers with redundant power, networking and connectivity, physically separated from the other AZs of the Region but linked to them by low-latency networking.

#### How many Availability Zones does a Region have?

At least three for most Regions (new Regions are built with three or more). Deploying across at least two AZs is the baseline for high availability.

#### What four factors should you consider when choosing a Region?

1. **Compliance and data residency:** legal requirements may force data to stay in a country.
2. **Proximity to users:** lower latency.
3. **Service availability:** not every service or feature is in every Region.
4. **Pricing:** the same service can cost different amounts in different Regions.

#### What is an edge location?

A site that runs CloudFront caches and Route 53 DNS (and services such as Lambda@Edge) close to end users. There are many more edge locations than Regions.

#### What is a Local Zone?

An extension of a Region placed near a large city, running selected services (such as EC2 and EBS) to give single-digit millisecond latency to users there.

#### What is AWS Wavelength?

Infrastructure embedded in telecom providers' 5G networks, so applications can reach mobile devices with very low latency.

#### What is AWS Outposts?

Racks of AWS-managed hardware installed in your own data center, running AWS services with the same APIs and tools. Used for low latency to on-premises systems, local data processing or data residency.

#### Are services global or regional?

Most services are regional: resources live in one Region. A few are global: IAM, Route 53, CloudFront, AWS Organizations and WAF for CloudFront. Some, such as EC2 subnets and EBS volumes, are scoped to a single Availability Zone.

#### What is the AWS Well-Architected Framework?

A set of best practices and questions for designing and reviewing workloads on AWS, organized into six pillars. The Well-Architected Tool in the console runs a structured review of a workload.

#### What are the six pillars of the Well-Architected Framework?

Operational excellence, Security, Reliability, Performance efficiency, Cost optimization and Sustainability.

#### What does the Operational excellence pillar focus on?

Running and monitoring systems and continually improving processes: operations as code, small and reversible changes, learning from failures and anticipating them.

#### What does the Security pillar focus on?

Protecting data, systems and assets: a strong identity foundation, traceability, security at every layer, automated security controls, encryption in transit and at rest, and preparing for security events.

#### What does the Reliability pillar focus on?

A workload performing its intended function correctly and consistently: automatic recovery from failure, testing recovery procedures, scaling horizontally, and managing change through automation.

#### What does the Performance efficiency pillar focus on?

Using resources efficiently as demand and technology change: choosing the right resource types, using managed and serverless services, going global in minutes and experimenting often.

#### What does the Cost optimization pillar focus on?

Delivering business value at the lowest price: paying only for what you use, measuring efficiency, avoiding spending on undifferentiated work, and analyzing and attributing expenditure.

#### What does the Sustainability pillar focus on?

Minimizing the environmental impact of workloads: understanding your impact, maximizing utilization, using managed services and more efficient hardware, and reducing the resources downstream users need.

#### What does "design for failure" mean?

Assume any component can fail and build the system so it keeps working when it does: multiple AZs, health checks, automatic replacement, retries and decoupled components.

#### What is loose coupling, and which services help achieve it?

Designing components so a failure or slowdown in one doesn't cascade to others. Queues (Amazon SQS), notifications (Amazon SNS), event buses (Amazon EventBridge) and load balancers let components communicate without depending directly on each other.

#### What is the difference between a stateless and a stateful application?

A stateless component keeps no session data between requests, so any instance can serve any request and instances can be added or removed freely. State is stored elsewhere (DynamoDB, ElastiCache, S3). Stateful components are harder to scale horizontally.

#### What is infrastructure as code, and why does the Well-Architected Framework recommend it?

Defining infrastructure in versioned templates or code (CloudFormation, AWS CDK) instead of manual console clicks. Environments become reproducible, reviewable and quick to rebuild, which supports operational excellence and reliability.

### Security, the shared responsibility model and IAM

#### What is the shared responsibility model in AWS?

Security is shared between AWS and the customer. AWS is responsible for security **of** the cloud (hardware, global infrastructure, facilities, the virtualization layer, managed-service software). The customer is responsible for security **in** the cloud (data, identities and permissions, operating systems and applications they run, network and firewall configuration, encryption choices).

#### How does the shared responsibility model change between EC2, RDS and S3?

The more managed the service, the less the customer does. On EC2 you patch the guest operating system and software. On RDS, AWS patches the operating system and database engine and you manage users, network access and data. On S3 you manage data, access policies and encryption settings.

#### Who is responsible for patching the operating system of an EC2 instance?

The customer. AWS patches the hypervisor and physical hosts. Tools like AWS Systems Manager Patch Manager help automate guest patching.

#### Who is responsible for physical security of data centers?

AWS. Customers never get physical access to AWS data centers.

#### Which responsibilities are shared by both?

Patch management (AWS patches infrastructure, the customer patches guest systems and applications), configuration management, and awareness and training (each trains its own staff).

#### What is AWS Identity and Access Management (IAM)?

The global service that controls who can sign in to an AWS account (authentication) and what they can do (authorization). It manages users, groups, roles and policies at no extra charge.

#### What is the root user, and how should it be protected?

The identity created with the account, with unrestricted access to everything, including billing and closing the account. Protect it with a strong password and MFA, delete its access keys, and use it only for the few tasks that require it.

#### Which tasks can only be done with the root user?

Examples: changing the account's root email or name, closing the account, changing the AWS Support plan, restoring IAM permissions when the only administrator locked themselves out, and some billing settings.

#### What is an IAM user?

An identity representing a person or application, with long-term credentials: a password for the console and/or access keys for the API. AWS recommends federated or temporary credentials over IAM users for people where possible.

#### What is an IAM group?

A collection of IAM users. Policies attached to the group apply to every member, which makes permissions easier to manage. Groups cannot be nested and are not identities themselves.

#### What is an IAM role?

An identity with permissions but no long-term credentials. A trusted entity (an AWS service such as EC2 or Lambda, a user, another account or a federated identity) assumes the role and receives temporary credentials from AWS STS.

#### Why should an EC2 instance use a role rather than access keys?

Keys stored on the instance can leak and must be rotated by hand. A role provides automatically rotated temporary credentials through the instance metadata, and nothing secret is stored on disk.

#### What is an IAM policy?

A JSON document that allows or denies actions on resources under optional conditions. Identity-based policies attach to users, groups or roles. Resource-based policies (such as S3 bucket policies) attach to resources.

#### What does an IAM policy statement contain?

`Effect` (Allow or Deny), `Action` (for example `s3:GetObject`), `Resource` (an ARN), and optionally `Condition` (for example a source IP or required MFA). Resource-based policies also have a `Principal`.

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/reports/*"
  }]
}
```

#### How does IAM evaluate permissions when policies conflict?

Everything is denied by default. An explicit Allow grants access, but an explicit Deny anywhere always wins over any Allow.

#### What is the principle of least privilege?

Grant only the permissions needed to do a task, and nothing more. Start small and add permissions as needed. IAM Access Analyzer can generate policies from actual activity.

#### What is multi-factor authentication (MFA), and which devices does AWS support?

A second factor in addition to the password. AWS supports passkeys and FIDO2 security keys, virtual authenticator apps, and hardware TOTP tokens.

#### What are access keys?

An access key ID and secret access key pair used to sign programmatic requests (CLI, SDK). They are long-term credentials: never commit them to code, rotate them, and prefer roles or IAM Identity Center where possible.

#### What is AWS IAM Identity Center?

The successor to AWS Single Sign-On. It centrally manages workforce access to multiple AWS accounts and business applications, using its own directory or an external identity provider (Microsoft Entra ID, Okta, Active Directory).

#### What is identity federation?

Letting users sign in with an existing identity (corporate directory, SAML 2.0 or OIDC provider) and receive temporary AWS credentials, without creating IAM users for them.

#### What is AWS STS?

The AWS Security Token Service issues temporary, limited-privilege credentials, for example when a role is assumed or a federated user signs in.

#### What is the IAM credential report?

An account-level CSV listing all users and the status of their credentials: passwords, access keys, MFA, last used dates. Useful for audits.

#### What is IAM Access Advisor?

A view showing which services a user, group or role has permissions for and when they were last accessed. It helps remove unused permissions.

#### What is an ARN?

An Amazon Resource Name uniquely identifies a resource: `arn:partition:service:region:account-id:resource`, for example `arn:aws:s3:::my-bucket`.

#### What is a password policy in IAM?

Account rules for IAM user passwords: minimum length, required character types, expiry, reuse prevention.

### Security services and compliance

#### What is AWS Organizations?

A service for centrally managing multiple AWS accounts: group them into organisational units (OUs), apply policies, and consolidate billing. A management account owns the organization.

#### What are Service Control Policies (SCPs)?

Policies in AWS Organizations that set the maximum permissions for accounts or OUs. They don't grant permissions: they limit what IAM policies in those accounts can allow, even for the root user of a member account.

#### What is AWS Control Tower?

A service that sets up and governs a secure multi-account environment (a landing zone) following best practices, with preventive and detective guardrails and a dashboard.

#### What is AWS Key Management Service (KMS)?

A managed service to create and control encryption keys and use them to encrypt data. It is integrated with most AWS services and logs key usage to CloudTrail.

#### What is the difference between AWS KMS and AWS CloudHSM?

KMS is a multi-tenant managed service where AWS operates the hardware security modules. CloudHSM gives you dedicated, single-tenant HSMs that you control, for strict compliance requirements.

#### What is the difference between encryption at rest and in transit?

At rest protects stored data (S3 objects, EBS volumes, database files), typically with KMS keys. In transit protects data moving across the network, typically with TLS.

#### What is AWS Certificate Manager (ACM)?

A service that provisions, manages and renews SSL/TLS certificates for use with AWS services such as Elastic Load Balancing, CloudFront and API Gateway. Public certificates are free.

#### What is AWS Secrets Manager?

A service to store, retrieve and automatically rotate secrets such as database passwords and API keys, so they aren't hard-coded in applications.

#### What is the difference between Secrets Manager and Systems Manager Parameter Store?

Both store configuration and secrets. Secrets Manager adds built-in automatic rotation and cross-account sharing, at a per-secret cost. Parameter Store's standard tier is free and is good for configuration values and simple secrets without rotation.

#### What is AWS Shield?

Managed DDoS protection. Shield Standard is automatic and free for all customers against common network and transport-layer attacks. Shield Advanced is paid and adds protection for larger attacks, 24/7 access to the Shield Response Team and cost protection.

#### What is AWS WAF?

A web application firewall that filters HTTP(S) requests to CloudFront, Application Load Balancer, API Gateway and AppSync using rules (IP sets, rate limits, SQL injection and cross-site scripting patterns, managed rule groups).

#### What is Amazon GuardDuty?

An intelligent threat-detection service that continuously analyzes CloudTrail events, VPC Flow Logs and DNS logs (and optionally other sources) with machine learning and threat intelligence to find suspicious activity, such as compromised credentials or crypto-mining.

#### What is Amazon Inspector?

An automated vulnerability management service that scans EC2 instances, container images in ECR and Lambda functions for software vulnerabilities and unintended network exposure.

#### What is Amazon Macie?

A service that uses machine learning and pattern matching to discover and protect sensitive data, such as personal data, in Amazon S3.

#### What is AWS Security Hub?

A central view of security alerts and compliance posture across accounts. It aggregates findings from GuardDuty, Inspector, Macie and partner tools and runs automated checks against standards such as CIS benchmarks.

#### What is Amazon Detective?

A service that analyzes and visualizes security data to investigate the root cause of a security finding or suspicious activity.

#### What is AWS Artifact?

A self-service portal for AWS compliance reports (SOC, ISO, PCI DSS) and agreements (such as the Business Associate Addendum for HIPAA).

#### What is the AWS Security Center and the compliance program?

AWS maintains certifications and attestations (ISO 27001, SOC 1/2/3, PCI DSS, HIPAA eligibility, GDPR support) for its infrastructure. Customers inherit the infrastructure controls but must make their own workloads compliant.

#### Do you need permission from AWS to run a penetration test?

Not for a list of permitted services (EC2, RDS, Lambda, CloudFront and others). Some activities remain prohibited, such as DoS attacks, which require a separate approval process for simulated events.

#### What is AWS Abuse, and when do you contact it?

The AWS team to report AWS resources being used for abuse, such as spam, port scanning, DoS attacks or hosting malware.

### Compute: EC2, containers and serverless

#### What is Amazon EC2 and what are its key features?

Elastic Compute Cloud provides resizable virtual servers (instances). Key features: many instance types, choice of operating systems through AMIs, several pricing models, EBS and instance-store storage, security groups, Auto Scaling, Elastic IP addresses and placement in any AZ.

#### What is an AMI?

An Amazon Machine Image is a template containing the operating system, software and configuration used to launch instances. You can use AWS, Marketplace, community or your own AMIs.

#### What are the EC2 instance families?

- **General purpose** (M, T): balanced CPU, memory and networking.
- **Compute optimized** (C): high-performance processors, for batch processing, gaming, scientific modeling.
- **Memory optimized** (R, X): large in-memory datasets.
- **Accelerated computing** (P, G, Inf, Trn): GPUs or custom chips for machine learning and graphics.
- **Storage optimized** (I, D): high, sequential read/write on local storage, for data warehouses and OLTP.

#### What are T instances and burstable performance?

T instances provide a baseline CPU level and accumulate CPU credits when idle, which they spend to burst above baseline. They suit workloads with low average CPU and occasional spikes.

#### What are the EC2 pricing options?

- **On-Demand:** pay per second or hour, no commitment.
- **Savings Plans:** commit to a spend per hour for 1 or 3 years, up to about 72% off.
- **Reserved Instances:** commit to an instance configuration for 1 or 3 years.
- **Spot Instances:** unused capacity at up to 90% off, can be interrupted with a two-minute warning.
- **Dedicated Hosts:** a physical server for you, for licensing and compliance.
- **Dedicated Instances:** instances on hardware not shared with other accounts.
- **Capacity Reservations:** reserve capacity in an AZ, at On-Demand price.

#### When should you use Spot Instances?

For flexible, fault-tolerant, interruptible workloads: batch jobs, data processing, CI builds, stateless web workers. Never for a database that cannot stop.

#### What is the difference between Compute Savings Plans and EC2 Instance Savings Plans?

Compute Savings Plans apply to any instance family, size, Region and operating system, and also to Fargate and Lambda. EC2 Instance Savings Plans are tied to an instance family in a Region but give a larger discount.

#### When do you need a Dedicated Host?

When software licences are tied to physical cores or sockets (bring your own license), or when compliance requires visibility and control of the physical server.

#### What is a security group?

A stateful virtual firewall for instances (attached to network interfaces). It has allow rules only. Return traffic is allowed automatically, and by default all inbound traffic is denied and all outbound allowed.

#### What is EC2 Auto Scaling?

A service that adds or removes EC2 instances in an Auto Scaling group according to policies (target tracking, step, scheduled, predictive), and replaces unhealthy instances. You set minimum, desired and maximum capacity.

#### What is Elastic Load Balancing, and what are its types?

A service that distributes traffic across targets in several AZs and checks their health.
- **Application Load Balancer:** HTTP/HTTPS, layer 7, path and host-based routing.
- **Network Load Balancer:** TCP/UDP/TLS, layer 4, very high performance and static IPs.
- **Gateway Load Balancer:** layer 3, for third-party network appliances such as firewalls.

#### What is an Elastic IP address?

A static public IPv4 address you allocate to your account and can attach to an instance. Public IPv4 addresses are charged hourly, whether attached or not.

#### What is EC2 user data?

A script passed at launch that runs on first boot, used to install software or configure the instance.

#### What is AWS Lambda?

A serverless compute service that runs your function in response to events (an API call, a file in S3, a message, a schedule). You pay per request and per duration in milliseconds. A single invocation can run for at most 15 minutes.

#### When would you choose Lambda over EC2?

For event-driven, short-lived, variable or unpredictable workloads where you don't want to manage servers. EC2 suits long-running processes, special operating system requirements or steady high load.

#### What is the difference between Amazon ECS and Amazon EKS?

Both orchestrate containers. ECS is AWS's own, simpler orchestrator. EKS is managed Kubernetes, for teams that use Kubernetes tooling or need portability.

#### What is AWS Fargate?

A serverless compute engine for containers that works with ECS and EKS. You define CPU and memory per task or pod, and AWS runs it without servers for you to manage.

#### What is Amazon ECR?

Elastic Container Registry, a managed registry to store, scan and share Docker and OCI container images.

#### What is AWS Elastic Beanstalk?

A platform as a service: you upload application code (Java, .NET, Node.js, Python, PHP, Go, Ruby, Docker) and Beanstalk provisions and manages EC2, load balancing, Auto Scaling and monitoring. The underlying resources remain visible and configurable.

#### What is Amazon Lightsail?

A simplified service for virtual private servers, databases and containers at a predictable monthly price, aimed at simple websites and users new to AWS.

#### What is AWS Batch?

A service that runs batch computing jobs at any scale, provisioning EC2 or Fargate capacity (including Spot) based on the jobs queued.

#### What is AWS App Runner?

A fully managed service that builds and runs web applications and APIs from source code or a container image, with automatic scaling and HTTPS.

#### What is the EC2 instance store?

Temporary block storage physically attached to the host. It is very fast but its data is lost when the instance stops or terminates, so it suits buffers, caches and scratch data.

#### What does EC2 Instance Connect or Session Manager give you?

Ways to access instances without managing SSH keys. Session Manager (part of Systems Manager) even works without opening inbound ports, with sessions logged.

#### What is the difference between stopping and terminating an instance?

Stopping shuts it down: EBS root volumes are kept and you pay only for storage, and you can start it again. Terminating deletes the instance, and by default its root EBS volume.

### Storage

#### What is Amazon S3 and what storage classes does it offer?

Simple Storage Service is object storage with 11 nines (99.999999999%) of durability, where data is stored as objects in buckets. Storage classes:
- **S3 Standard:** frequently accessed data.
- **S3 Intelligent-Tiering:** moves objects between tiers automatically when access patterns are unknown or change.
- **S3 Standard-IA:** infrequent access, millisecond retrieval, retrieval fee.
- **S3 One Zone-IA:** infrequent access stored in one AZ, cheaper, less resilient.
- **S3 Express One Zone:** single-digit millisecond latency for the most performance-sensitive data.
- **S3 Glacier Instant Retrieval:** archive accessed about once a quarter, millisecond retrieval.
- **S3 Glacier Flexible Retrieval:** archive, retrieval in minutes to hours.
- **S3 Glacier Deep Archive:** cheapest, retrieval within 12 to 48 hours.

#### What is an S3 bucket and an object?

A bucket is a container for objects with a globally unique name, created in one Region. An object is a file plus metadata, identified by a key, up to 5 TB in size.

#### What are S3 lifecycle policies?

Rules that automatically transition objects to cheaper storage classes after a given age, or delete them (expiration).

#### What is S3 Versioning?

A bucket setting that keeps every version of an object, so overwritten or deleted objects can be restored.

#### How do you control access to S3?

With IAM policies, bucket policies, access points, ACLs (now disabled by default) and Block Public Access, which prevents public access at the bucket or account level. Presigned URLs give temporary access to one object.

#### How is S3 data encrypted?

All new objects are encrypted at rest by default with S3-managed keys (SSE-S3). You can choose KMS keys (SSE-KMS), customer-provided keys (SSE-C), or encrypt on the client before uploading.

#### What is S3 replication?

Automatic, asynchronous copying of objects to another bucket in another Region (Cross-Region Replication) or the same Region (Same-Region Replication). It requires versioning.

#### What is S3 static website hosting?

Serving a website made of static files (HTML, CSS, JS, images) directly from a bucket, usually behind CloudFront for HTTPS and caching.

#### What is S3 Transfer Acceleration?

Faster uploads over long distances by routing them through CloudFront edge locations and the AWS backbone network.

#### What is Amazon EBS?

Elastic Block Store provides network block volumes for EC2 instances, persisting independently of the instance's life. A volume lives in one AZ and is replicated within it. Types include gp3 (general SSD), io2 (provisioned IOPS SSD), st1 (throughput HDD) and sc1 (cold HDD).

#### What are EBS snapshots?

Incremental point-in-time backups of EBS volumes stored in S3 (managed by AWS). They can be copied to other Regions and used to create new volumes.

#### What is Amazon EFS?

Elastic File System is a managed NFS file system for Linux that grows and shrinks automatically and can be mounted by many instances across several AZs at once.

#### What is the difference between S3, EBS and EFS?

S3 is object storage accessed by API, virtually unlimited, for any number of clients. EBS is block storage attached to (usually) one instance in one AZ, like a disk. EFS is a shared file system for many Linux instances across AZs.

#### What is Amazon FSx?

Fully managed third-party file systems: FSx for Windows File Server (SMB), FSx for Lustre (high-performance computing), FSx for NetApp ONTAP and FSx for OpenZFS.

#### What is AWS Storage Gateway?

A hybrid storage service that gives on-premises applications access to cloud storage. Types: S3 File Gateway, FSx File Gateway, Volume Gateway and Tape Gateway (virtual tape library for backups).

#### What is the AWS Snow Family?

Physical devices to move large amounts of data into and out of AWS offline, or to process data at the edge where there is little or no connectivity (AWS Snowball Edge devices).

#### What is AWS Backup?

A central service to automate and audit backups across services: EBS, EC2, RDS, DynamoDB, EFS, FSx, S3 and more, with backup plans and cross-Region or cross-account copies.

#### What is AWS DataSync?

An online data transfer service that moves data between on-premises storage (NFS, SMB, HDFS, object stores) and AWS storage services, quickly and with verification.

#### How durable and available is S3 Standard?

Designed for 99.999999999% durability and 99.99% availability, with data stored across at least three AZs.

#### When would you use S3 One Zone-IA?

For infrequently accessed data that can be recreated, such as secondary backup copies or derived data, where losing an AZ is acceptable in exchange for a lower price.

### Databases and analytics

#### How does Amazon RDS differ from Amazon DynamoDB?

RDS is a managed relational database service (SQL, schemas, joins, transactions) running MySQL, PostgreSQL, MariaDB, Oracle, SQL Server or Db2 on instances you size. DynamoDB is a serverless NoSQL key-value and document database with single-digit millisecond performance at any scale, no fixed schema beyond the keys, and automatic scaling.

#### What does Amazon RDS manage for you?

Provisioning, operating system and database patching, automated backups and point-in-time recovery, Multi-AZ failover, read replicas, monitoring and storage scaling. You manage schema, queries, users and network access.

#### What is the difference between RDS Multi-AZ and read replicas?

Multi-AZ keeps a synchronous standby (or standbys) in another AZ for high availability and automatic failover. It is not meant to serve reads in the classic setup. Read replicas are asynchronous copies used to scale read traffic, possibly in other Regions, and can be promoted.

#### What is Amazon Aurora?

A cloud-native relational database compatible with MySQL and PostgreSQL. It stores six copies of data across three AZs, scales storage automatically, and offers Aurora Serverless for variable workloads.

#### What is Amazon ElastiCache?

Managed in-memory caching with Valkey, Redis OSS or Memcached, used to reduce database load and serve frequent reads with microsecond latency.

#### What is Amazon MemoryDB?

A durable in-memory database compatible with Valkey and Redis OSS, usable as a primary database thanks to its multi-AZ transaction log.

#### What is Amazon Redshift?

A managed, petabyte-scale cloud data warehouse for analytical SQL queries (OLAP), with columnar storage, a serverless option and the ability to query data in S3.

#### What is the difference between OLTP and OLAP, and which AWS services fit each?

OLTP handles many small transactional reads and writes (orders, payments): RDS, Aurora, DynamoDB. OLAP runs large analytical queries over historical data: Redshift, Athena.

#### What is Amazon DocumentDB?

A managed document database compatible with MongoDB workloads.

#### What is Amazon Neptune?

A managed graph database for highly connected data such as social networks, fraud detection and knowledge graphs.

#### What is Amazon Keyspaces?

A serverless managed database compatible with Apache Cassandra.

#### What is Amazon Timestream?

A managed time-series database for IoT and operational metrics.

#### What is AWS Database Migration Service (DMS)?

A service that migrates databases to AWS with minimal downtime, between the same engines (homogeneous) or different engines (heterogeneous, with the Schema Conversion Tool), and can replicate ongoing changes.

#### What is Amazon Athena?

A serverless interactive query service to analyze data in S3 with standard SQL. You pay per amount of data scanned, so columnar formats and partitioning reduce cost.

#### What is AWS Glue?

A serverless data integration service: crawlers to discover schemas, the Glue Data Catalog as a central metadata store, and Spark-based ETL jobs.

#### What is Amazon EMR?

A managed big-data platform to run Apache Spark, Hive, Presto/Trino, HBase and other frameworks on EC2, EKS or serverless.

#### What is Amazon Kinesis?

Services for real-time streaming data. Kinesis Data Streams captures and stores streams for custom processing. Amazon Data Firehose loads streams into destinations such as S3, Redshift or OpenSearch.

#### What is Amazon QuickSight?

A serverless business intelligence service to build interactive dashboards and reports, with machine-learning insights and natural-language questions.

#### What is Amazon OpenSearch Service?

A managed service for OpenSearch (and legacy Elasticsearch) clusters, used for log analytics, full-text search and observability.

#### What is AWS Lake Formation?

A service to build, secure and manage a data lake on S3, with central fine-grained permissions on Glue Data Catalog tables.

### Networking and content delivery

#### What is Amazon VPC?

Virtual Private Cloud is a logically isolated virtual network in a Region where you launch resources. You choose its IP range and create subnets, route tables and gateways.

#### What is the difference between a public and a private subnet?

A public subnet has a route to an internet gateway, so resources with public IPs can be reached from the internet. A private subnet has no such route; its resources can reach the internet only through a NAT gateway, if at all.

#### What is an internet gateway?

A VPC component that allows communication between resources in the VPC and the internet.

#### What is a NAT gateway?

A managed service that lets instances in private subnets start outbound connections to the internet (for updates, for example) while blocking unsolicited inbound connections.

#### What is the difference between a security group and a network ACL?

A security group works at the instance (network interface) level, is stateful and supports allow rules only. A network ACL works at the subnet level, is stateless (return traffic must be allowed explicitly), supports allow and deny rules, and evaluates rules in number order.

#### What is VPC peering?

A private network connection between two VPCs (in the same or different accounts or Regions). It is not transitive.

#### What is AWS Transit Gateway?

A hub that connects many VPCs and on-premises networks through one gateway, replacing complex meshes of peering connections.

#### What is AWS Site-to-Site VPN?

An encrypted IPsec connection between an on-premises network and a VPC over the internet. Quick to set up, but its performance depends on the internet.

#### What is AWS Direct Connect?

A dedicated private network connection from your premises to AWS. It provides consistent bandwidth and latency and can reduce data transfer costs, but takes weeks to set up. It is not encrypted by default.

#### What is AWS Client VPN?

A managed VPN service that lets individual users connect securely to AWS and on-premises networks from their devices.

#### What is a VPC endpoint?

A private connection from a VPC to AWS services without going through the internet. Gateway endpoints serve S3 and DynamoDB. Interface endpoints (AWS PrivateLink) serve many other services.

#### What is AWS PrivateLink?

Technology that exposes services privately across VPCs and accounts through interface endpoints, keeping traffic on the AWS network.

#### What are VPC Flow Logs?

Records of IP traffic going to and from network interfaces in a VPC, sent to CloudWatch Logs or S3 for troubleshooting and security analysis.

#### What is Amazon Route 53?

A highly available DNS service and domain registrar, with health checks and routing policies.

#### What are the Route 53 routing policies?

Simple, weighted, latency-based, failover, geolocation, geoproximity, IP-based and multivalue answer.

#### What is Amazon CloudFront?

A content delivery network that caches content at edge locations close to users, reducing latency. It works with origins such as S3, load balancers or any HTTP server, supports HTTPS, and integrates with WAF and Shield.

#### What is AWS Global Accelerator?

A service that routes user traffic onto the AWS global network through two static anycast IP addresses, improving the performance and availability of TCP/UDP applications across Regions. Unlike CloudFront, it doesn't cache.

#### What is Amazon API Gateway?

A managed service to create, publish, secure and monitor REST, HTTP and WebSocket APIs, often in front of Lambda functions.

#### What is a CIDR block?

A notation for an IP address range, such as 10.0.0.0/16, used to define the address space of a VPC and its subnets.

#### What is a bastion host?

An instance in a public subnet used as a hardened entry point for SSH or RDP access to instances in private subnets. Systems Manager Session Manager often replaces it.

### Management, governance and developer tools

#### What is Amazon CloudWatch?

A monitoring and observability service: metrics, alarms, logs (CloudWatch Logs), dashboards and events, for AWS resources and applications.

#### What is AWS CloudTrail?

A service that records API calls and account activity (who did what, when, from where) for governance, compliance and auditing. Logs can be delivered to S3 and analyzed with CloudTrail Lake.

#### What is the difference between CloudWatch and CloudTrail?

CloudWatch monitors performance and health (metrics, logs, alarms). CloudTrail audits actions (API calls made in the account).

#### What is AWS Config?

A service that records resource configurations and their changes over time and evaluates them against rules, for compliance auditing and troubleshooting.

#### What is AWS Systems Manager?

A set of operational tools for managing EC2 and on-premises servers at scale: Session Manager, Patch Manager, Run Command, Parameter Store, Automation and inventory.

#### What is AWS CloudFormation?

Infrastructure as code: you describe resources in JSON or YAML templates, and CloudFormation creates, updates and deletes them as a stack, in the right order.

#### What is the AWS Cloud Development Kit (CDK)?

A framework to define cloud infrastructure in programming languages (TypeScript, Python, Java, C#, Go). It synthesizes CloudFormation templates.

#### What is AWS Trusted Advisor?

A service that inspects your account and recommends improvements in five categories: cost optimization, performance, security, fault tolerance and service quotas. Basic and Developer Support plans get core checks only. Business and higher plans get the full set.

#### What is the AWS Health Dashboard?

A view of AWS service health and of events that affect your own resources, such as scheduled maintenance or issues in your Regions.

#### What are the ways to interact with AWS?

The AWS Management Console (web), the AWS CLI, the SDKs for programming languages, infrastructure as code (CloudFormation, CDK) and AWS CloudShell (a browser-based shell already authenticated).

#### What are AWS CodeCommit, CodeBuild, CodeDeploy and CodePipeline?

Developer tools for CI/CD: CodeBuild compiles and tests code, CodeDeploy automates deployments to EC2, Lambda, ECS and on premises, CodePipeline orchestrates release pipelines. CodeCommit is a Git hosting service that is closed to new customers.

#### What is AWS X-Ray?

A service that traces requests through distributed applications to find performance bottlenecks and errors.

#### What is Amazon SQS?

Simple Queue Service is a fully managed message queue that decouples components. Standard queues give high throughput with at-least-once delivery. FIFO queues guarantee order and exactly-once processing.

#### What is the difference between SQS and SNS?

SQS is a queue: consumers poll messages, each message is processed by one consumer. SNS is publish/subscribe: a message published to a topic is pushed to all subscribers (SQS, Lambda, HTTP, email, SMS). They are often combined in a fan-out pattern.

#### What is Amazon EventBridge?

A serverless event bus that routes events from AWS services, SaaS applications and your own code to targets based on rules, and schedules tasks (EventBridge Scheduler).

### Billing, pricing and support

#### What are the three fundamental drivers of AWS cost?

Compute, storage and outbound data transfer. Inbound data transfer is generally free.

#### What is the AWS Free Tier?

Offers that let you try AWS at no cost within limits. It includes always-free offers (for example Lambda requests and DynamoDB storage up to a limit), credits or 12-month offers for new accounts depending on the account plan, and short free trials of specific services. Usage beyond the limits is billed.

#### What is the AWS Pricing Calculator?

A free tool to estimate the cost of an architecture before building it.

#### What is AWS Cost Explorer?

A tool to visualize, analyze and forecast costs and usage over time, with filters by service, account or tag, and recommendations for Savings Plans and rightsizing.

#### What is AWS Budgets?

A service to set custom cost, usage or reservation budgets and receive alerts (or trigger actions) when actual or forecast spend crosses a threshold.

#### What is the AWS Cost and Usage Report, now Data Exports?

The most detailed billing data, delivered to S3 at hourly or daily granularity, for analysis with Athena, QuickSight or other tools.

#### What are cost allocation tags?

Tags (key-value pairs such as `project=lakehouse`) activated in the billing console so that costs can be grouped and filtered by them in Cost Explorer and reports.

#### What is consolidated billing in AWS Organizations?

One bill for all accounts of an organization, paid by the management account. Usage is combined for volume pricing discounts, and Reserved Instances and Savings Plans discounts can be shared across accounts.

#### What is AWS Compute Optimizer?

A service that uses machine learning on utilization metrics to recommend optimal EC2 instance types, Auto Scaling groups, EBS volumes, Lambda functions and ECS on Fargate configurations.

#### What are the AWS Support plans?

- **Basic:** free. Documentation, forums, AWS re:Post, Health Dashboard, core Trusted Advisor checks.
- **Developer:** business-hours email access to support engineers, for testing and development.
- **Business:** 24/7 phone, chat and email support, full Trusted Advisor, fast response for production systems down.
- **Enterprise On-Ramp:** adds a pool of Technical Account Managers and faster response for business-critical systems.
- **Enterprise:** a designated Technical Account Manager, the fastest response for business-critical systems down, and concierge billing support.

Check the AWS Support page for current plan names and response times, as AWS revises them.

#### What is a Technical Account Manager (TAM)?

A dedicated AWS technical contact for Enterprise customers who provides proactive guidance on architecture, operations and best practices.

#### What is AWS re:Post?

A community question-and-answer site, moderated with AWS experts, which replaced the AWS Forums.

#### What is the AWS Marketplace?

A curated digital catalog of third-party software, data and services that run on AWS, purchasable with billing through your AWS account.

#### What is AWS Professional Services and the AWS Partner Network?

AWS Professional Services is AWS's own consulting team. The AWS Partner Network (APN) is the global community of consulting and technology partners that help customers build on AWS.

#### How can you reduce costs on AWS?

Rightsize instances, turn off unused resources, use Savings Plans or Reserved Instances for steady workloads and Spot for interruptible ones, choose cheaper storage classes with lifecycle rules, use serverless for variable load, reduce data transfer (for example with CloudFront and VPC endpoints), and track spending with tags, Budgets and Cost Explorer.
