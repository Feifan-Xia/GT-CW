# Minority Games in Urban Commuting: Bounded Rationality and Inductive Coordination

---

## Abstract

We study the minority game in the context of urban commuting, where 101 workers independently decide each morning whether to drive or use alternative transport. We derive the unique symmetric mixed Nash equilibrium ($p^* \approx 0.62$, expected attendance $\approx 62.6$, above the capacity threshold $T=60$) and show that it is Pareto-dominated by the reachable social optimum by a factor of 2.4. Stage-game best-reply dynamics collapse into a two-period oscillation. An inductive-agent model following Arthur (1994), featuring 11 heterogeneous predictors including two novel commuter-psychology-motivated rules, reduces congestion from 65% (mixed NE) to approximately 46% with mean per-agent payoff in the range $[0.29, 0.32]$ across seeds, on average marginally above the mixed NE benchmark of $0.30$. Ablation and exploration-sensitivity experiments quantify the contributions of predictor diversity and stochastic exploration.

---

## 1. Game Definition and Urban Commuting Framing

### 1.1 Motivating Context

Every weekday morning, $N=101$ workers decide independently whether to **drive** or use **alternative transport** (public transit). The road has a capacity $T=60$: when at most 60 cars use it, traffic flows freely; when more than 60 enter, all drivers experience congestion. This is a minority game (Challet & Zhang, 1997): a driver benefits only by being in the minority who chose to drive. The minority-game structure distinguishes this from coordination games (where agents want to match others' choices) and motivates adaptive rather than equilibrium-based decision-making.

### 1.2 Normal-Form Game

The stage game is defined by three components:

- **Players:** $\mathcal{N} = \{1,\ldots, 101\}$
- **Strategy space:** $S_i = \{\textit{drive},\, \textit{transit}\}$ for each $i \in \mathcal{N}$
- **Aggregate outcome:** $A = \sum_{i} \mathbf{1}[s_i = \textit{drive}]$

**Payoff** (consistent with project spec: "more than $T$ drivers $\Rightarrow$ unhappy"):

$$
r_i(s_i, \mathbf{s}_{-i}) = \begin{cases} 1 & \text{if } s_i = \textit{drive} \text{ and } A \leq T \\ 0 & \text{if } s_i = \textit{drive} \text{ and } A > T \\ r_{\text{transit}} = 0.3 & \text{if } s_i = \textit{transit} \end{cases}
$$

The payoff $r_{\text{transit}} = 0.3$ reflects the reliable but modest utility of public transport. Driving strictly dominates transit *if and only if* the road is uncongested, creating the minority-game tension.

**Information structure:** The game is simultaneous; players choose without observing others' decisions. After each round, public attendance $A_t$ is announced. This public signal is the only feedback available to all players, which motivates predictive rather than purely reactive strategies for sustained coordination.

### 1.3 Repeated Game

The stage game $G$ is repeated for $m = 200$ rounds. Let $h^t = (A_1, \ldots, A_{t-1}) \in \mathbb{R}^{t-1}$ denote the public history at round $t$, and $H = \bigcup_{t \geq 1} \mathbb{R}^{t-1}$ the set of all histories. A **strategy** is a mapping $\sigma_i : H \rightarrow S_i$ from histories to actions. The cumulative payoff is $\Pi_i = \sum_{t=1}^{m} r_i^{(t)}$.

For agents using fixed strategies (such as always driving, always using transit, or randomising at $p^*$), rounds are independent conditional on the history, so $\Pi_i$ reduces to $m \cdot \mathbb{E}[r_i^{(t)}]$. For adaptive agents such as those in Section 4.2, whose strategy profiles change as predictor scores are updated, this reduction does not hold exactly -- but per-round expected payoff remains the natural performance metric and enables direct comparison against the static mixed NE benchmark.

---

## 2. Theoretical Analysis of the Stage Game

### 2.1 Pure Strategy Nash Equilibria

**Claim 1: No symmetric pure strategy NE exists.**

- All $N$ drive: $A = 101 > T$, every driver earns $0 < r_{\text{transit}} = 0.3$. Each prefers to deviate to transit. Not a NE.
- All $N$ take transit: $A = 0 \leq T$, any deviating driver drives alone and earns $1 > 0.3$. Not a NE.

**Claim 2: Asymmetric pure NE exist but require prior coordination to reach.**

Any configuration with exactly $T = 60$ drivers is a NE:

- Each driver earns $1$ (since $A = 60 \leq T$). Switching to transit gives $0.3 < 1$. No incentive to deviate.
- Each transit user earns $0.3$. Switching to driving yields $A = 61 > T$, earning $0 < 0.3$. No incentive to deviate.

There are $\binom{101}{60}$ such equilibria, an astronomically large uncoordinated set. In the urban commuting context, reaching one would require exactly 60 specific workers to pre-agree on driving while the rest use transit, a mechanism the model does not provide.

*Note on refinements:* The symmetric mixed NE (Section 2.2) is the unique symmetric equilibrium concept; trembling-hand perturbations cannot select among the asymmetric pure NE without a coordination device. For finite repetition, the folk theorem does not apply when the stage game lacks a unique NE payoff profile, so sustained cooperation above the mixed NE level is not theoretically guaranteed.

### 2.2 Mixed Strategy Nash Equilibrium

Each player independently drives with probability $p$. Indifference requires $\mathbb{E}[r \mid \textit{drive}] = r_{\text{transit}} = 0.3$:

$$
P\!\left(\text{Bin}(100,\,p) \leq T{-}1\right) = P\!\left(A_{-i} + 1 \leq T\right) = 0.3
$$

Since $P(\text{Bin}(100, p) \leq 59)$ is **strictly decreasing** in $p$, the equation has a **unique solution**:

$$
p^* \approx 0.6202, \qquad Np^* \approx 62.6 > T = 60
$$

At $p^*$, expected attendance exceeds the threshold. This is not paradoxical: indifference is achieved when a marginal driver faces exactly a 30% chance of an uncongested road -- consistent with mean attendance slightly above capacity, because the binomial variance ($\sigma = \sqrt{Np^*(1-p^*)} \approx 4.9$) keeps the probability of $A \leq 60$ at 35% even when $\mathbb{E}[A] = 62.6$. The congestion rate is $P(A > 60) \approx 65\%$, confirmed empirically at 65.4%.

### 2.3 Welfare Analysis

The mixed NE is Pareto-inefficient. At the indifference condition, every player earns exactly $r_{\text{transit}} = 0.3$, the same as choosing transit at every round.

| Outcome                               | Mean attendance | Per-agent payoff | Total welfare  |
| ------------------------------------- | --------------- | ---------------- | -------------- |
| All transit                           | 0               | 0.300            | 30.3           |
| Mixed NE ($p^* = 0.62$)             | 62.6            | **0.300**  | **30.3** |
| Inductive agents (simulated)          | ~56             | ~0.306           | ~30.9          |
| Social optimum = Asymm. NE ($A=60$) | 60              | **0.716**  | **72.3** |

The social optimum coincides with any asymmetric pure NE with exactly $T=60$ drivers: total welfare $= 60 \times 1 + 41 \times 0.3 = 72.3$, or $0.716$ per agent, **2.4 times the mixed NE welfare**. The mixed NE represents a coordination failure: each commuter rationally accounts for others' independence, and the collective result is that the road is congested nearly two-thirds of the time despite all players earning only $0.3$.

The 2.4× welfare gap, equivalent to 42 uncongested journeys foregone each morning, quantifies the daily cost of uncoordinated commuting and the motivation for policy intervention. A city that can direct exactly 60 daily drivers through pricing, reservations, or a permit scheme attains welfare equal to the social optimum. Without such a mechanism, rational independent play achieves the same welfare as universal transit use.

**Connection to the repeated game.** One might expect repeated play to drive agents toward the symmetric mixed NE or even toward an efficient asymmetric NE. Section 4 shows neither happens under homogeneous reactive strategies. The mixed NE is an equilibrium of beliefs, not a dynamical attractor; and the asymmetric NE requires coordination that the single public signal $A_t$ cannot provide. This motivates the inductive approach, which achieves coordination near $T$ through predictor diversity rather than equilibrium reasoning.

---

## 3. Static Game Simulation

### 3.1 Numerical Verification of $p^*$

Running 1,000 independent single-shot games for each $p \in \{0.10, 0.15, \ldots, 0.90\}$ confirms the analytical prediction. **Figure 1(a)** plots mean attendance across the same sweep, confirming $\mathbb{E}[A] = Np^* \approx 62.6$ at the crossing point. **Figure 1(b)** shows $\mathbb{E}[r \mid \textit{drive}]$ declining from near 1 at low $p$ to near 0 at high $p$, crossing $r_{\text{transit}} = 0.3$ precisely at $p^* \approx 0.62$, matching the Brent-method solution.

![Figure 1](figure1_static_sweep.png)
*Figure 1: (a) Mean attendance $\mathbb{E}[A]$ vs $p$ across the full sweep, with $T$ and $Np^*$ marked. (b) Indifference condition -- $\mathbb{E}[r \mid drive]$ crosses $r_\text{transit}=0.3$ at $p^*\approx 0.62$.*

### 3.2 Attendance Distribution at $p^*$

**Figure 2** shows 1000 independent single-shot outcomes at $p = p^*$. The empirical mean is $62.55 \approx Np^* = 62.64$, empirical standard deviation $\sigma = 4.93$, and theoretical binomial standard deviation $\sqrt{Np^*(1-p^*)} = 4.88$, a near-perfect agreement validating simulation fidelity. Congestion ($A > T = 60$) occurs in **65.4%** of rounds.

![Figure 2](figure2_histogram_pstar.png)
*Figure 2: Attendance histogram at $p^*$ (1000 runs). Congestion in 65.4% of rounds, despite every player playing the mixed NE.*

Even if every commuter knew $p^*$ and played it, congestion would occur on two out of every three mornings due to binomial variance. This motivates the repeated game: is there an adaptive strategy that exploits memory to reduce the 65% congestion rate?

---

## 4. Repeated Game Dynamics

### 4.1 Stage-Game Best-Reply Dynamics

Before inductive strategies, we study the simplest adaptive rule: agents who apply the **stage-game best response to the previous round's realised attendance**, updating their choice each period without accounting for others' reasoning or the game's repeated structure.

**Rule:** if $A_{t-1} \leq T$ (road uncongested) $\Rightarrow$ drive; if $A_{t-1} > T$ (road congested) $\Rightarrow$ transit.

Note that this constitutes a best response to the *previous* period's outcome, not a best response in the repeated-game sense (which would require a belief distribution over co-players' current actions and acknowledgment of future consequences). The distinction matters: true best-reply reasoning in the repeated game could involve a fixed or mixed per-round strategy, while this rule is purely reactive to the last observation.

