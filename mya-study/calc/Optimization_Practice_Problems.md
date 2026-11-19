# Calculus I — Optimization (§4.7)

## Optimization

**1.** A farmer has a budget of $960 to fence in a rectangular pasture that is split into two pens by one interior fence running parallel to one pair of sides. The outer fence costs $8 per foot and the interior divider costs $4 per foot. What dimensions maximize the total enclosed area, and what is that maximum area? Include units.

**2.** An open-top box is made from a square sheet of cardboard \(12\) in on a side by cutting equal squares of side \(x\) out of each corner and folding up the flaps. What value of \(x\) gives the box the largest possible volume, and what is that volume? Include units.

Volume of a rectangular box: \(V = \ell\, w\, h\).

**3.** A closed cylindrical can must hold \(108\pi\) cm³. The material for the top and bottom costs twice as much per square centimeter as the material for the curved side. Find the radius and height that make the can as cheap as possible to build.

Volume of a cylinder: \(V = \pi r^2 h\). Area of the curved side: \(2\pi r h\). Area of each circular end: \(\pi r^2\).

**4.** Find the point on the curve \(y = \sqrt{x}\) that is closest to the point \((4, 0)\). What is the minimum distance?

**5.** A property manager owns 100 apartments. At a rent of $800 per month, every unit is rented. For each $20 increase in monthly rent, one more unit becomes vacant. Each occupied unit costs the manager $80 per month in maintenance (vacant units cost nothing). What rent maximizes monthly profit? How many units are rented at that price, and what is the maximum monthly profit?

## Answer Key

**1.**
**Step 1 — Name the variables.** Let \(x\) be the length (ft) of the two outer sides that run parallel to the divider, and \(y\) the length (ft) of the other two outer sides. The divider itself also has length \(x\).

**Step 2 — Write the constraint (the budget).** The outer fence is \(2x + 2y\) feet at $8/ft, and the divider is \(x\) feet at $4/ft:

$$8(2x + 2y) + 4x = 960 \quad\Longrightarrow\quad 20x + 16y = 960.$$

Solve for \(y\):

$$y = \frac{960 - 20x}{16} = 60 - \frac{5}{4}x.$$

**Step 3 — Write the objective in one variable.** Total area of the two pens together is

$$A(x) = xy = x\left(60 - \frac{5}{4}x\right) = 60x - \frac{5}{4}x^2.$$

**Step 4 — State the domain.** Both sides must be positive: \(x > 0\) and \(y = 60 - \tfrac54 x > 0 \Rightarrow x < 48\). So \(0 < x < 48\).

**Step 5 — Find the critical number.**

$$A'(x) = 60 - \frac{5}{2}x = 0 \quad\Longrightarrow\quad x = 24.$$

**Step 6 — Confirm it is a maximum.** \(A''(x) = -\tfrac{5}{2} < 0\) for every \(x\), so \(A\) is concave down and \(x = 24\) is a local max. It is the only critical number on the interval, so it is the absolute max. (Also \(A \to 0\) as \(x \to 0^+\) or \(x \to 48^-\).)

**Step 7 — Find the other dimension and the area.**

$$y = 60 - \frac{5}{4}(24) = 60 - 30 = 30, \qquad A = 24 \cdot 30 = 720.$$

Check the budget: \(20(24) + 16(30) = 480 + 480 = 960\). ✓

**Final answer:** the pasture should be **24 ft** (the sides parallel to the divider) by **30 ft**, enclosing a maximum of **720 ft²**.

**2.**
**Step 1 — Draw and label.** After cutting a square of side \(x\) from each corner, the base is a square of side \(12 - 2x\) (we lose \(x\) from each end), and the folded flaps make the height \(x\).

**Step 2 — Write the volume in one variable.** Using \(V = \ell w h\):

$$V(x) = (12 - 2x)(12 - 2x)(x) = x(12 - 2x)^2.$$

**Step 3 — State the domain.** We need \(x \ge 0\) and \(12 - 2x \ge 0\), so \(0 \le x \le 6\). This is a closed interval, so we can use the Closed Interval Method.

**Step 4 — Differentiate.** Expand first: \((12 - 2x)^2 = 144 - 48x + 4x^2\), so

$$V(x) = 4x^3 - 48x^2 + 144x,$$

$$V'(x) = 12x^2 - 96x + 144 = 12(x^2 - 8x + 12) = 12(x - 2)(x - 6).$$

