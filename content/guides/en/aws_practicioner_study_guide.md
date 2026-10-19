## AWS Certified Cloud Practitioner Study Guide

##### Published on {{PUBLISH_DATE}}
<!-- TITLE_IMAGE -->

![AWS Certified Cloud Practitioner study guide: about 200 questions](../../images/aws_practicioner_guide_title_img.png)

About 200 questions and short answers I used to prepare the AWS Certified Cloud Practitioner exam (CLF-C02), which I passed in October 2026. They follow the exam's four domains: cloud concepts, security and compliance, cloud technology and services, and billing, pricing and support.

The guide follows a learning path in four stages. Each section is split into short units: learning goals, a concept explanation and a worked example, then questions (recall first, then application), a practical challenge and key takeaways. To **learn**, read each unit top to bottom. To **review**, switch to review mode or use "Skip to questions", mark answers you want to see again, and try a mixed review across sections. Service details and prices change, so check the AWS documentation before relying on a number.

<!-- QA -->
<!-- stage: Cloud foundations -->

### Cloud concepts

<!-- unit: Why the cloud -->

<!-- goals -->

- Explain the economic case for cloud computing.
- Connect AWS's six advantages to concrete business benefits.

<!-- concept -->

Running your own data center means buying for the peak you expect years ahead, then paying for idle capacity until you get there. The cloud flips that: you rent capacity by the second, from a provider whose scale makes each unit cheaper than you could buy it. Money moves from upfront investment to operating expense.

Speed follows from the same shift. When a server is an API call away, trying an idea costs minutes, and launching in another continent is a configuration change rather than a construction project.

<!-- example -->

| Question | On-premises | AWS |
|---|---|---|
| Capacity for Black Friday | Buy servers for the peak | Scale out for the week |
| New region for EU customers | Lease space, ship hardware | Deploy to eu-west-3 |
| Cost model | CapEx upfront | OpEx, pay as you go |

#### What is cloud computing?

The on-demand delivery of IT resources (compute, storage, databases, networking, software) over the internet with pay-as-you-go pricing. Instead of buying and running data centers, you rent capacity from a provider and release it when you no longer need it.

#### What are the six advantages of cloud computing according to AWS?

1. Trade fixed expense (capital expense) for variable expense.
2. Benefit from massive economies of scale.
3. Stop guessing capacity.
4. Increase speed and agility.
5. Stop spending money running and maintaining data centers.
6. Go global in minutes.

#### What are some advantages of using AWS instead of on-premises infrastructure?

No upfront hardware purchase, pay only for what you use, capacity in minutes instead of months, global reach, managed services that remove undifferentiated work (patching, backups), built-in security and compliance certifications, and the ability to experiment cheaply and shut down what fails.

#### What is the difference between CapEx and OpEx?

Capital expenditure (CapEx) is an upfront investment in physical assets, such as servers, depreciated over years. Operational expenditure (OpEx) is ongoing spending on services. The cloud turns most IT CapEx into OpEx.

#### What does "economies of scale" mean in the cloud?

AWS buys hardware, power and network at a scale no single customer can, so its cost per unit is lower. Part of the saving is passed on through lower prices, which AWS has reduced many times.

#### What is agility in the context of the cloud?

The speed at which you can provide resources and try new ideas. Resources that took weeks to procure are available in minutes, so the cost and time of experimenting fall sharply.

#### What does "go global in minutes" mean?

You can deploy an application in AWS Regions around the world with a few clicks or API calls, giving users lower latency without building data centers in other countries.

<!-- challenge -->

A startup's CFO asks why they shouldn't buy servers, since "renting always costs more in the end". Give two arguments in plain terms.

<!-- solution -->

They'd pay upfront for capacity they may never use, and guessing wrong either way is expensive. With AWS they pay for what they use, scale with demand, and keep cash for the business; savings plans lower prices further once usage is predictable.

<!-- takeaways -->

- Cloud trades upfront CapEx for variable OpEx.
- Economies of scale lower AWS's unit prices.
- Agility: resources in minutes, regions worldwide.

<!-- unit: Service and deployment models -->

<!-- goals -->

- Tell apart IaaS, PaaS and SaaS with AWS examples.
- Compare cloud, hybrid and on-premises deployments.

<!-- concept -->

Cloud services differ in how much AWS runs for you. With infrastructure services you get virtual machines and manage everything on them. With platform services you bring code and AWS runs the servers. With software services you just use the application. Managed and serverless services sit toward the platform end: less to operate, less to control.

Deployment models answer a different question: where things run. Many companies mix cloud and on-premises for years during a migration.

<!-- example -->

| You manage | IaaS (EC2) | PaaS (Elastic Beanstalk) | SaaS |
|---|---|---|---|
| Application code | Yes | Yes | No |
| OS patches | Yes | No | No |
| Hardware | No | No | No |

#### What are the different cloud deployment models supported by AWS?

- **Cloud (cloud-native):** everything runs in the public cloud.
- **On-premises (private cloud):** resources in your own data center, often with virtualization and resource-management tools. AWS Outposts brings AWS infrastructure on premises.
- **Hybrid:** cloud resources connected to on-premises infrastructure, for example during a migration or for data that must stay on site.

#### What do IaaS, PaaS and SaaS mean? Give AWS examples.

- **IaaS (Infrastructure as a Service):** you get virtual machines, storage and networks and manage the operating system and everything above it. Example: Amazon EC2.
- **PaaS (Platform as a Service):** the provider runs the infrastructure and platform, you deploy code. Example: AWS Elastic Beanstalk.
- **SaaS (Software as a Service):** a complete application used over the internet. Examples: Amazon WorkMail, Amazon Chime, Amazon QuickSight.

#### What is a managed service?

A service where AWS operates the underlying infrastructure and software (provisioning, patching, backups, scaling) and you only use it. Amazon RDS is a managed database. Running a database on EC2 is not managed: you do all of that yourself.

#### What does "serverless" mean?

You run code or use a service without provisioning or managing servers. Capacity scales automatically and you pay for actual use. Examples: AWS Lambda, Amazon S3, Amazon DynamoDB, AWS Fargate, Amazon Athena.

<!-- challenge -->

A team runs PostgreSQL on EC2 and spends hours on patches and backups. Which model change would help, and what do they give up?

<!-- solution -->

Move to a managed database (Amazon RDS for PostgreSQL), where AWS handles patching, backups and failover. They give up OS-level access and some low-level configuration.

<!-- takeaways -->

- IaaS, PaaS and SaaS differ in what you manage.
- Managed and serverless services shift operations to AWS.
- Hybrid mixes cloud and on-premises.

<!-- unit: Elasticity and scaling -->

<!-- goals -->

- Distinguish elasticity from scalability.
- Choose between vertical and horizontal scaling.

<!-- concept -->

Scalability is the ability to handle more load by adding resources. Elasticity adds a time dimension: resources grow and shrink automatically as demand changes, so you don't pay for the peak all year.

How you scale matters. A bigger machine is simple but has a ceiling and is still one point of failure. More machines behind a load balancer scale further and survive failures, but the application must be designed so any instance can serve any request.

<!-- example -->

```text
Vertical:   t3.large ─► m7i.2xlarge         (bigger box, restart, limit)
Horizontal: 2 × m7i.large ─► 8 × m7i.large  (more boxes, load balancer, no limit)
```

#### What is elasticity?

The ability to acquire resources when you need them and release them when you don't, automatically following demand. Example: an Auto Scaling group that adds EC2 instances during a traffic spike and removes them afterwards.

#### What is scalability?

The ability of a system to handle a growing load by adding resources. Scaling up (vertical) means bigger resources, scaling out (horizontal) means more resources. Elasticity is scalability that also scales back down automatically.

#### What is the difference between scaling vertically and horizontally?

Vertical scaling replaces a resource with a larger one (a bigger instance type). It is simple but has a ceiling and often needs a restart. Horizontal scaling adds more resources of the same size behind a load balancer. It has no practical ceiling and improves availability.

<!-- challenge -->

An online shop's traffic triples every evening and drops at night. Which approach do you suggest?

<!-- solution -->

Horizontal scaling with EC2 Auto Scaling behind a load balancer: add instances in the evening, remove them at night. That's elasticity, and it means paying for peak capacity only when it's used.

<!-- takeaways -->

- Scalability handles growth; elasticity follows demand.
- Vertical is simple but limited; horizontal scales further.
- Elastic designs avoid paying for idle peak capacity.

<!-- unit: Availability and recovery -->

<!-- goals -->

- Define high availability, fault tolerance and disaster recovery.
- Pick a DR strategy from RTO and RPO.

<!-- concept -->

Failures are certain; the question is how much they cost. High availability keeps downtime short when parts fail; fault tolerance keeps the system running with no interruption at all, at a higher price. Disaster recovery covers the bigger events, such as losing a whole Region.

Two numbers frame every DR choice: how long you can be down (RTO) and how much data you can lose (RPO). Lower numbers need more standby resources, so cost rises as both shrink.

<!-- example -->

| Strategy | RTO / RPO | Cost |
|---|---|---|
| Backup and restore | Hours / hours | $ |
| Pilot light | Tens of minutes | $$ |
| Warm standby | Minutes | $$$ |
| Multi-site active/active | Near zero | $$$$ |

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