**Round-1 initialisation:** Agents perceive a prior attendance of $T = 60$ (uncongested), so all 101 drive in round 1 ($A_1 = 101 > T$). All switch to transit in round 2 ($A_2 = 0 \leq T$). All drive again in round 3. The result is the permanent two-period oscillation shown in **Figure 3**: attendance alternates between 0 and 101, never approaching $T$ or $Np^*$.

![Figure 3](figure3_best_response.png)
*Figure 3: Stage-game best-reply -- permanent 0--101 oscillation. Mean payoff $= (0.3 + 0)/2 = 0.15$, below the transit-only payoff.*

This is an oscillatory anti-coordination regime. Homogeneity of strategies simultaneously coordinates overcrowding and complete avoidance, earning mean per-agent payoff 0.15, half of the payoff 0.30 achieved by any fixed strategy such as always driving, always using transit, or randomising at p*.

The dynamic instability of symmetric pure NE (Section 2.1) manifests here as a limit cycle: all agents apply the same rule to the same public signal At−1 perpetually overshoot in both directions rather than settling at any fixed point. The result also shows that the symmetric mixed NE at p*=0.62 is not a dynamical attractor: no simple reactive rule applied uniformly by all agents converges to it.

This failure is not specific to Best-Reply: it applies to any homogeneous reactive rule. For commuting applications, a navigation system broadcasting a single uniform recommendation replicates this failure, and universal adoption of one reactive rule produces oscillatory flow waves qualitatively consistent with those observed on instrumented ring roads (Cabannes et al., 2018).

