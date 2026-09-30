# Business Requirements Document (BRD)
**Project Title:** Post-Purchase Logistics & Customer Retention Optimization  
**Project Key:** OCR (Olist Customer Retention)  
**Lead Business Analyst:** Shrey Gupta  
**Stakeholders:** VP of Operations, Head of Logistics, Category Managers, Customer Experience (CX) Team  

---

## 1. Executive Summary & Problem Statement
* **Current State:** Analysis of 100k+ transactions indicates a critical baseline repeat purchase rate of only **3.0%** (97% single-order churn across ~93.4k unique buyers).
* **Core Bottleneck:** Logistics delay is the primary driver of customer sentiment collapse. While on-time deliveries achieve a **4.29 / 5.0 CSAT** with a 6.6% 1-star rating rate, delayed deliveries experience an **8.1x surge in 1-star reviews (53.7%)** and an average rating drop to **2.27 / 5.0**.
* **Category Exposure:** Bulky freight categories—specifically `Office Furniture`—exhibit a **20.37% 1-star review rate** and an average review score of 3.52.
* **Objective:** Implement automated milestone tracking, dynamic SLA risk prediction, and proactive churn mitigation protocols to elevate repeat retention from 3.0% to 5.0% over two fiscal quarters.

---

## 2. Project Scope (In-Scope vs. Out-of-Scope)
* **In-Scope:**
  * Root cause quantification linking fulfillment lead time against customer review scores.
  * Integration of carrier tracking webhooks for automated Day $(N-1)$ delivery delay alerts.
  * Automated issuance of goodwill apology vouchers (₹100 credit) upon detected SLA breaches.
  * Executive Power BI dashboard tracking real-time SLA breach rates and CSAT impact.
* **Out-of-Scope:**
  * Renegotiating primary 3PL line-haul contracts.
  * Redesigning front-end checkout UI or checkout payment gateway integration.

---

## 3. Business Requirements & Functional Specifications

| Req ID | Category | Requirement Description | Success Metric / Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **BR-01** | Data Pipeline | Daily ETL pipeline aggregating carrier transit timestamps against estimated delivery dates. | 100% orders classified as `On-Time` or `Late` within 2 hours of delivery mark. |
| **BR-02** | Risk Engine | Predictive trigger flagging in-transit shipments exceeding Day $(N-1)$ of the estimated SLA. | System flags delayed shipments $\ge 24$ hours prior to scheduled SLA breach. |
| **BR-03** | CX Automation | Automated SMS/Email notification sent upon breach flag with dynamic goodwill discount coupon. | Delivery notification dispatched before customer logs a complaint; voucher claimed rate $\ge 15\%$. |
| **BR-04** | BI Reporting | Executive dashboard reporting monthly retention, category breach volumes, and CSAT breakdown. | Drill-down enabled by state, seller, and product category; daily automated data refresh. |

---

## 4. User Stories & Acceptance Criteria

### OCR-1: Establish Baseline Retention Metric
* **User Story:** *As a Business Analyst, I need to evaluate customer purchase frequency so the business can benchmark customer retention against marketplace standards.*
* **Acceptance Criteria:** Given the delivered orders dataset, query distinct customer identifiers (`customer_unique_id`) to compute the exact ratio of multi-order buyers.

### OCR-2: Quantify Logistics CSAT Impact
* **User Story:** *As an Operations Manager, I want to segment review scores by delivery timeliness to measure customer sentiment sensitivity to fulfillment delays.*
* **Acceptance Criteria:** Given delivery timestamps and estimated dates, calculate average review scores and percentage of 1-star reviews for on-time vs. late shipments.

### OCR-3: Isolate Churn-Driving Categories
* **User Story:** *As a Category Lead, I need to isolate categories with disproportionate negative reviews to deploy freight packaging and carrier adjustments.*
* **Acceptance Criteria:** Filter delivered orders by product category (minimum threshold $\ge 500$ orders) and rank by descending volume and percentage of 1-star reviews.

### OCR-4: Executive KPI Dashboard
* **User Story:** *As an Executive Stakeholder, I need an interactive Power BI dashboard displaying delivery SLA breaches and CSAT distribution.*
* **Acceptance Criteria:** Deliver an interactive visual interface supporting filtering by delivery performance, top 10 categories, and monthly order trends.

---

## 5. Success Metrics & Target KPIs
* **Repeat Purchase Rate:** Increase from **3.0% to 5.0%** within 6 months.
* **Late Delivery 1-Star CSAT Surge:** Reduce 1-star ratings on delayed shipments from **53.7% to $<30\%$** via proactive communication.
* **Office Furniture CSAT:** Lift average category score from **3.52 to $\ge 4.0$**.