<!-- challenge -->

A payroll system can be down for 8 hours and lose at most 1 hour of data. Which DR strategy fits, and why not a more expensive one?

<!-- solution -->

Backup and restore with hourly backups (or pilot light if restores take too long) meets an 8-hour RTO and 1-hour RPO. Warm standby or multi-site would cost much more for recovery speed the business doesn't need.

<!-- takeaways -->

- High availability limits downtime; fault tolerance avoids it.
- RTO is time to recover; RPO is data you can lose.
- Faster recovery means more standby cost.

<!-- unit: Planning a migration -->

<!-- goals -->

- Describe the AWS Cloud Adoption Framework.
- Choose a migration strategy among the 7 Rs.

<!-- concept -->

Moving to the cloud is as much an organizational change as a technical one. The Cloud Adoption Framework structures the work into perspectives, from business and people to security and operations, so that skills and processes change along with servers.

For each application, the 7 Rs give the options, from leaving it alone to rewriting it. Most companies use several: rehost quickly to exit a data center, then refactor the systems where cloud features pay off.

<!-- example -->

| Application | Strategy |
|---|---|
| Old reporting tool nobody uses | Retire |
| ERP with a hard license constraint | Retain (for now) |
| Web app on VMs | Rehost to EC2 |
| Self-managed MySQL | Replatform to RDS |
| Monolith that needs to scale | Refactor |

#### What is the AWS Cloud Adoption Framework (AWS CAF)?

Guidance that helps organizations plan a cloud transformation. It groups capabilities into six perspectives: Business, People, Governance (business-focused) and Platform, Security, Operations (technical).

#### What are the 7 Rs of migration?

Retire, Retain, Rehost ("lift and shift"), Relocate (for example VMware Cloud on AWS), Repurchase (move to SaaS), Replatform ("lift, tinker and shift", such as moving to RDS) and Refactor/re-architect (rebuild as cloud-native).

<!-- challenge -->

A company must leave its data center in 6 months and has 300 applications. Which strategy would you use for most of them, and what comes after?

<!-- solution -->

Rehost most of them (lift and shift), since it's fastest, and retire or retain the rest. After the exit, refactor or replatform the applications where managed services or scaling bring clear benefits.

<!-- takeaways -->

- CAF covers business, people, governance, platform, security, operations.
- The 7 Rs range from retire to refactor.
- Rehost first, optimize later is a common path.

### Global infrastructure and the Well-Architected Framework

<!-- unit: Regions and Availability Zones -->

<!-- goals -->

- Describe Regions, Availability Zones and global versus regional services.
- Choose a Region using compliance, latency, services and price.

<!-- concept -->

AWS builds its infrastructure in layers of isolation. A Region is a geographic area; inside it, Availability Zones are separate data centers with their own power and networking, close enough for fast connections but far enough that one event doesn't hit them all.

That layout drives design: spreading across AZs protects against a data center failure, and spreading across Regions protects against a regional event. Choosing the Region starts with legal requirements, then latency, service availability and price.

<!-- example -->

```text
Region eu-west-3 (Paris)
 ├─ AZ eu-west-3a ── app + DB primary
 ├─ AZ eu-west-3b ── app + DB standby
 └─ AZ eu-west-3c ── app
```

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

#### Are services global or regional?

Most services are regional: resources live in one Region. A few are global: IAM, Route 53, CloudFront, AWS Organizations and WAF for CloudFront. Some, such as EC2 subnets and EBS volumes, are scoped to a single Availability Zone.

<!-- challenge -->

A French health company wants low latency for French users and must keep patient data in France. Which Region and layout do you suggest?

<!-- solution -->

Paris (eu-west-3), which meets data residency, with the application and database spread across at least two Availability Zones for high availability. Confirm the needed services are available there.

<!-- takeaways -->

- Regions contain several isolated Availability Zones.
- Spread across AZs for availability, Regions for disasters.
- Compliance comes first when choosing a Region.

<!-- unit: Edge and on-premises infrastructure -->

<!-- goals -->

- Explain edge locations, Local Zones, Wavelength and Outposts.
- Match each to a latency or location need.

<!-- concept -->

Not everything can run in a Region. Content and DNS answers are faster from edge locations near users. Some applications need single-digit millisecond latency to a city or a 5G network, which Local Zones and Wavelength provide. Some must stay in your building for regulatory or latency reasons, which Outposts handle by bringing AWS hardware to you.

Each option extends the same AWS services and APIs to a new place.

<!-- example -->

| Need | Option |
|---|---|
| Cache images near users worldwide | Edge locations (CloudFront) |
| Video editing near Los Angeles | Local Zone |
| Mobile game over 5G | Wavelength |
| Factory systems on site | Outposts |

#### What is an edge location?

A site that runs CloudFront caches and Route 53 DNS (and services such as Lambda@Edge) close to end users. There are many more edge locations than Regions.

#### What is a Local Zone?

An extension of a Region placed near a large city, running selected services (such as EC2 and EBS) to give single-digit millisecond latency to users there.

#### What is AWS Wavelength?

Infrastructure embedded in telecom providers' 5G networks, so applications can reach mobile devices with very low latency.

#### What is AWS Outposts?

Racks of AWS-managed hardware installed in your own data center, running AWS services with the same APIs and tools. Used for low latency to on-premises systems, local data processing or data residency.

<!-- challenge -->

A bank must keep a trading system in its own data center but wants AWS APIs and tools. Which service fits?

<!-- solution -->

AWS Outposts: AWS-managed racks installed on premises that run AWS services with the same APIs, connected to a parent Region.

<!-- takeaways -->

- Edge locations serve CloudFront and Route 53 near users.
- Local Zones and Wavelength bring compute closer to cities and 5G.
- Outposts run AWS in your data center.

<!-- unit: The Well-Architected pillars -->

<!-- goals -->

- Name the six pillars of the Well-Architected Framework.
- Summarize what each pillar asks of a workload.

<!-- concept -->

The Well-Architected Framework is a structured way to ask whether a workload is built well. It splits "well" into six concerns that often pull against each other: running it smoothly, keeping it secure, making it reliable, using resources efficiently, spending wisely and reducing environmental impact.

The value is in the trade-offs. A design review using the pillars makes them explicit, for example paying more for multi-AZ reliability or accepting less performance for lower cost.

<!-- example -->

| Pillar | Typical question |
|---|---|
| Operational excellence | How do you deploy and learn from incidents? |
| Security | How do you manage identities and protect data? |
| Reliability | How does the workload recover from failure? |
| Performance efficiency | How do you choose the right resources? |
| Cost optimization | How do you know what you spend and why? |
| Sustainability | How do you reduce resource use? |

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

<!-- challenge -->

A team runs its production database on one instance with no backups to save money. Which pillars does this neglect, and what is the cheapest fix?

<!-- solution -->

Mainly Reliability (single point of failure, no recovery) in favor of Cost optimization. The cheapest fix is automated backups with point-in-time recovery; Multi-AZ adds availability at higher cost.

<!-- takeaways -->

- Six pillars: operations, security, reliability, performance, cost, sustainability.
- Pillars often trade against each other.
- Reviews make those trade-offs explicit.

<!-- unit: Design principles -->

<!-- goals -->

- Apply "design for failure", loose coupling and statelessness.
- Explain why infrastructure as code is recommended.

<!-- concept -->

A few principles recur across the pillars. Expect every component to fail, so build redundancy and automatic recovery. Connect components through queues and events so a slow part doesn't stall the rest. Keep application servers stateless so any one can be replaced.

Infrastructure as code makes all of this repeatable: environments become reviewed, versioned templates, and rebuilding after a failure is running the template again.

<!-- example -->

```text
Tightly coupled:  web ─► order service ─► payment API (down → orders fail)
Loosely coupled:  web ─► SQS queue ─► order workers ─► payment API (down → orders wait)
```

#### What does "design for failure" mean?

Assume any component can fail and build the system so it keeps working when it does: multiple AZs, health checks, automatic replacement, retries and decoupled components.

#### What is loose coupling, and which services help achieve it?

Designing components so a failure or slowdown in one doesn't cascade to others. Queues (Amazon SQS), notifications (Amazon SNS), event buses (Amazon EventBridge) and load balancers let components communicate without depending directly on each other.

#### What is the difference between a stateless and a stateful application?

A stateless component keeps no session data between requests, so any instance can serve any request and instances can be added or removed freely. State is stored elsewhere (DynamoDB, ElastiCache, S3). Stateful components are harder to scale horizontally.

#### What is infrastructure as code, and why does the Well-Architected Framework recommend it?

Defining infrastructure in versioned templates or code (CloudFormation, AWS CDK) instead of manual console clicks. Environments become reproducible, reviewable and quick to rebuild, which supports operational excellence and reliability.

<!-- challenge -->

Users get logged out whenever Auto Scaling removes an instance. What is the cause, and the fix?

<!-- solution -->

Sessions are stored on the instances, so the application is stateful. Move session data to a shared store (ElastiCache or DynamoDB) so any instance can serve any user.

<!-- takeaways -->

- Design for failure: redundancy and automatic recovery.
- Queues and events decouple components.
- Stateless servers and IaC make replacement easy.

<!-- stage: Security -->

### Security, the shared responsibility model and IAM

