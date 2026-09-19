# Stakeholder Map and User Personas — MacroOps AI
**Author:** Shivya
**Date:** September 18, 2026


**Note:** The personas below are representative user personas created for product discovery. Names, locations, store IDs, ages, and experience levels are fictional and are used to model typical stakeholder needs.


---

## Stakeholder Map

### Primary Stakeholders (Direct Users)
These people will interact with MacroOps AI every day:

1. Operations Manager — manages day-to-day operations of one store
2. Fulfillment Manager — oversees picking, packing, and dispatch
3. Delivery Operations Manager — manages riders and assignments
4. Frontline Picker — physically picks items in the warehouse

### Secondary Stakeholders (Indirect Users)
These people benefit from MacroOps AI but may not use it directly:

5. Regional Manager — oversees multiple stores across a city
6. Business Analyst — uses reports for strategy and planning

### Technical Stakeholders
7. IT / DevOps Team — deploys and maintains the system

---

## User Persona 1 — The Operations Manager

**Name:** Rahul Sharma
**Role:** Operations Manager, Mumbai Dark Store (ST044)
**Age:** 32
**Experience:** 4 years in e-commerce operations

**A Day in Rahul's Life:**
Rahul arrives at 8am and immediately opens four different systems
— the OMS to check order status, the WMS for inventory, a delivery
tracking app for riders, and WhatsApp for team updates. He spends
the first 90 minutes just trying to understand what is happening.
At 10am, he gets a customer complaint about a late order. He
manually traces it through three systems to find out the picker
took 28 minutes. By the time he identifies the problem and
reassigns the picker, five more orders are already late.

**Goals:**
- Know what is happening across the store at a glance
- Catch problems before they become customer complaints
- Have one place for all operational information
- Reduce the time he spends on manual investigation

**Pain Points:**
- Too many systems to monitor simultaneously
- Finds out about problems too late to act
- Cannot predict which orders will be late
- Spends 2+ hours daily just gathering information

**What He Needs from MacroOps AI:**
- Single dashboard showing all KPIs in real time
- Proactive SLA breach alerts with root cause explanation
- AI assistant to answer operational questions instantly
- Exception list with recommended actions

**Quote:**
"By the time I find out an order is going to be late,
it is already late."

---

## User Persona 2 — The Fulfillment Manager

**Name:** Priya Nair
**Role:** Fulfillment Manager, Bengaluru Hub (ST019)
**Age:** 28
**Experience:** 2 years in warehouse operations

**A Day in Priya's Life:**
Priya manages 40 pickers across three shifts. She monitors
picking performance through a handheld scanner system that shows
individual picker activity but gives her no aggregate view. She
notices slow pickers only when a team lead complains or when a
customer complaint is traced back to slow picking. Inventory
discrepancies are discovered randomly when pickers report missing
items mid-pick.

**Goals:**
- See picker productivity in real time across all 40 pickers
- Identify picking bottlenecks before orders are affected
- Know about inventory issues before pickers encounter them
- Reduce missing items in completed orders

**Pain Points:**
- No aggregate view of picking performance
- Inventory system does not match physical reality
- Missing items discovered only during picking, not before
- Cannot easily identify which SKUs cause the most problems

**What She Needs from MacroOps AI:**
- Picker performance dashboard with speed and accuracy
- Inventory discrepancy alerts before picking begins
- SKU-level stockout and variance monitoring
- Alerts for slow picking in progress

---

## User Persona 3 — The Delivery Operations Manager

**Name:** Arjun Mehta
**Role:** Delivery Operations Manager, Delhi Region (ST098)
**Age:** 35
**Experience:** 6 years in logistics and delivery

**A Day in Arjun's Life:**
Arjun manages 200 delivery riders across 15 dark stores. During
peak hours (7-9pm), he receives calls from store managers about
rider shortages. He manually reallocates riders from less busy
stores to busier ones. He has no tool that predicts when a shortage
will occur — he only finds out when it has already happened.
Assignment delays average 8.17 minutes but he has no
visibility into which stores are consistently worse.

**Goals:**
- Predict rider demand before peak hours hit
- See assignment delay trends by store and time of day
- Get alerts before rider shortages cause SLA breaches
- Identify riders with consistently high delay patterns

**What He Needs from MacroOps AI:**
- Rider availability and assignment delay dashboard
- Store-level delivery performance comparison
- Predictive alerts for upcoming rider shortages
- Individual rider performance metrics over time

---

## User Persona 4 — The Frontline Picker

**Name:** Amit Kumar
**Role:** Picker, Pune Dark Store (ST067)
**Age:** 24
**Experience:** 8 months as a picker

**A Day in Amit's Life:**
Amit receives picking tasks through his handheld scanner. He follows
the system's shelf location instructions to collect items. Sometimes
items are not where the system says they are. When this happens, he
is not sure whether to search further, report it as missing, or ask
someone. The SOP manual is a printed booklet kept at the manager's
desk — he cannot access it while he is on the warehouse floor. He
often makes decisions based on habit or by asking a more experienced
colleague.

**Goals:**
- Know the correct procedure for unusual situations instantly
- Get answers without having to find his manager
- Access SOPs while on the warehouse floor
- Reduce the time he loses when items are not where expected

**What He Needs from MacroOps AI:**
- Mobile-accessible SOP assistant he can ask in plain language
- Instant answers to "what do I do when..." questions
- Clear escalation guidance for complex situations

---

## Summary Table

| Persona | Primary Need | Key Dashboard Page | GenAI Feature |
|---------|-------------|-------------------|---------------|
| Operations Manager | Single view of all operations | Operations Overview | Copilot for data queries |
| Fulfillment Manager | Picking and inventory visibility | Exception Management | Discrepancy and picker alerts |
| Delivery Operations Manager | Rider performance monitoring | Delivery Analytics | Rider demand prediction |
| Frontline Picker | SOP access on mobile | Not applicable | RAG-based SOP Assistant |