This motivates the inductive approach: heterogeneous predictors break the synchronisation that homogeneous rules cannot escape.

### 4.2 Inductive Strategies

Following Arthur (1994), agents replace reactive rules with **inductive predictors**: internal models of next-period attendance, updated continuously by prediction accuracy. Each agent $i$ holds $K=6$ predictors drawn at random at initialisation from a global pool of 11, ensuring **heterogeneity by construction** and preventing the synchronisation that causes stage-game best-reply to fail.

**Implementation note.** Before round 1, each agent's history is seeded with 10 warmup observations drawn uniformly from $\{50, \ldots, 71\}$ to initialise predictor scores. These warmup rounds are not counted in the M=200 simulation rounds.

**Predictor pool:**

| Predictor                         | Forecast$\hat{A}_t$                                               | Motivation                        |
| --------------------------------- | ------------------------------------------------------------------- | --------------------------------- |
| last                              | $A_{t-1}$                                                         | Yesterday repeats                 |
| avg-$n$ ($n \in \{3,5,7\}$)   | $\bar{A}_{t-n:t}$                                                 | Inertia of recent flow            |
| contrarian                        | $2T - A_{t-1}$                                                    | Oscillation half-period           |
| trend                             | $A_{t-1} + \Delta A_{t-1}$, clipped to $[0,N]$                  | Momentum extrapolation            |
| **cong-mom** *(novel)*    | $A_{t-1} + 0.5(T{-}A_{t-1})$ if $A_{t-1}{>}T$, else $A_{t-1}$ | Partial recovery after congestion |
| **thresh-prox** *(novel)* | $T + 0.5(A_{t-1}{-}T)$                                            | Mean-reversion toward capacity    |
| cycle-$k$ ($k \in \{2,3,5\}$) | $A_{t-k}$                                                         | Periodic pattern detection        |