<!-- unit: Shared responsibility -->

<!-- goals -->

- Explain what AWS secures and what the customer secures.
- Show how responsibilities shift between EC2, RDS and S3.

<!-- concept -->

Security on AWS is split along a line. AWS secures the cloud itself: buildings, hardware, the virtualization layer, the managed services' internals. You secure what you put in it: data, identities, configuration, and anything you install.

Where the line falls depends on the service. The more AWS manages, the less you do, but data, access and configuration always stay yours.

<!-- example -->

| Task | EC2 | RDS | S3 |
|---|---|---|---|
| Physical security | AWS | AWS | AWS |
| OS patching | Customer | AWS | AWS |
| Database engine patching | Customer | AWS | n/a |
| Data, access policies, encryption settings | Customer | Customer | Customer |

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

<!-- challenge -->

A company's S3 bucket was made public by mistake and data leaked. Under the shared responsibility model, whose failure was it, and what control would prevent it?

<!-- solution -->

The customer's: bucket access configuration is their responsibility. S3 Block Public Access at the account level (plus SCPs in Organizations and Config rules) would prevent buckets from becoming public.

<!-- takeaways -->

- AWS secures "of" the cloud; you secure "in" the cloud.
- More managed services move more work to AWS.
- Data, identities and configuration are always yours.

<!-- unit: Root user and IAM identities -->

<!-- goals -->

- Protect the root user and know its exclusive tasks.
- Choose between IAM users, groups and roles.

<!-- concept -->

Every account starts with a root user that can do anything, including closing the account. Because it can't be limited, it should be locked away with MFA and used only for the few tasks that require it.

Daily access goes through IAM. Users represent people or applications with long-term credentials; groups make permissions manageable; roles provide temporary credentials to whoever is trusted to assume them. Roles are the safer default, especially for applications.

<!-- example -->

```text
root user        ─► MFA, no access keys, used only for root-only tasks
group: analysts  ─► policy AnalystsReadOnly ◄─ users ana, luis
role: ec2-app    ─► policy AppS3Access      ◄─ assumed by EC2 instances
```

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

<!-- challenge -->

A developer stores access keys in a config file on an EC2 instance so the app can read S3. What do you recommend?

<!-- solution -->

Create an IAM role with read access to the needed bucket, attach it to the instance through an instance profile, remove the keys from the file and deactivate them. The app gets rotated temporary credentials automatically.

<!-- takeaways -->

- Protect root with MFA; don't use it daily.
- Groups manage user permissions; roles give temporary credentials.
- Applications on AWS should use roles, not keys.

<!-- unit: Policies and permission evaluation -->

<!-- goals -->

- Read an IAM policy statement and its parts.
- Predict the result when policies allow and deny.

<!-- concept -->

Permissions in AWS are written as JSON policies that allow or deny actions on resources, optionally under conditions. Resources are named by ARNs, which is how a policy can point at one bucket or one table.

Evaluation follows a simple rule: everything starts denied, an allow opens access, and an explicit deny always wins. Least privilege means writing allows as narrowly as the task needs and widening them only when necessary.

