1. Sudden UE Surge (e.g., concert, stadium, emergency)
Description: A large number of UEs connect rapidly.

Simulation: Spawn 10+ UEs within 10–20 seconds.

Metrics impacted: fivegs_amffunction_rm_registeredsubnbr, CPU, memory, session requests.

2. Gradual UE Growth and Saturation
Description: Gradual increase in UEs over 5–10 minutes simulating office hour ramp-up.

Simulation: Increase UEs slowly using CSV-based scheduler.

Metrics: Traffic in/out, session durations, bandwidth, system load.

3. UE Handover Simulation (simulated via UE disconnect/reconnect)
Description: Simulate movement of UEs between gNBs (conceptually, we "fake" this by stopping/starting different UEs).

Simulation: Alternate UEs in groups of 2–3.

Metrics: Session teardown/setup, CPU spike, paging events if available.

4. Burst Traffic from Few UEs
Description: Few UEs generate a large amount of traffic (e.g., video streaming).

Simulation: Generate TCP/UDP traffic from 2 UEs using iperf or curl.

Metrics: Network In/Out, congestion indicators.

5. Network Idle State
Description: Period with no active UEs.

Simulation: No containers running for ~5 minutes.

Metrics: Low CPU, bandwidth, baseline metrics.

6. Network Recovery (after outage or reset)
Description: Simulate total network drop, then restart UEs.

Simulation: Kill all UE containers, wait, then restart them all.

Metrics: Spike in registrations, PDU sessions, auth, paging.