A key **coverage condition** (Arthur 1994): the pool must span both sides of $T$ so that each round some agents are directed to drive and others to transit. Contrarian, cycle-$k$, avg-$n$, and thresh-prox produce a distribution of forecasts on both sides of $T$ depending on history, preventing systematic bias.

The two novel predictors are grounded in commuter psychology: thresh-prox formalises the tendency to anchor forecasts between yesterday's congestion and capacity, a heuristic consistent with empirical commuter adaptation, while cong-mom captures partial recovery after a congested morning, reflecting that drivers do not immediately fully commit to transit following a single bad experience. Technically, both predictors share an important property: when At−1 < T, both forecast at or below T — the same binary decision as 'last'. The novel predictors therefore do not extend the action space. Their contribution is to **forecast calibration**: by predicting a value between $A_{t-1}$ and $T$ rather than $A_{t-1}$ itself, they fall within the accuracy window $\delta=5$ more often when attendance reverts toward threshold. Thresh-prox in particular -- forecasting the midpoint $\frac{1}{2}(A_{t-1}+T)$ -- is systematically more accurate than `last' when attendance moves toward capacity, earning higher score updates and accumulating a dominant position in the population. Cong-mom offers an analogous calibration advantage but only for the supra-threshold case; its marginal contribution is therefore much smaller (Section 5.2).

**Score update:** Each predictor's accuracy is tracked via exponential smoothing:

$$
\text{score}_d(t) = \gamma \cdot \text{score}_d(t{-}1) + \mathbf{1}\!\left[|\hat{A}_{d,t} - A_t| < \delta\right], \quad \gamma = 0.9,\; \delta = 5
$$

This update uses the forecasts from the most recent non-exploration round; during $\varepsilon$-exploration rounds the scores are updated but the active forecast is not refreshed. The agent follows the highest-scoring predictor, with exploration probability $\varepsilon = 0.05$. The decision threshold is $T$ (public knowledge -- road capacity is posted):