<!-- example -->

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::sales-reports/*",
    "Condition": {"Bool": {"aws:SecureTransport": "true"}}
  }]
}
```

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

#### What is an ARN?

An Amazon Resource Name uniquely identifies a resource: `arn:partition:service:region:account-id:resource`, for example `arn:aws:s3:::my-bucket`.

<!-- challenge -->

A user has a group policy allowing `s3:*` on all buckets and a user policy denying `s3:DeleteObject` on `finance-*`. Can they delete objects in `finance-2026`?

<!-- solution -->

No. The explicit deny overrides any allow, so deletes on buckets matching `finance-*` are refused, while other S3 actions there remain allowed.

<!-- takeaways -->

- Policies allow or deny actions on resources, with conditions.
- Default deny; allow grants; explicit deny always wins.
- Least privilege: start narrow, widen when needed.

<!-- unit: Credentials and account hygiene -->

<!-- goals -->

- Secure sign-in with MFA and password policies.
- Audit credentials and unused permissions.

<!-- concept -->

Most account compromises start with a stolen credential. MFA makes a stolen password insufficient, password policies make weak ones rarer, and access keys, which never expire on their own, should be few and rotated.

Hygiene also means looking back: who still has old keys, who has permissions they never use. The credential report and Access Advisor answer those questions so you can remove what isn't needed.

<!-- example -->

```bash
aws iam generate-credential-report
aws iam get-credential-report --query Content --output text | base64 -d \
  | cut -d, -f1,4,9,11 | column -t -s,      # user, password, key 1 active, key 1 last rotated
```

#### What is multi-factor authentication (MFA), and which devices does AWS support?

A second factor in addition to the password. AWS supports passkeys and FIDO2 security keys, virtual authenticator apps, and hardware TOTP tokens.

#### What are access keys?

An access key ID and secret access key pair used to sign programmatic requests (CLI, SDK). They are long-term credentials: never commit them to code, rotate them, and prefer roles or IAM Identity Center where possible.

#### What is a password policy in IAM?

Account rules for IAM user passwords: minimum length, required character types, expiry, reuse prevention.

#### What is the IAM credential report?

An account-level CSV listing all users and the status of their credentials: passwords, access keys, MFA, last used dates. Useful for audits.

#### What is IAM Access Advisor?

A view showing which services a user, group or role has permissions for and when they were last accessed. It helps remove unused permissions.

<!-- challenge -->

An audit finds a user with admin rights who hasn't signed in for a year but has an active access key. What do you do?

<!-- solution -->

Check the key's last use; deactivate it, then delete the key and the user if no longer needed. Use Access Advisor on remaining identities to remove unused permissions.

<!-- takeaways -->

- MFA blocks most password-based compromises.
- Access keys don't expire; minimize and rotate them.
- Credential reports and Access Advisor reveal what to remove.

<!-- unit: Federation and temporary credentials -->

<!-- goals -->

- Give workforce users access through IAM Identity Center and federation.
- Explain how STS issues temporary credentials.

<!-- concept -->

In companies with many accounts and many people, creating IAM users everywhere doesn't scale and leaves credentials behind when people leave. Federation lets people sign in with their corporate identity, and IAM Identity Center maps them to permission sets across accounts.

Underneath, STS issues short-lived credentials whenever a role is assumed. Temporary credentials expire on their own, which is why they're safer than long-term keys.

<!-- example -->

```bash
aws sso login --profile data-dev                  # corporate sign-in via Identity Center
aws sts get-caller-identity --profile data-dev    # temporary role credentials
```

#### What is AWS IAM Identity Center?

The successor to AWS Single Sign-On. It centrally manages workforce access to multiple AWS accounts and business applications, using its own directory or an external identity provider (Microsoft Entra ID, Okta, Active Directory).

#### What is identity federation?

Letting users sign in with an existing identity (corporate directory, SAML 2.0 or OIDC provider) and receive temporary AWS credentials, without creating IAM users for them.

#### What is AWS STS?

The AWS Security Token Service issues temporary, limited-privilege credentials, for example when a role is assumed or a federated user signs in.

<!-- challenge -->

A company with 20 AWS accounts creates IAM users in each one for 150 employees. What do you propose?

<!-- solution -->

Connect the corporate identity provider to IAM Identity Center, define permission sets per job role, and assign groups to accounts. Then remove the per-account IAM users and their keys.

<!-- takeaways -->

- Identity Center centralizes workforce access across accounts.
- Federation reuses corporate identities.
- STS credentials expire on their own.

### Security services and compliance

<!-- unit: Multi-account governance -->

<!-- goals -->

- Organize accounts with AWS Organizations and OUs.
- Set guardrails with SCPs and Control Tower.

<!-- concept -->

Companies use many accounts to separate teams, environments and risk. Managing them one by one doesn't scale, so Organizations groups them into organizational units and applies rules from the top.

Service Control Policies set the maximum anyone in an account can do, even administrators: for example, no one can leave approved Regions or disable logging. Control Tower packages this into a ready landing zone with guardrails.

<!-- example -->

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {"StringNotEquals": {"aws:RequestedRegion": ["eu-west-1", "eu-west-3"]}}
}
```

#### What is AWS Organizations?

A service for centrally managing multiple AWS accounts: group them into organisational units (OUs), apply policies, and consolidate billing. A management account owns the organization.

#### What are Service Control Policies (SCPs)?

Policies in AWS Organizations that set the maximum permissions for accounts or OUs. They don't grant permissions: they limit what IAM policies in those accounts can allow, even for the root user of a member account.

#### What is AWS Control Tower?

A service that sets up and governs a secure multi-account environment (a landing zone) following best practices, with preventive and detective guardrails and a dashboard.

<!-- challenge -->

An SCP denies all actions outside two EU Regions. An account administrator has full IAM permissions. Can they launch an instance in us-east-1?

<!-- solution -->

No. SCPs set the maximum permissions for the account, so even an administrator can't act outside the allowed Regions. (Global services may need exceptions in the SCP.)

<!-- takeaways -->

- Organizations groups accounts into OUs.
- SCPs cap what any identity in an account can do.
- Control Tower sets up a governed landing zone.

<!-- unit: Encryption and secrets -->

<!-- goals -->

- Encrypt data at rest and in transit with KMS and ACM.
- Store and rotate secrets with Secrets Manager or Parameter Store.

<!-- concept -->

Encryption protects data in two states. At rest, keys managed in KMS encrypt volumes, objects and databases, and access to the key becomes a second permission check. In transit, TLS certificates from ACM protect traffic to load balancers and CloudFront.

Secrets such as database passwords need their own home. Storing them in a managed service with rotation means they never sit in code and change without redeploying.

<!-- example -->

| Need | Service |
|---|---|
| Encrypt S3, EBS, RDS with keys you control | KMS |
| Single-tenant HSM for strict compliance | CloudHSM |
| HTTPS certificate for a load balancer | ACM |
| Rotating database password | Secrets Manager |
| App configuration values | Parameter Store |

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

<!-- challenge -->

A database password is in the application's source code and was pushed to a public repository. What do you do now and to prevent it next time?

<!-- solution -->

Rotate the password immediately and check logs for misuse. Move it to Secrets Manager with automatic rotation, have the app read it at runtime through its IAM role, and add secret scanning to the repository.

<!-- takeaways -->

- KMS manages encryption keys; CloudHSM gives dedicated HSMs.
- ACM provides and renews TLS certificates.
- Secrets Manager stores and rotates secrets.

<!-- unit: Protecting and detecting -->

<!-- goals -->

- Match AWS security services to threats they address.
- Combine protection, detection and investigation services.

<!-- concept -->

Security services fall into three jobs. Some protect at the edge: Shield absorbs DDoS attacks and WAF filters malicious web requests. Some detect: GuardDuty spots threats in logs, Inspector finds vulnerabilities, Macie finds sensitive data where it shouldn't be. Some help you respond: Security Hub gathers findings in one place, and Detective helps trace what happened.

Knowing which job a service does is usually enough to pick the right one.

<!-- example -->

| Problem | Service |
|---|---|
| SQL injection attempts on a web app | WAF |
| Large DDoS against a website | Shield (Advanced for extra protection) |
| Instance talking to a known malicious IP | GuardDuty |
| Unpatched CVE in a container image | Inspector |
| Credit card numbers in an S3 bucket | Macie |
| One view of all findings across accounts | Security Hub |

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

<!-- challenge -->

GuardDuty reports that an EC2 instance is mining cryptocurrency. Which service helps you understand how it happened, and what do you do first?

<!-- solution -->

Isolate the instance (restrictive security group, snapshot for forensics) and revoke its credentials. Use Detective to trace the activity and entry point, and Inspector to check for the vulnerability that was exploited.

<!-- takeaways -->

- Shield and WAF protect at the edge.
- GuardDuty, Inspector and Macie detect threats, vulnerabilities and sensitive data.
- Security Hub centralizes; Detective investigates.

<!-- unit: Compliance and reporting -->

<!-- goals -->

- Find AWS compliance reports and agreements.
- Know the rules for penetration testing and abuse reports.

<!-- concept -->

Customers inherit part of their compliance from AWS. Auditors want proof that AWS's side is certified, and Artifact provides those reports and agreements on demand. Your side still needs your own controls and evidence.

Testing your own security is allowed for many services without asking, within published rules. When AWS resources are used against you, or yours are abused, the abuse team is the contact.

<!-- example -->

| Need | Where |
|---|---|
| SOC 2 report for an auditor | AWS Artifact |
| Sign a business associate addendum (HIPAA) | AWS Artifact |
| Pen test your EC2 web app | Allowed under the policy, no approval |
| Report spam coming from an AWS IP | AWS Trust & Safety (abuse) |

#### What is AWS Artifact?

A self-service portal for AWS compliance reports (SOC, ISO, PCI DSS) and agreements (such as the Business Associate Addendum for HIPAA).

#### What is the AWS Security Center and the compliance program?

AWS maintains certifications and attestations (ISO 27001, SOC 1/2/3, PCI DSS, HIPAA eligibility, GDPR support) for its infrastructure. Customers inherit the infrastructure controls but must make their own workloads compliant.

#### Do you need permission from AWS to run a penetration test?

Not for a list of permitted services (EC2, RDS, Lambda, CloudFront and others). Some activities remain prohibited, such as DoS attacks, which require a separate approval process for simulated events.

#### What is AWS Abuse, and when do you contact it?

The AWS team to report AWS resources being used for abuse, such as spam, port scanning, DoS attacks or hosting malware.

<!-- challenge -->

An auditor asks for proof that the data center hosting your workload is ISO 27001 certified. What do you provide, and is it enough for your audit?

<!-- solution -->

Download AWS's ISO 27001 certificate from AWS Artifact. It covers AWS's responsibilities only; you must also show your own controls (access, encryption, logging) for your workloads.

<!-- takeaways -->

- Artifact provides AWS compliance reports and agreements.
- AWS compliance covers only AWS's side.
- Pen testing many services needs no approval.

<!-- stage: Core services -->

### Compute: EC2, containers and serverless

<!-- unit: EC2 basics -->

<!-- goals -->

- Describe EC2 instances, AMIs and instance families.
- Understand instance storage and lifecycle.

<!-- concept -->

EC2 rents virtual servers. You choose a template (an AMI with the operating system and software), a size from a family tuned for CPU, memory, storage or accelerators, and a script to run at first boot. Instances then behave like servers you control.

Lifecycle matters for cost and data. Stopped instances keep their EBS volumes and stop paying for compute; terminated ones are gone. Instance store disks are fast but lose data when the instance stops.

<!-- example -->

```bash
aws ec2 run-instances --image-id ami-0abcd1234 --instance-type m7i.large \
  --iam-instance-profile Name=web-app \
  --user-data file://install_web.sh
```

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

#### What is EC2 user data?

A script passed at launch that runs on first boot, used to install software or configure the instance.

#### What is the EC2 instance store?

Temporary block storage physically attached to the host. It is very fast but its data is lost when the instance stops or terminates, so it suits buffers, caches and scratch data.

#### What is the difference between stopping and terminating an instance?

Stopping shuts it down: EBS root volumes are kept and you pay only for storage, and you can start it again. Terminating deletes the instance, and by default its root EBS volume.

<!-- challenge -->

A memory-hungry in-memory analytics app runs on a general-purpose instance and keeps swapping. Which family do you suggest?

<!-- solution -->

A memory-optimized family (R or X), which offers much more RAM per vCPU. Measure memory use first to choose the size.

<!-- takeaways -->

- An AMI is the template; the family sets the resource balance.
- Stop keeps EBS; terminate deletes the instance.
- Instance store data doesn't survive stops.

<!-- unit: Paying for EC2 -->

<!-- goals -->

- Compare On-Demand, Savings Plans, Reserved, Spot and Dedicated options.
- Match a pricing option to a workload pattern.

<!-- concept -->

The same instance can cost very different amounts depending on how you commit. On-Demand is the price of flexibility. Committing to steady usage for one or three years with Savings Plans or Reserved Instances cuts it substantially. Spot sells spare capacity at the deepest discount, but AWS can take it back with two minutes' notice.

So the pricing choice follows the workload: steady baseline on commitments, spikes on On-Demand, interruptible batch on Spot.

<!-- example -->

| Workload | Pricing |
|---|---|
| Web servers running 24/7 for years | Savings Plan |
| Holiday traffic spikes | On-Demand |
| Nightly image rendering, restartable | Spot |
| License tied to physical cores | Dedicated Host |

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

<!-- challenge -->

A company runs 20 instances all year and adds 30 more for two months each winter. How do you price this?

<!-- solution -->

Cover the 20 steady instances with a Savings Plan (Compute Savings Plans keep flexibility), and run the 30 seasonal instances On-Demand, or Spot if the workload tolerates interruptions.

<!-- takeaways -->

- Commit for steady usage; stay On-Demand for spikes.
- Spot is cheapest but interruptible.
- Dedicated Hosts serve per-core licensing and isolation needs.

<!-- unit: Networking and scaling EC2 -->

<!-- goals -->

- Control instance traffic with security groups and access instances safely.
- Scale and balance load with Auto Scaling and ELB.

<!-- concept -->

An instance alone is neither reachable safely nor resilient. Security groups decide which traffic reaches it, and they are stateful, so replies are allowed automatically. Session Manager and Instance Connect give administrators access without long-lived SSH keys.

Resilience and scale come from groups of instances: a load balancer spreads traffic across AZs and stops sending to unhealthy targets, while Auto Scaling replaces failed instances and adjusts capacity to demand.

<!-- example -->

```text
users ─► Application Load Balancer (AZ a, b)
           └─► Auto Scaling group: min 2, desired 4, max 10 (target CPU 50%)
                 security group: allow 443 from the load balancer only
```

#### What is a security group?

A stateful virtual firewall for instances (attached to network interfaces). It has allow rules only. Return traffic is allowed automatically, and by default all inbound traffic is denied and all outbound allowed.

#### What is an Elastic IP address?

A static public IPv4 address you allocate to your account and can attach to an instance. Public IPv4 addresses are charged hourly, whether attached or not.

#### What is EC2 Auto Scaling?

A service that adds or removes EC2 instances in an Auto Scaling group according to policies (target tracking, step, scheduled, predictive), and replaces unhealthy instances. You set minimum, desired and maximum capacity.

#### What is Elastic Load Balancing, and what are its types?

A service that distributes traffic across targets in several AZs and checks their health.
- **Application Load Balancer:** HTTP/HTTPS, layer 7, path and host-based routing.
- **Network Load Balancer:** TCP/UDP/TLS, layer 4, very high performance and static IPs.
- **Gateway Load Balancer:** layer 3, for third-party network appliances such as firewalls.

#### What does EC2 Instance Connect or Session Manager give you?

Ways to access instances without managing SSH keys. Session Manager (part of Systems Manager) even works without opening inbound ports, with sessions logged.

<!-- challenge -->

A web app runs on one instance with an Elastic IP. It went down when the instance failed. How do you redesign it?

<!-- solution -->

Put two or more instances in an Auto Scaling group across two AZs behind an Application Load Balancer, point DNS at the load balancer, and drop the Elastic IP. Failed instances are replaced automatically.

<!-- takeaways -->

- Security groups are stateful instance firewalls.
- Load balancers spread traffic and check health.
- Auto Scaling replaces and adjusts instances.

<!-- unit: Containers and functions -->

<!-- goals -->

- Choose between Lambda, ECS, EKS and Fargate.
- Know where container images are stored.

<!-- concept -->

Containers and functions move work further from servers. Lambda runs a function per event and charges only while it runs, which suits short, spiky work. Containers package an application with its dependencies; ECS and EKS schedule them, and Fargate runs them without managing instances.

The choice depends on how long the work runs, how much control you need, and whether the team already knows Kubernetes.

<!-- example -->

| Workload | Good fit |
|---|---|
| Resize an image when uploaded | Lambda |
| Web API in containers, small team | ECS on Fargate |
| Company standard is Kubernetes | EKS |
| Store and scan images | ECR |

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

<!-- challenge -->

A data processing task runs for 40 minutes each night. A colleague proposes Lambda. Does it fit?

<!-- solution -->

No: Lambda functions are limited to 15 minutes. Run it as a container task on ECS with Fargate (or AWS Batch), which has no such limit and still needs no servers.

<!-- takeaways -->

- Lambda for short, event-driven work (max 15 minutes).
- ECS is simpler; EKS is Kubernetes.
- Fargate runs containers without managing instances.

<!-- unit: Managed platforms -->

<!-- goals -->

- Recognize Elastic Beanstalk, Lightsail, Batch and App Runner use cases.
- Pick the simplest platform that fits.

<!-- concept -->

Some services exist mainly to hide infrastructure decisions. Elastic Beanstalk deploys code onto EC2 with load balancing and scaling configured for you. App Runner does the same for containers and source code with even less to set up. Lightsail offers simple servers at a fixed price for small projects. Batch schedules large numbers of jobs on managed capacity.

They trade control for speed, which is often the right trade for small teams.

<!-- example -->

| Need | Service |
|---|---|
| Deploy a Django app without learning EC2 details | Elastic Beanstalk |
| Run a container web API from a repo | App Runner |
| Small blog with predictable monthly price | Lightsail |
| 10,000 simulation jobs | AWS Batch |

#### What is AWS Elastic Beanstalk?

A platform as a service: you upload application code (Java, .NET, Node.js, Python, PHP, Go, Ruby, Docker) and Beanstalk provisions and manages EC2, load balancing, Auto Scaling and monitoring. The underlying resources remain visible and configurable.

#### What is Amazon Lightsail?

A simplified service for virtual private servers, databases and containers at a predictable monthly price, aimed at simple websites and users new to AWS.

#### What is AWS Batch?

A service that runs batch computing jobs at any scale, provisioning EC2 or Fargate capacity (including Spot) based on the jobs queued.

#### What is AWS App Runner?

A fully managed service that builds and runs web applications and APIs from source code or a container image, with automatic scaling and HTTPS.

<!-- challenge -->

A two-person startup wants to deploy a containerized API with HTTPS and autoscaling this week, with no ops experience. What do you suggest?

<!-- solution -->

AWS App Runner: point it at the container image or repository and it handles build, deployment, HTTPS, load balancing and scaling. Revisit ECS later if they need more control.

<!-- takeaways -->

- Platform services trade control for speed.
- Beanstalk and App Runner deploy apps without infrastructure work.
- Batch runs large job queues on managed capacity.

### Storage

<!-- unit: S3 basics -->

<!-- goals -->

- Describe buckets, objects, durability and storage classes.
- Lower storage costs with classes and lifecycle rules.

<!-- concept -->

S3 stores objects (files with metadata) in buckets, with extremely high durability because each object is copied across several facilities. What varies is how fast and how often you need the data, and storage classes price that: frequent access costs more per gigabyte to store, archives cost little to store but more and longer to retrieve.

Lifecycle rules move objects between classes as they age, so data gets cheaper automatically.

<!-- example -->

```json
{"Rules": [{"ID": "logs", "Status": "Enabled", "Filter": {"Prefix": "logs/"},
  "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"},
                  {"Days": 180, "StorageClass": "GLACIER"}],
  "Expiration": {"Days": 730}}]}
```

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

#### How durable and available is S3 Standard?

Designed for 99.999999999% durability and 99.99% availability, with data stored across at least three AZs.

#### When would you use S3 One Zone-IA?

For infrequently accessed data that can be recreated, such as secondary backup copies or derived data, where losing an AZ is acceptable in exchange for a lower price.

#### What are S3 lifecycle policies?

Rules that automatically transition objects to cheaper storage classes after a given age, or delete them (expiration).

<!-- challenge -->

Application logs are read often for a week, rarely for a year, and must be kept for 7 years for audits. Design a lifecycle.

<!-- solution -->

Keep them in S3 Standard for 30 days, move to Standard-IA, then to Glacier Flexible Retrieval or Deep Archive after a year, and expire them after 7 years.

<!-- takeaways -->

- S3 stores objects in buckets with 11 nines of durability.
- Storage classes trade access speed for price.
- Lifecycle rules move and expire data automatically.

<!-- unit: Protecting and serving S3 data -->

<!-- goals -->

- Protect objects with versioning, access controls, encryption and replication.
- Serve websites and speed up uploads from S3.

<!-- concept -->

S3's defaults are safe (new buckets are private and encrypted), and most incidents come from changing them. Versioning protects against overwrites and deletions, Block Public Access prevents accidental exposure, policies limit who reads what, and replication keeps a copy in another Region.

S3 can also serve content directly, for static websites, usually behind CloudFront, and speed up long-distance uploads through edge locations.

<!-- example -->

```bash
aws s3api put-bucket-versioning --bucket finance-docs --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket finance-docs \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

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

<!-- challenge -->

A user deleted an important folder in a bucket. Versioning was on. Can you recover it, and how?

<!-- solution -->

Yes. With versioning, the delete only added delete markers. Remove the delete markers (or copy the previous versions back), and consider MFA delete or Object Lock for critical buckets.

<!-- takeaways -->

- Versioning protects against overwrites and deletes.
- Block Public Access prevents accidental exposure.
- Replication copies objects to another Region or account.

<!-- unit: Block and file storage -->

<!-- goals -->

- Compare S3, EBS, EFS and FSx.
- Back up EBS volumes with snapshots.

<!-- concept -->

Not all applications can use object storage. Databases and operating systems need block storage, a disk attached to one instance: that's EBS, backed up with incremental snapshots. Applications that share files across many servers need a file system: EFS for Linux, FSx for Windows and specialized file systems.

The choice follows the access pattern: API objects, one-instance disk, or shared files.

<!-- example -->

| Need | Service |
|---|---|
| Boot and database disk for one instance | EBS |
| Shared folder for 20 Linux web servers | EFS |
| Windows file shares with Active Directory | FSx for Windows File Server |
| Images and backups accessed over HTTP | S3 |

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

<!-- challenge -->

Ten Linux servers behind a load balancer must read and write the same uploaded files. Which storage do you choose?

<!-- solution -->

Amazon EFS, mounted by all servers over NFS, or S3 if the application can use an API. EBS volumes attach to one instance, so they don't fit shared access.

<!-- takeaways -->

- EBS is block storage for one instance.
- EFS and FSx are shared file systems.
- S3 is object storage accessed by API.

<!-- unit: Hybrid, transfer and backup -->

<!-- goals -->

- Move data to AWS online and offline.
- Centralize backups across services.

<!-- concept -->

Getting data into AWS depends on volume and bandwidth. Online transfers with DataSync suit ongoing or moderate amounts; when a network transfer would take weeks, Snow devices ship the data physically. Some on-premises applications keep running and use cloud storage through Storage Gateway.

Once workloads run on AWS, backups should be centralized, with policies and audit across services, which is AWS Backup's job.

<!-- example -->

| Situation | Service |
|---|---|
| 500 TB archive, slow office link | Snowball |
| Daily sync from an NFS server to S3 | DataSync |
| On-premises backup app writing to cloud tape | Storage Gateway (Tape Gateway) |
| Backup policy for RDS, EBS and DynamoDB | AWS Backup |

#### What is AWS Storage Gateway?

A hybrid storage service that gives on-premises applications access to cloud storage. Types: S3 File Gateway, FSx File Gateway, Volume Gateway and Tape Gateway (virtual tape library for backups).

#### What is the AWS Snow Family?

Physical devices to move large amounts of data into and out of AWS offline, or to process data at the edge where there is little or no connectivity (AWS Snowball Edge devices).

#### What is AWS DataSync?

An online data transfer service that moves data between on-premises storage (NFS, SMB, HDFS, object stores) and AWS storage services, quickly and with verification.

#### What is AWS Backup?

A central service to automate and audit backups across services: EBS, EC2, RDS, DynamoDB, EFS, FSx, S3 and more, with backup plans and cross-Region or cross-account copies.

<!-- challenge -->

A company must move 200 TB to AWS over a 100 Mbps link. Estimate the online transfer time and suggest an option.

<!-- solution -->

At 100 Mbps, 200 TB takes about 185 days at full speed. Use Snowball Edge devices to ship the data, then DataSync for the changes made during shipping.

<!-- takeaways -->

- DataSync moves data online; Snow devices ship it.
- Storage Gateway links on-premises apps to cloud storage.
- AWS Backup centralizes backup policies.

### Databases and analytics

<!-- unit: Relational databases -->

<!-- goals -->

- Compare RDS, Aurora and DynamoDB.
- Distinguish Multi-AZ from read replicas, and use DMS for migrations.

<!-- concept -->

Relational databases on AWS come managed: RDS runs familiar engines and handles backups, patching and failover; Aurora is AWS's cloud-native engine with storage replicated across zones. DynamoDB is a different model, a key-value store that scales without servers.

Two RDS features are often confused. Multi-AZ is for availability: a standby takes over if the primary fails. Read replicas are for scale: they serve reads. DMS moves existing databases in with little downtime.

<!-- example -->

| Need | Choice |
|---|---|
| Survive an AZ failure | RDS Multi-AZ |
| Offload reporting reads | Read replica |
| Shopping cart with millions of users, key access | DynamoDB |
| Move on-premises Oracle to PostgreSQL | DMS (+ Schema Conversion) |

#### How does Amazon RDS differ from Amazon DynamoDB?

RDS is a managed relational database service (SQL, schemas, joins, transactions) running MySQL, PostgreSQL, MariaDB, Oracle, SQL Server or Db2 on instances you size. DynamoDB is a serverless NoSQL key-value and document database with single-digit millisecond performance at any scale, no fixed schema beyond the keys, and automatic scaling.

#### What does Amazon RDS manage for you?

Provisioning, operating system and database patching, automated backups and point-in-time recovery, Multi-AZ failover, read replicas, monitoring and storage scaling. You manage schema, queries, users and network access.

#### What is the difference between RDS Multi-AZ and read replicas?

Multi-AZ keeps a synchronous standby (or standbys) in another AZ for high availability and automatic failover. It is not meant to serve reads in the classic setup. Read replicas are asynchronous copies used to scale read traffic, possibly in other Regions, and can be promoted.

#### What is Amazon Aurora?

A cloud-native relational database compatible with MySQL and PostgreSQL. It stores six copies of data across three AZs, scales storage automatically, and offers Aurora Serverless for variable workloads.

#### What is AWS Database Migration Service (DMS)?

A service that migrates databases to AWS with minimal downtime, between the same engines (homogeneous) or different engines (heterogeneous, with the Schema Conversion Tool), and can replicate ongoing changes.

<!-- challenge -->

Reports slow down an RDS database during business hours. The team proposes enabling Multi-AZ. Is that the right fix?

<!-- solution -->

No. Multi-AZ standbys don't serve reads; they're for failover. Add a read replica and point reports to it (or move reporting to a warehouse).

<!-- takeaways -->

- RDS manages engines; Aurora is cloud-native; DynamoDB is key-value.
- Multi-AZ is availability; read replicas are read scale.
- DMS migrates databases with minimal downtime.

<!-- unit: Purpose-built databases -->

<!-- goals -->

- Match caching, document, graph, wide-column and time-series needs to services.
- Know when an in-memory store helps.

<!-- concept -->

AWS's approach is "the right database for the job". Instead of forcing every data shape into tables, it offers engines built for specific access patterns: in-memory caches for microsecond reads, document stores for JSON, graphs for relationships, wide-column stores for massive writes, time series for metrics.

The question to ask is how the application reads and writes data; the engine follows.

<!-- example -->

| Access pattern | Service |
|---|---|
| Cache product pages | ElastiCache |
| Durable Redis-compatible primary store | MemoryDB |
| MongoDB-style documents | DocumentDB |
| Fraud rings, social graphs | Neptune |
| Cassandra workloads | Keyspaces |
| IoT sensor readings | Timestream |

#### What is Amazon ElastiCache?

Managed in-memory caching with Valkey, Redis OSS or Memcached, used to reduce database load and serve frequent reads with microsecond latency.

#### What is Amazon MemoryDB?

A durable in-memory database compatible with Valkey and Redis OSS, usable as a primary database thanks to its multi-AZ transaction log.

#### What is Amazon DocumentDB?

A managed document database compatible with MongoDB workloads.

#### What is Amazon Neptune?

A managed graph database for highly connected data such as social networks, fraud detection and knowledge graphs.

#### What is Amazon Keyspaces?

A serverless managed database compatible with Apache Cassandra.

#### What is Amazon Timestream?

A managed time-series database for IoT and operational metrics.

<!-- challenge -->

An e-commerce site's product pages query the database on every view and it's overloaded. What do you add?

<!-- solution -->

An ElastiCache cache in front of the database: cache rendered product data with a sensible expiry, so most views never reach the database.

<!-- takeaways -->

- Pick the database for the access pattern.
- Caches cut database load and latency.
- Graph, document and time-series stores fit specific shapes.

<!-- unit: Analytics services -->

<!-- goals -->

- Distinguish OLTP from OLAP and the services for each.
- Place Redshift, Athena, Glue, EMR and Lake Formation in a data platform.

<!-- concept -->

Transactional systems answer many small questions fast; analytical systems answer big questions over lots of history. Mixing them slows both, so analytics usually moves to a separate platform.

On AWS that platform has interchangeable parts: S3 as the lake, Glue to catalog and transform, Lake Formation to govern, Athena for serverless SQL on files, Redshift as a warehouse for heavy BI, and EMR for big-data frameworks.

<!-- example -->

```text
RDS (OLTP) ─► DMS / Glue ─► S3 data lake ─► Athena (ad hoc SQL)
                               │  Glue Data Catalog + Lake Formation
                               └─► Redshift (dashboards)   EMR (Spark)
```

#### What is Amazon Redshift?

A managed, petabyte-scale cloud data warehouse for analytical SQL queries (OLAP), with columnar storage, a serverless option and the ability to query data in S3.

#### What is the difference between OLTP and OLAP, and which AWS services fit each?

OLTP handles many small transactional reads and writes (orders, payments): RDS, Aurora, DynamoDB. OLAP runs large analytical queries over historical data: Redshift, Athena.

#### What is Amazon Athena?

A serverless interactive query service to analyze data in S3 with standard SQL. You pay per amount of data scanned, so columnar formats and partitioning reduce cost.

#### What is AWS Glue?

A serverless data integration service: crawlers to discover schemas, the Glue Data Catalog as a central metadata store, and Spark-based ETL jobs.

#### What is Amazon EMR?

A managed big-data platform to run Apache Spark, Hive, Presto/Trino, HBase and other frameworks on EC2, EKS or serverless.

#### What is AWS Lake Formation?

A service to build, secure and manage a data lake on S3, with central fine-grained permissions on Glue Data Catalog tables.

<!-- challenge -->

Analysts want to run occasional SQL over three years of log files in S3 without loading them anywhere. Which service fits?

<!-- solution -->

Amazon Athena with tables in the Glue Data Catalog: queries run directly on S3 and you pay per data scanned. Converting logs to Parquet keeps costs low.

<!-- takeaways -->

- OLTP for transactions; OLAP for analysis.
- Athena queries S3; Redshift serves heavy BI.
- Glue and Lake Formation catalog and govern the lake.

<!-- unit: Streaming, search and BI -->

<!-- goals -->

- Recognize Kinesis, OpenSearch and QuickSight use cases.
- Build a simple real-time-to-dashboard flow.

<!-- concept -->

Some data is valuable only while it's fresh: clicks, sensor readings, logs. Kinesis captures and delivers those streams, either for custom processing or straight into storage. OpenSearch indexes text and logs so you can search and explore them interactively.

At the end of most pipelines sits a BI tool; QuickSight provides serverless dashboards that business users can explore and share.

<!-- example -->

```text
app clicks ─► Kinesis Data Streams ─► consumers (real-time alerts)
           └► Firehose ─► S3 ─► Athena ─► QuickSight dashboard
app logs   ─► OpenSearch Service (search, log analytics)
```

#### What is Amazon Kinesis?

Services for real-time streaming data. Kinesis Data Streams captures and stores streams for custom processing. Amazon Data Firehose loads streams into destinations such as S3, Redshift or OpenSearch.

#### What is Amazon OpenSearch Service?

A managed service for OpenSearch (and legacy Elasticsearch) clusters, used for log analytics, full-text search and observability.

#### What is Amazon QuickSight?

A serverless business intelligence service to build interactive dashboards and reports, with machine-learning insights and natural-language questions.

<!-- challenge -->

Support engineers want to search application error logs by keyword within seconds of an error. Which service do you suggest?

<!-- solution -->

Amazon OpenSearch Service, fed by the logs (for example through Firehose or CloudWatch subscriptions), with OpenSearch Dashboards for search and visualizations.

<!-- takeaways -->

- Kinesis captures and delivers streaming data.
- OpenSearch powers search and log analytics.
- QuickSight provides serverless BI dashboards.

### Networking and content delivery

<!-- unit: VPC building blocks -->

<!-- goals -->

- Describe VPCs, CIDR blocks and subnets.
- Route traffic with internet gateways, NAT gateways and bastions.

<!-- concept -->

A VPC is your private network in a Region, with an address range you choose. Subnets divide it by AZ and by exposure. What makes a subnet public is not a setting but a route to an internet gateway; private subnets have none, so their resources can't be reached from the internet.

Private resources still need to download updates, which NAT gateways allow in one direction only. Administrative access goes through a hardened bastion or, better, Session Manager.

<!-- example -->

```text
VPC 10.0.0.0/16
 ├─ public subnet  10.0.1.0/24  (AZ a)  route 0.0.0.0/0 → internet gateway   [load balancer, NAT]
 └─ private subnet 10.0.11.0/24 (AZ a)  route 0.0.0.0/0 → NAT gateway        [app servers, DB]
```

#### What is Amazon VPC?

Virtual Private Cloud is a logically isolated virtual network in a Region where you launch resources. You choose its IP range and create subnets, route tables and gateways.

#### What is a CIDR block?

A notation for an IP address range, such as 10.0.0.0/16, used to define the address space of a VPC and its subnets.

#### What is the difference between a public and a private subnet?

A public subnet has a route to an internet gateway, so resources with public IPs can be reached from the internet. A private subnet has no such route; its resources can reach the internet only through a NAT gateway, if at all.

#### What is an internet gateway?

A VPC component that allows communication between resources in the VPC and the internet.

#### What is a NAT gateway?

A managed service that lets instances in private subnets start outbound connections to the internet (for updates, for example) while blocking unsolicited inbound connections.

#### What is a bastion host?

An instance in a public subnet used as a hardened entry point for SSH or RDP access to instances in private subnets. Systems Manager Session Manager often replaces it.

<!-- challenge -->

Database servers must not be reachable from the internet but need to download OS patches. Where do you place them, and how do they get patches?

<!-- solution -->

In private subnets with no route to the internet gateway, and a route to a NAT gateway in a public subnet for outbound traffic only. Better still, use VPC endpoints and Systems Manager Patch Manager.

<!-- takeaways -->

- A route to an internet gateway makes a subnet public.
- NAT gateways allow outbound-only internet access.
- Keep databases and app servers in private subnets.

<!-- unit: Network security and private access -->

<!-- goals -->

- Compare security groups and network ACLs.
- Reach AWS services privately and log network traffic.

<!-- concept -->

Network defense has two layers. Security groups protect each resource and remember connections, so replies flow back automatically. Network ACLs protect whole subnets, evaluate rules in order, and need explicit rules both ways. Most designs rely on security groups and keep ACLs simple.

Traffic to AWS services doesn't need the internet either: endpoints and PrivateLink keep it on the AWS network. Flow Logs record what actually passed.

<!-- example -->

| | Security group | Network ACL |
|---|---|---|
| Applies to | Network interface | Subnet |
| State | Stateful | Stateless |
| Rules | Allow only | Allow and deny, numbered |

#### What is the difference between a security group and a network ACL?

A security group works at the instance (network interface) level, is stateful and supports allow rules only. A network ACL works at the subnet level, is stateless (return traffic must be allowed explicitly), supports allow and deny rules, and evaluates rules in number order.

#### What are VPC Flow Logs?

Records of IP traffic going to and from network interfaces in a VPC, sent to CloudWatch Logs or S3 for troubleshooting and security analysis.

#### What is a VPC endpoint?

A private connection from a VPC to AWS services without going through the internet. Gateway endpoints serve S3 and DynamoDB. Interface endpoints (AWS PrivateLink) serve many other services.

#### What is AWS PrivateLink?

Technology that exposes services privately across VPCs and accounts through interface endpoints, keeping traffic on the AWS network.

<!-- challenge -->

You must block one malicious IP range from reaching any instance in a subnet. Security group or NACL?

<!-- solution -->

A network ACL with a deny rule for that range, numbered before the allow rules: security groups can't deny, they only allow.

<!-- takeaways -->

- Security groups: stateful, per resource, allow only.
- NACLs: stateless, per subnet, allow and deny.
- Endpoints keep traffic to AWS services private.

<!-- unit: Connecting networks -->

<!-- goals -->

- Connect VPCs with peering and Transit Gateway.
- Connect offices and users with VPN and Direct Connect.

<!-- concept -->

As companies grow, networks multiply: many VPCs, offices, data centers and remote workers. Peering connects two VPCs directly, but doesn't chain, so many VPCs become a mesh. Transit Gateway replaces the mesh with a hub.

For on-premises links, VPN is quick and encrypted over the internet; Direct Connect is a private line with steady performance that takes weeks to set up. Client VPN serves individual users.

<!-- example -->

| Need | Service |
|---|---|
| Two VPCs share a database | VPC peering |
| 40 VPCs and two data centers | Transit Gateway |
| Office link this week | Site-to-Site VPN |
| Steady 10 Gbps to AWS | Direct Connect |
| Remote employees | Client VPN |

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

<!-- challenge -->

A company needs a reliable, high-bandwidth link to AWS but can't wait months, and must be covered if the link fails. What do you set up?

<!-- solution -->

Order Direct Connect for steady bandwidth and set up a Site-to-Site VPN right away; keep the VPN as a backup path once Direct Connect is live.

<!-- takeaways -->

- Peering links two VPCs; Transit Gateway links many.
- VPN is quick and encrypted; Direct Connect is private and steady.
- Client VPN connects individual users.

<!-- unit: DNS and content delivery -->

<!-- goals -->

- Route users with Route 53 and its routing policies.
- Speed up applications with CloudFront, Global Accelerator and API Gateway.

<!-- concept -->

Users reach applications through names and networks you can shape. Route 53 answers DNS queries and can send users to the closest, healthiest or a weighted endpoint. CloudFront caches content near users so most requests never reach your servers. Global Accelerator puts traffic on AWS's backbone early for non-cacheable traffic.

API Gateway fronts APIs with authentication, throttling and monitoring, often in front of Lambda.

<!-- example -->

| Goal | Route 53 policy |
|---|---|
| Send 10% of users to a new version | Weighted |
| Fail over to a standby Region | Failover |
| Serve users from the fastest Region | Latency |
| Serve French content to France | Geolocation |

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

<!-- challenge -->

A website hosted in eu-west-1 is slow for users in Asia, mostly because of large images. What do you add first?

<!-- solution -->

Amazon CloudFront in front of the site (or the S3 bucket with images), so content is cached at edge locations near Asian users.

<!-- takeaways -->

- Route 53 routes by weight, latency, health or location.
- CloudFront caches content at the edge.
- API Gateway fronts and protects APIs.

<!-- stage: Operating and paying -->

### Management, governance and developer tools

<!-- unit: Monitoring and auditing -->

<!-- goals -->

- Distinguish CloudWatch, CloudTrail and Config.
- Trace requests and follow AWS service health.

<!-- concept -->

Three questions need three services. Is it healthy? CloudWatch collects metrics and logs and raises alarms. Who did what? CloudTrail records every API call. Is it configured as it should be? Config records resource settings over time and checks them against rules.

For distributed applications, X-Ray follows a request through services, and the Health Dashboard tells you when AWS itself has a problem affecting you.

<!-- example -->

| Question | Service |
|---|---|
| CPU above 80% for 10 minutes? | CloudWatch alarm |
| Who deleted the security group? | CloudTrail |
| Are all buckets encrypted? | Config rule |
| Which service slows checkout? | X-Ray |
| Is an AWS outage hitting my Region? | Health Dashboard |

#### What is Amazon CloudWatch?

A monitoring and observability service: metrics, alarms, logs (CloudWatch Logs), dashboards and events, for AWS resources and applications.

#### What is AWS CloudTrail?

A service that records API calls and account activity (who did what, when, from where) for governance, compliance and auditing. Logs can be delivered to S3 and analyzed with CloudTrail Lake.

#### What is the difference between CloudWatch and CloudTrail?

CloudWatch monitors performance and health (metrics, logs, alarms). CloudTrail audits actions (API calls made in the account).

#### What is AWS Config?

A service that records resource configurations and their changes over time and evaluates them against rules, for compliance auditing and troubleshooting.

#### What is AWS X-Ray?

A service that traces requests through distributed applications to find performance bottlenecks and errors.

#### What is the AWS Health Dashboard?

A view of AWS service health and of events that affect your own resources, such as scheduled maintenance or issues in your Regions.

<!-- challenge -->

A production security group was opened to the whole internet last night. How do you find who did it and get alerted next time?

<!-- solution -->

Search CloudTrail for the `AuthorizeSecurityGroupIngress` call to find the identity and time. Add a Config rule (or EventBridge rule) that flags open security groups and notifies the team, with automatic remediation if desired.

<!-- takeaways -->

- CloudWatch: health. CloudTrail: activity. Config: configuration.
- X-Ray traces distributed requests.
- The Health Dashboard reports AWS issues affecting you.

<!-- unit: Managing and automating -->

<!-- goals -->

- Interact with AWS through the console, CLI, SDKs and IaC.
- Automate infrastructure, operations and deployments.

<!-- concept -->

Everything in AWS is an API, and the console, CLI and SDKs are just different ways to call it. Repeatable work should go through code: CloudFormation and CDK describe infrastructure, Systems Manager runs operational tasks across fleets, and the Code* services build and deploy software.

Trusted Advisor closes the loop by reviewing the account and pointing out savings, risks and limits.

<!-- example -->

```yaml
# CloudFormation: a versioned, private S3 bucket
Resources:
  ReportsBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration: {Status: Enabled}
      PublicAccessBlockConfiguration: {BlockPublicAcls: true, BlockPublicPolicy: true,
                                       IgnorePublicAcls: true, RestrictPublicBuckets: true}
```

#### What are the ways to interact with AWS?

The AWS Management Console (web), the AWS CLI, the SDKs for programming languages, infrastructure as code (CloudFormation, CDK) and AWS CloudShell (a browser-based shell already authenticated).

#### What is AWS CloudFormation?

Infrastructure as code: you describe resources in JSON or YAML templates, and CloudFormation creates, updates and deletes them as a stack, in the right order.

#### What is the AWS Cloud Development Kit (CDK)?

A framework to define cloud infrastructure in programming languages (TypeScript, Python, Java, C#, Go). It synthesizes CloudFormation templates.

#### What is AWS Systems Manager?

A set of operational tools for managing EC2 and on-premises servers at scale: Session Manager, Patch Manager, Run Command, Parameter Store, Automation and inventory.

#### What are AWS CodeCommit, CodeBuild, CodeDeploy and CodePipeline?

Developer tools for CI/CD: CodeBuild compiles and tests code, CodeDeploy automates deployments to EC2, Lambda, ECS and on premises, CodePipeline orchestrates release pipelines. CodeCommit is a Git hosting service that is closed to new customers.

#### What is AWS Trusted Advisor?

A service that inspects your account and recommends improvements in five categories: cost optimization, performance, security, fault tolerance and service quotas. Basic and Developer Support plans get core checks only. Business and higher plans get the full set.

<!-- challenge -->

A team creates test environments by clicking in the console, and each one ends up slightly different. What do you propose?

<!-- solution -->

Define the environment in CloudFormation or CDK, store it in Git, and create every environment from the same template with parameters. Deploy changes through a pipeline instead of the console.

<!-- takeaways -->

- Console, CLI and SDKs all call the same APIs.
- CloudFormation and CDK make infrastructure repeatable.
- Trusted Advisor checks cost, security, limits and more.

<!-- unit: Decoupling applications -->

<!-- goals -->

- Choose between SQS, SNS and EventBridge.
- Decouple producers from consumers.

<!-- concept -->

When one component calls another directly, a slowdown in one spreads to both. Messaging services break that link. A queue holds work until a consumer is ready; a topic delivers each message to many subscribers at once; an event bus routes events by content to the right targets, including AWS services and SaaS.

The difference is in delivery: one consumer per message, all subscribers, or rule-based routing.

<!-- example -->

| Pattern | Service |
|---|---|
| Orders processed by a pool of workers | SQS |
| Send one alert to email, SMS and a Lambda | SNS |
| Route "order placed" events to billing and analytics by rules | EventBridge |

#### What is Amazon SQS?

Simple Queue Service is a fully managed message queue that decouples components. Standard queues give high throughput with at-least-once delivery. FIFO queues guarantee order and exactly-once processing.

#### What is the difference between SQS and SNS?

SQS is a queue: consumers poll messages, each message is processed by one consumer. SNS is publish/subscribe: a message published to a topic is pushed to all subscribers (SQS, Lambda, HTTP, email, SMS). They are often combined in a fan-out pattern.

#### What is Amazon EventBridge?

A serverless event bus that routes events from AWS services, SaaS applications and your own code to targets based on rules, and schedules tasks (EventBridge Scheduler).

<!-- challenge -->

An order service calls the email service directly; when email is slow, checkout times out. How do you fix it?

<!-- solution -->

Publish order events to an SQS queue (or SNS topic with an SQS subscription) and let the email service consume them at its own pace. Checkout finishes as soon as the message is stored.

<!-- takeaways -->

- SQS queues work for one consumer per message.
- SNS fans out to many subscribers.
- EventBridge routes events by rules.

### Billing, pricing and support

<!-- unit: What drives cost -->

<!-- goals -->

- Name the main cost drivers on AWS.
- Estimate costs and use the Free Tier wisely.

<!-- concept -->

AWS bills mainly for three things: compute time, stored data and data leaving AWS. Most surprises come from forgetting one of them, such as idle instances or large outbound transfers. The Free Tier helps you learn, within limits that are easy to exceed.

Cost work starts before building, with an estimate, and continues after, by removing waste and committing to steady usage.

<!-- example -->

| Cost driver | Example | Lever |
|---|---|---|
| Compute | 10 instances 24/7 | Rightsize, Savings Plans, stop when idle |
| Storage | 50 TB in S3 Standard | Lifecycle to cheaper classes |
| Data transfer out | Video served from EC2 | CloudFront, compression |

#### What are the three fundamental drivers of AWS cost?

Compute, storage and outbound data transfer. Inbound data transfer is generally free.

#### What is the AWS Free Tier?

Offers that let you try AWS at no cost within limits. It includes always-free offers (for example Lambda requests and DynamoDB storage up to a limit), credits or 12-month offers for new accounts depending on the account plan, and short free trials of specific services. Usage beyond the limits is billed.

#### What is the AWS Pricing Calculator?

A free tool to estimate the cost of an architecture before building it.

#### How can you reduce costs on AWS?

Rightsize instances, turn off unused resources, use Savings Plans or Reserved Instances for steady workloads and Spot for interruptible ones, choose cheaper storage classes with lifecycle rules, use serverless for variable load, reduce data transfer (for example with CloudFront and VPC endpoints), and track spending with tags, Budgets and Cost Explorer.

<!-- challenge -->

A student's Free Tier account produced a 90 USD bill. Name two likely causes and how to avoid them.

<!-- solution -->

Resources outside Free Tier limits (a larger instance, a NAT gateway, an RDS instance left running) or usage after the 12-month offers ended. Set a budget alert at a low amount and delete resources after experiments.

<!-- takeaways -->

- Compute, storage and outbound transfer drive cost.
- Estimate with the Pricing Calculator before building.
- The Free Tier has limits; set budget alerts.

<!-- unit: Tracking and controlling spend -->

<!-- goals -->

- Analyze and forecast spend with Cost Explorer and detailed exports.
- Control and attribute costs with budgets, tags and consolidated billing.

<!-- concept -->

You can't control what you can't see. Cost Explorer shows trends and forecasts; detailed exports give line-level data for your own analysis; tags attribute costs to projects and teams. Budgets add alerts, and Compute Optimizer suggests better sizes from actual use.

In organizations, consolidated billing combines usage across accounts, which reaches volume discounts sooner and lets commitments benefit the whole company.

<!-- example -->

```bash
aws budgets create-budget --account-id 123456789012 --budget '{
  "BudgetName": "data-team-monthly", "BudgetLimit": {"Amount": "5000", "Unit": "USD"},
  "TimeUnit": "MONTHLY", "BudgetType": "COST",
  "CostFilters": {"TagKeyValue": ["user:team$data"]}}'
```

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

<!-- challenge -->

Finance wants each team's monthly AWS cost, but all teams share accounts. What do you set up?

<!-- solution -->

Define a `team` tag, require it on resources (tag policies, SCPs or IaC), activate it as a cost allocation tag, and report by tag in Cost Explorer with a budget per team. Separate accounts per team is the longer-term fix.

<!-- takeaways -->

- Cost Explorer shows and forecasts spend.
- Tags and accounts attribute costs to owners.
- Consolidated billing shares discounts across accounts.

<!-- unit: Support and partners -->

<!-- goals -->

- Compare AWS Support plans and what each includes.
- Know where to get help: re:Post, TAMs, Marketplace and partners.

<!-- concept -->

Help on AWS comes in tiers. Everyone gets documentation, the re:Post community and basic checks. Paid support plans add technical cases with faster response times as the plan rises, and the top tiers add a Technical Account Manager who knows your environment.

Beyond AWS itself, partners and Professional Services provide consulting, and the Marketplace sells ready software that runs on AWS, billed through your AWS account.

<!-- example -->

| Need | Plan or resource |
|---|---|
| Learning, no production | Basic + re:Post |
| Production workload, business hours issues | Developer or Business |
| Business-critical, 24/7 fast response | Business or Enterprise On-Ramp |
| Dedicated TAM, critical systems | Enterprise |

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

<!-- challenge -->

A company's production site is down at 2 a.m. and it has the Developer plan. What support can it get, and which plan would fit better?

<!-- solution -->

Developer gives business-hours email support for general guidance, not urgent production cases. Business (or higher) adds 24/7 phone and chat with a fast response for production system down.

<!-- takeaways -->

- Support plans differ in response times and access.
- Enterprise plans include a TAM.
- Marketplace and partners extend what AWS provides.