**Step 5 — Critical numbers.** \(V'(x) = 0\) at \(x = 2\) and \(x = 6\).

**Step 6 — Closed Interval Method.** Evaluate \(V\) at the critical numbers and endpoints:

$$V(0) = 0, \qquad V(2) = 2(12 - 4)^2 = 2 \cdot 64 = 128, \qquad V(6) = 6(0)^2 = 0.$$

The largest value is at \(x = 2\).

**Final answer:** cut **\(x = 2\) in** squares; the box is \(8 \times 8 \times 2\) in with maximum volume **128 in³**.

**3.**
**Step 1 — Name the variables.** Let \(r\) be the radius (cm) and \(h\) the height (cm). Let \(k\) be the cost per cm² of the side material, so the ends cost \(2k\) per cm². (The value of \(k\) will not matter.)

**Step 2 — Write the objective (cost).** The curved side has area \(2\pi r h\) and the two ends have total area \(2\pi r^2\):

$$C = k(2\pi r h) + 2k(2\pi r^2) = k\left(2\pi r h + 4\pi r^2\right).$$

**Step 3 — Use the constraint (volume) to eliminate \(h\).**

$$\pi r^2 h = 108\pi \quad\Longrightarrow\quad h = \frac{108}{r^2}.$$

Substitute:

$$C(r) = k\left(2\pi r \cdot \frac{108}{r^2} + 4\pi r^2\right) = k\left(\frac{216\pi}{r} + 4\pi r^2\right), \qquad r > 0.$$

**Step 4 — Differentiate and find the critical number.**

$$C'(r) = k\left(-\frac{216\pi}{r^2} + 8\pi r\right) = 0 \quad\Longrightarrow\quad 8\pi r = \frac{216\pi}{r^2} \quad\Longrightarrow\quad r^3 = 27 \quad\Longrightarrow\quad r = 3.$$

**Step 5 — Confirm it is a minimum.**

$$C''(r) = k\left(\frac{432\pi}{r^3} + 8\pi\right) > 0 \text{ for all } r > 0,$$

so \(C\) is concave up and \(r = 3\) is a local min. It is the only critical number on \((0, \infty)\), so it is the absolute min.

**Step 6 — Find the height.**

$$h = \frac{108}{3^2} = \frac{108}{9} = 12.$$

Notice \(h = 4r\): because the ends are more expensive, the cheapest can is taller and narrower than the \(h = 2r\) shape that minimizes surface area alone.

**Final answer:** **\(r = 3\) cm** and **\(h = 12\) cm**.

**4.**
**Step 1 — Write the distance.** A point on the curve is \((x, \sqrt{x})\). Its distance to \((4, 0)\) is

$$D = \sqrt{(x - 4)^2 + (\sqrt{x} - 0)^2}.$$

**Step 2 — Minimize the squared distance instead.** Since \(\sqrt{\;}\) is increasing, \(D\) and \(D^2\) are smallest at the same \(x\). Let

$$S(x) = D^2 = (x - 4)^2 + x = x^2 - 8x + 16 + x = x^2 - 7x + 16, \qquad x \ge 0.$$

**Step 3 — Critical number.**

$$S'(x) = 2x - 7 = 0 \quad\Longrightarrow\quad x = \frac{7}{2}.$$

**Step 4 — Confirm it is a minimum.** \(S''(x) = 2 > 0\), so this is a minimum. Check the endpoint too: \(S(0) = 16\), while

$$S\left(\tfrac{7}{2}\right) = \frac{49}{4} - \frac{49}{2} + 16 = \frac{49 - 98 + 64}{4} = \frac{15}{4},$$

which is smaller. So \(x = \tfrac72\) gives the absolute minimum.

**Step 5 — Find the point and the distance.**

$$y = \sqrt{\tfrac{7}{2}} = \frac{\sqrt{14}}{2}, \qquad D = \sqrt{\tfrac{15}{4}} = \frac{\sqrt{15}}{2} \approx 1.94.$$

**Final answer:** the closest point is **\(\left(\tfrac{7}{2}, \tfrac{\sqrt{14}}{2}\right)\)**, at minimum distance **\(\tfrac{\sqrt{15}}{2}\)**.

**5.**
**Step 1 — Name the variable.** Let \(n\) be the number of $20 rent increases. Then

$$\text{rent} = 800 + 20n, \qquad \text{units rented} = 100 - n, \qquad 0 \le n \le 100.$$

**Step 2 — Write the profit.** Each rented unit brings in the rent minus $80 of maintenance:

$$P(n) = (\text{rent} - 80)(\text{units}) = (720 + 20n)(100 - n).$$

Expand:

$$P(n) = 72000 - 720n + 2000n - 20n^2 = 72000 + 1280n - 20n^2.$$

**Step 3 — Critical number.**

$$P'(n) = 1280 - 40n = 0 \quad\Longrightarrow\quad n = 32.$$

**Step 4 — Confirm it is a maximum.** \(P''(n) = -40 < 0\), so \(n = 32\) is a maximum. Endpoints check: \(P(0) = 72{,}000\) and \(P(100) = 0\), both smaller than \(P(32)\) below.

**Step 5 — Compute rent, units, and profit.**

$$\text{rent} = 800 + 20(32) = 1440, \qquad \text{units} = 100 - 32 = 68,$$

$$P(32) = (1440 - 80)(68) = 1360 \cdot 68 = 95{,}200 - 2{,}720 = 92{,}480.$$

**Final answer:** charge **$1,440 per month**; **68 units** are rented, for a maximum profit of **$92,480 per month**.