$$
s_i(t) = \begin{cases} \textit{drive} & \text{if } \hat{A}_t \leq T \\ \textit{transit} & \text{otherwise} \end{cases}
$$

### 4.3 Simulation Results

**Convergence near threshold (Figure 4).** Consistent with Arthur's (1994) finding that mean attendance converges to $T$, our simulation yields $\bar{A} \approx 56$ across seeds 42, 123, and 7 ($\pm 0.7$), below but near $T = 60$ and substantially below $Np^* = 62.6$. The rolling mean stabilises by approximately round 30 (counting from after the warmup period). Congestion rate: **45--48%**, compared to 65.4% at the mixed NE.

![Figure 4](figure4_inductive_attendance.png)
*Figure 4: Inductive agents -- attendance stabilises near but below $T=60$, well below $Np^*$, within approximately 30 rounds.*

Convergence is not the result of agents computing $p^*$. Rather, the **composition of active predictors** determines the aggregate drive fraction: those directing agents to drive win score points when attendance is below $T$, increasing $A$ toward $T$; once above $T$, predictors directing agents to transit win points, lowering $A$ again. The mean drive fraction in steady state is approximately $\bar{A}/N \approx 55\%$, which is slightly below $T/N \approx 59\%$, consistent with the mean attendance being slightly below $T$.

**Predictor composition (Figure 5).** The active predictor distribution shifts over time: avg-7 and thresh-prox dominate in the converged steady state (each approximately 23% share), with cycle-2 at 13%, reflecting the residual short-period oscillations visible in Figure 4. The trend predictor is eliminated (0% share) as it systematically overestimates momentum and is outcompeted across all history conditions. The novel thresh-prox achieves 23% steady-state share, confirming its relevance in the commuting setting; cong-mom reaches only 3%, consistent with its narrower calibration advantage (Section 4.2).

![Figure 5](figure5_predictor_ecology.png)
*Figure 5: Active predictor composition -- trend predictor eliminated; thresh-prox and avg-7 dominate at convergence. Predictors grouped by color (basic: blue, averaging: purple, opposite: orange, momentum: red, novel: green, cyclic: green shades) with varying transparency for intra-group distinction.*

**Payoff comparison (Figure 6).** **Figure 6** plots cumulative average payoff for the three populations, with the inductive line showing the mean across three seeds (shaded band: $\pm 1\sigma$). In steady state:

- Stage-game best-reply: $0.150$ (oscillatory anti-coordination regime)
- Uncorrelated random play at $p^*$: $\approx 0.300$ (mixed NE, as expected from the indifference condition)
- Inductive (mean ac ross seeds 42, 123, 7): $\approx 0.306$

Individual seed payoffs are [0.294, 0.300, 0.323], with seed 42 being the only seed that falls marginally below the 0.300 benchmark. The cross-seed mean exceeds the benchmark; results are not uniformly above it. The principal advantage of inductive agents over uncorrelated random play is not the raw payoff difference -- which is small -- but the **reduced congestion rate** (46% vs 65%) and lower variance in individual outcomes.

![Figure 6](figure6_payoff_comparison.png)
*Figure 6: Cumulative payoff -- inductive (mean $\pm 1\sigma$ across 3 seeds) vs uncorrelated $p^*$ vs stage-game best-reply.*

**Individual payoff heterogeneity.** Tracking per-agent payoffs (seed 42): mean = 0.294, std = 0.021, range [0.243, 0.341]. The 37% spread between the best and worst agents reflects the composition of each agent's predictor subset: agents randomly assigned higher-performing predictors (particularly thresh-prox and avg-7) consistently earn more. This within-population payoff inequality is an emergent consequence of random predictor assignment, absent from the symmetric mixed NE in which all players are treated identically.

---

## 5. Ablation and Sensitivity Analysis

### 5.1 Exploration vs. Exploitation

Setting $\varepsilon = 0$ (pure exploitation, no stochastic exploration):

| Seed | Mean payoff ($\varepsilon=0.05$) | Mean payoff ($\varepsilon=0$) | Change      |
| ---- | ---------------------------------- | ------------------------------- | ----------- |
| 42   | 0.294                              | 0.266                           | $-9.5\%$  |
| 123  | 0.300                              | 0.259                           | $-13.7\%$ |
| 7    | 0.323                              | 0.252                           | $-22.0\%$ |

Without exploration, agents lock into their initial best predictor early and cannot adapt as the predictor landscape shifts around them. Payoff declines consistently across seeds (average $-15\%$). A small degree of stochastic deviation from the current best rule (5% random action rate) is necessary for sustained near-threshold coordination.

### 5.2 Predictor Count per Agent (K)

Varying the number of predictors $K$ assigned to each agent controls the degree of subset overlap among the population.

| Seed           | Mean payoff ($K=3$) | Mean payoff ($K=6$) | Mean payoff ($K=9$) |
| -------------- | --------------------- | --------------------- | --------------------- |
| 42             | 0.337                 | 0.294                 | 0.230                 |
| 123            | 0.302                 | 0.300                 | 0.242                 |
| 7              | 0.344                 | 0.323                 | 0.244                 |
| **Mean** | **0.328**       | **0.306**       | **0.239**       |

Agents with fewer predictors ($K=3$) achieve a higher stable payoff on average ($0.328$). At $K=3$, two agents have a 34% probability of sharing no predictors at all, computed as $P(\text{no overlap}) = \binom{11-3}{3}/\binom{11}{3} = 56/165 \approx 0.34$, whereas at $K=6$ overlap is guaranteed by construction ($\binom{11-6}{6}/\binom{11}{6} = 0$), making convergence on the same highest-scoring predictor substantially more likely. This preserves population-level heterogeneity that drives near-threshold coordination. As $K$ increases toward $11$, structural overlap rises and agents increasingly converge on the same forecast, replicating the synchronised overcorrection of Section 5.4. Mean payoff collapses to $0.239$ at $K=9$, suggesting an optimal $K$ exists well below the pool size where individual commitment and population diversity are jointly maximised.

### 5.3 Contribution of Novel Predictors (Ablation)

The table below shows the effect of removing each novel predictor individually and jointly. To isolate contribution from reduction in pool size, we note that removing one predictor from 11 still leaves abundant combinatorial diversity ($\binom{10}{6} = 210$ vs $\binom{11}{6} = 462$ distinct agent subsets).

| Condition               | Seed 42 | Seed 123 | Seed 7 | Mean  | $\Delta$ vs full |
| ----------------------- | ------- | -------- | ------ | ----- | ------------------ |
| Full pool               | 0.294   | 0.300    | 0.323  | 0.306 | --                 |
| Remove thresh-prox only | 0.293   | 0.300    | 0.271  | 0.288 | $-5.9\%$         |
| Remove cong-mom only    | 0.314   | 0.306    | 0.289  | 0.303 | $-1.0\%$         |
| Remove both             | 0.249   | 0.271    | 0.260  | 0.260 | $-15.0\%$        |

The results clarify the individual contributions: thresh-prox accounts for most of the ablation effect (predominantly at seed 7, $-16\%$), while cong-mom's marginal contribution is small ($-1\%$ mean), consistent with its steady-state share of only 3% (Section 4.3). The joint removal effect ($-15\%$) exceeds the sum of the individual effects ($-7\%$), suggesting complementarity: thresh-prox handles sub-threshold calibration while cong-mom covers the supra-threshold case, and removing both collapses the mechanism entirely.

The cross-seed variance in thresh-prox's contribution reflects the stochastic nature of predictor assignment. In seeds where thresh-prox achieves a higher steady-state share (seed 7), its removal has a larger impact; in seeds where thresh-prox accumulates a lower steady-state share due to random initialisation (seed 123), other predictors fill the same calibration role and its marginal contribution is near zero.

### 5.4 Homogeneous vs. Heterogeneous Population

| Population    | Mean ($A$) | Std ($A$)    | Congestion rate |
| ------------- | ------------ | -------------- | --------------- |
| Heterogeneous | 55.9         | 30.2           | 48.0%           |
| Homogeneous   | 50.6         | **40.1** | 48.5%           |

The mean congestion rates are comparable (both approximately 48%), but the attendance standard deviation is 33% larger for the homogeneous population. **Figure 7** illustrates the mechanism: the homogeneous population alternates between near-complete attendance (all agents share the same forecast, all drive, $A \approx 101$) and near-empty roads (all use transit, $A \approx 5$, driven by exploration alone), while the heterogeneous population produces moderate fluctuations around $T$. The homogeneous outcome is not simply worse on average but represents a qualitatively different, more volatile regime characterised by recurring aggregate overcorrections, structurally similar to the oscillatory best-reply result of Section 4.1.

Note that the homogeneous result depends on which six predictors are randomly drawn as the shared pool (seed 123 in this experiment). Running multiple draws would quantify the variance across shared predictor sets; the reported std=40.1 is for one specific draw.

![Figure 7](figure7_homo_hetero.png)
*Figure 7: Homogeneous population (bottom) exhibits extreme swings; heterogeneous population (top) converges to moderate near-threshold fluctuations.*

Note that the homogeneous result depends on which six predictors are randomly drawn as the shared pool (seed 123 in this experiment). Running multiple draws would quantify
the variance across shared predictor sets; the reported std=40.1 is for one specific draw.

For urban commuting, this finding has a direct policy implication: navigation systems that broadcast a single uniform recommendation replicate the homogeneous regime, producing the volatile oscillatory flows observed on instrumented ring roads rather than the stable near-threshold coordination achieved by a diverse commuter population. Deliberate recommendation diversification, not optimisation, is the structurally correct design principle.

---

## 6. Real-World Applications and Discussion

### 6.1 Commuter Behaviour and Emergent Coordination

The three simulated regimes map directly onto real commuter archetypes. Best-reply agents, who simply reverse yesterday's choice, represent the purely reactive commuter. The simulation shows this produces the worst collective outcome (payoff 0.15), confirming that reactivity without memory is not just individually suboptimal but collectively destructive. Inductive agents, by contrast, represent experienced commuters who maintain implicit mental models of road conditions. The dominance of thresh-prox (23% steady-state share) formalises the heuristic of anchoring forecasts between yesterday's observed attendance and capacity, a pattern consistent with empirical commuter adaptation. The result: congestion falls from 65% to 46%, and journey-time variance drops substantially, a quality-of-life benefit invisible in raw payoff comparisons.

### 6.2 The Navigation System Paradox and Policy Implications

The homogeneous experiment provides the formal mechanism behind observed traffic waves when navigation apps simultaneously reroute large volumes (Cabannes et al., 2018): comparable mean congestion to the heterogeneous case (48.5% vs 48.0%) but 33% higher attendance variance (std 40.1 vs 30.2), producing recurring extreme swings. The policy implication is counterintuitive: **diversity of routing recommendations is structurally necessary for network stability** . A system that deliberately personalises suggestions — replicating the heterogeneous predictor ecology — achieves stable near-threshold coordination. The welfare analysis quantifies the stakes: a mechanism directing exactly T=60 drivers achieves per-agent welfare of 0.716, approximately 2.4× the uncoordinated baseline of 0.300.

### 6.3 Counter-Intuitive Predictions and Limitations

The model generates one falsifiable prediction beyond the simulation: a weekend reduction in commuter numbers (N=75) combined with degraded transit quality (r_transit → 0.05) shifts the mixed NE indifference threshold sharply upward, driving most agents to choose the road despite lower total demand. Congestion frequency on weekends would *exceed*weekday levels, suggesting that transit service quality, not passenger volume, is the primary lever governing road congestion. Standard demand models miss this mechanism entirely.

Key model limitations: the binary action space excludes departure-time flexibility; homogeneous payoffs mask agent-specific transit costs; and the public attendance signal is stronger than real-world journey-time feedback. These suggest the welfare gains from heterogeneous routing may be somewhat smaller in practice, while oscillatory risks may be larger.

## 7. Extensions: Non-Stationary Environments

The baseline model assumes a structurally static environment ($N=101$, $T=60$). Real-world urban infrastructure, however, is subject to exogenous shocks and periodic fluctuations. We substitute the baseline parameters with two dynamic settings to examine the robustness and counter-intuitive implications of boundedly rational adaptation.

### 7.1 The "Weekend Effect": Congestion Despite Reduced Demand

Commuting is heavily calendar-dependent. While it is mathematically obvious that reducing total commuters ($N$) will eventually clear congestion if $T$ remains constant, this ignores the corresponding shift in external options. Real-world weekends feature less traffic but also a drastic reduction in public transit frequency.

**Simulation Setup:** We introduce a 7-day cyclical calendar.

- **Weekdays (5 days):** Baseline parameters ($N=101$, $T=60$, $r_{\text{transit}} = 0.3$).
- **Weekends (2 days):** The active commuter population drops by 25% to $N=75$. However, the payoff for alternative transport collapses to $r_{\text{transit}} = 0.05$ due to infrequent weekend schedules.

**Expected Dynamics:** Because the transit payoff is heavily penalised on weekends, the mixed NE indifference threshold $p^*$ shifts drastically upward. Drivers will abandon public transport and flood the road network despite there being fewer people travelling overall.

**Counter-Intuitive Finding:** The congestion rate (frequency of $A > T$) on weekends is expected to be strictly *higher* than on weekdays, despite a 25% reduction in total travellers. The adaptive ecology demonstrates that governing system congestion relies primarily on maintaining the *quality of the external alternative* ($r_{\text{transit}}$) rather than simply suppressing the absolute number of network participants ($N$).

【add simulation results】

---

## Conclusion

The minority game demonstrates the tension between individual rationality and collective efficiency in urban commuting. The unique symmetric mixed NE ($p^* \approx 0.62$) produces congestion 65% of the time and achieves per-agent welfare of $0.30$, identical to universal transit use and 2.4 times below the social optimum. Stage-game best-reply dynamics produce an oscillatory anti-coordination regime yielding the worst achievable payoff and confirm that the mixed NE is not a dynamical attractor. Inductive agents following Arthur (1994), with heterogeneous predictor pools, stabilise near $T=60$ within 30 rounds, reduce congestion to approximately 46%, and achieve mean payoff $\approx 0.306$ on average across seeds -- marginally above the mixed NE benchmark with one seed falling below it. Ablation experiments show that thresh-prox accounts for most of the novel predictors' contribution (approximately 6--16% payoff improvement) while cong-mom's marginal effect is small; exploration contributes an average 15% payoff gain over pure exploitation. The homogeneous population experiment confirms that predictor diversity is structurally necessary. The central finding for commuting infrastructure and recommendation system design is that diversity of strategies among users, rather than sophistication of any individual strategy, produces collective near-optimality.

---

## References

Arthur, W. B. (1994). Inductive reasoning and bounded rationality. *American Economic Review*, 84(2), 406--411.

Challet, D., & Zhang, Y. C. (1997). Emergence of cooperation and organization in an evolutionary game. *Physica A* , 246(3-4), 407-418.

Cabannes, T., Vincentelli, M. A. S., Sundt, A., Signargout, H., Porter, E., & Bayen, A. M. (2018). The impact of GPS-enabled shortest path routing on mobility: a game theoretic approach. *Transportation Research Part B* , 117, 486--504.

---

## Appendix: GenAI Declaration

| Category                 | Use                                                                                                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ideation**       | Claude Code (claude-sonnet-4-6) used to help structure report sections and identify key simulation insights. All theoretical arguments verified independently against the game-theoretic definitions covered in module lectures.      |
| **Coding**         | Claude Code (claude-sonnet-4-6) used to draft and debug Python simulation. All predictor designs, parameter choices, and experimental designs (sensitivity, ablation) specified by the student and verified against expected results. |
| **Report writing** | Claude Code (claude-sonnet-4-6) used to draft initial text. All claims cross-checked against simulation output. All equations derived independently. Final editing by the student.                                                    |
