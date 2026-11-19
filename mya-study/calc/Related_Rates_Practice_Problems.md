# Calculus I — Related Rates (§3.9)

## Related Rates

**1.** Water is pumped into an inverted conical tank (vertex pointing down) at a rate of \(2\) ft³/min. The tank is \(12\) ft tall and the radius of its top rim is \(4\) ft. How fast is the water level rising when the water is \(6\) ft deep? How fast is the radius of the water's surface growing at that moment? Include units.

Volume of a cone: \(V = \tfrac{1}{3}\pi r^2 h\).

**2.** Car A drives south toward an intersection at \(60\) mi/h, and car B drives east away from the same intersection at \(30\) mi/h. At the moment car A is \(0.3\) mi north of the intersection and car B is \(0.4\) mi east of it, how fast is the distance between the cars changing? Is the distance increasing or decreasing?

**3.** Air leaks out of a spherical balloon at a rate of \(72\pi\) cm³/s. (a) How fast is the radius decreasing when \(r = 6\) cm? (b) How fast is the surface area changing at that same instant? Include units.

Volume of a sphere: \(V = \tfrac{4}{3}\pi r^3\). Surface area of a sphere: \(S = 4\pi r^2\).

**4.** A hot-air balloon rises straight up from a level field. An observer stands \(500\) ft from the launch point. At the moment the angle of elevation from the observer to the balloon is \(\tfrac{\pi}{4}\), that angle is increasing at \(0.14\) rad/min. How fast is the balloon rising at that moment?

**5.** A water trough is \(10\) ft long. Its ends are isosceles triangles, vertex down, that are \(3\) ft across the top and \(1\) ft tall. Water flows in at \(12\) ft³/min. How fast is the water level rising when the water is \(6\) inches deep? Include units.

Volume of a prism (trough): \(V = (\text{area of cross-section})(\text{length}) = \tfrac{1}{2}\, b\, h \cdot L\), where \(b\) is the width of the water's surface and \(h\) is the water's depth.

**6.** A spotlight on the ground shines on a wall \(12\) m away. A man \(2\) m tall walks from the spotlight straight toward the wall at \(1.6\) m/s. How fast is the length of his shadow on the wall changing when he is \(4\) m from the wall? Is the shadow getting longer or shorter? Include units.

## Answer Key

**1.**
**Step 1 — Draw and name the variables.** At time \(t\), let \(h\) be the water depth, \(r\) the radius of the water's surface, and \(V\) the volume of water (ft and ft³).

**Step 2 — List what is given and what is wanted.**

$$\frac{dV}{dt} = 2 \text{ ft}^3/\text{min}, \qquad \text{find } \frac{dh}{dt} \text{ and } \frac{dr}{dt} \text{ when } h = 6.$$

**Step 3 — Relate \(r\) and \(h\) with similar triangles.** The water forms a smaller cone similar to the tank, so

$$\frac{r}{h} = \frac{4}{12} = \frac{1}{3} \quad\Longrightarrow\quad r = \frac{h}{3}.$$

**Step 4 — Write \(V\) in terms of \(h\) only.** We don't know \(\tfrac{dr}{dt}\) yet, so eliminate \(r\) before differentiating:

$$V = \frac{1}{3}\pi\left(\frac{h}{3}\right)^2 h = \frac{\pi h^3}{27}.$$

**Step 5 — Differentiate with respect to \(t\)** (chain rule on \(h^3\)):

$$\frac{dV}{dt} = \frac{3\pi h^2}{27}\,\frac{dh}{dt} = \frac{\pi h^2}{9}\,\frac{dh}{dt}.$$

**Step 6 — Plug in the instant and solve.** With \(\tfrac{dV}{dt} = 2\) and \(h = 6\):

$$2 = \frac{\pi (36)}{9}\,\frac{dh}{dt} = 4\pi\,\frac{dh}{dt} \quad\Longrightarrow\quad \frac{dh}{dt} = \frac{1}{2\pi} \approx 0.159 \text{ ft/min}.$$

**Step 7 — Rate for the radius.** Differentiate \(r = \tfrac{h}{3}\):

$$\frac{dr}{dt} = \frac{1}{3}\,\frac{dh}{dt} = \frac{1}{6\pi} \approx 0.053 \text{ ft/min}.$$

**Final answer:** the water level rises at **\(\tfrac{1}{2\pi} \approx 0.159\) ft/min**, and the surface radius grows at **\(\tfrac{1}{6\pi} \approx 0.053\) ft/min**.

**2.**
**Step 1 — Draw and name the variables.** Put the intersection at the origin. Let \(y\) be car A's distance north of the intersection, \(x\) car B's distance east of it, and \(z\) the distance between the cars (all in miles).

**Step 2 — Given and wanted.** Car A is moving *toward* the intersection, so \(y\) is shrinking; car B is moving away, so \(x\) is growing:

$$y = 0.3,\quad \frac{dy}{dt} = -60, \qquad x = 0.4,\quad \frac{dx}{dt} = 30, \qquad \text{find } \frac{dz}{dt}.$$

**Step 3 — Equation relating the variables (Pythagorean theorem).**

$$z^2 = x^2 + y^2.$$

**Step 4 — Differentiate with respect to \(t\).**

$$2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} \quad\Longrightarrow\quad z\,\frac{dz}{dt} = x\,\frac{dx}{dt} + y\,\frac{dy}{dt}.$$

**Step 5 — Find \(z\) at the instant.**

$$z = \sqrt{0.4^2 + 0.3^2} = \sqrt{0.16 + 0.09} = \sqrt{0.25} = 0.5.$$

**Step 6 — Plug in and solve.**

$$0.5\,\frac{dz}{dt} = (0.4)(30) + (0.3)(-60) = 12 - 18 = -6 \quad\Longrightarrow\quad \frac{dz}{dt} = -12.$$

**Step 7 — Interpret.** The negative sign means \(z\) is getting smaller: car A closing in on the intersection outweighs car B pulling away.

**Final answer:** the distance between the cars is **decreasing at 12 mi/h**.

**3.**
**Step 1 — Name the variables.** Let \(r\) be the radius (cm), \(V\) the volume (cm³), and \(S\) the surface area (cm²) at time \(t\).

**Step 2 — Given and wanted.** Air is *leaving*, so volume is decreasing:

$$\frac{dV}{dt} = -72\pi \text{ cm}^3/\text{s}, \qquad \text{find } \frac{dr}{dt} \text{ and } \frac{dS}{dt} \text{ when } r = 6.$$

**Step 3 (a) — Differentiate the volume formula.** From \(V = \tfrac{4}{3}\pi r^3\):

$$\frac{dV}{dt} = 4\pi r^2\,\frac{dr}{dt}.$$

**Step 4 (a) — Plug in and solve.**

$$-72\pi = 4\pi(6)^2\,\frac{dr}{dt} = 144\pi\,\frac{dr}{dt} \quad\Longrightarrow\quad \frac{dr}{dt} = -\frac{72\pi}{144\pi} = -\frac{1}{2} \text{ cm/s}.$$

**Step 5 (b) — Differentiate the surface-area formula.** From \(S = 4\pi r^2\):

$$\frac{dS}{dt} = 8\pi r\,\frac{dr}{dt}.$$

**Step 6 (b) — Plug in \(r = 6\) and \(\tfrac{dr}{dt} = -\tfrac12\) from part (a).**

$$\frac{dS}{dt} = 8\pi(6)\left(-\frac{1}{2}\right) = -24\pi \approx -75.4 \text{ cm}^2/\text{s}.$$

**Final answer:** (a) the radius is **decreasing at \(\tfrac12\) cm/s**; (b) the surface area is **decreasing at \(24\pi \approx 75.4\) cm²/s**.

**4.**
**Step 1 — Draw and name the variables.** The observer, the launch point, and the balloon form a right triangle. Let \(h\) be the balloon's height (ft) and \(\theta\) the angle of elevation (radians). The horizontal leg is fixed at \(500\) ft.

**Step 2 — Given and wanted.**

$$\theta = \frac{\pi}{4}, \qquad \frac{d\theta}{dt} = 0.14 \text{ rad/min}, \qquad \text{find } \frac{dh}{dt}.$$

**Step 3 — Equation relating \(h\) and \(\theta\).** Opposite over adjacent:

$$\tan\theta = \frac{h}{500}.$$

**Step 4 — Differentiate with respect to \(t\).** The derivative of \(\tan\theta\) is \(\sec^2\theta\), times \(\tfrac{d\theta}{dt}\) by the chain rule:

$$\sec^2\theta\,\frac{d\theta}{dt} = \frac{1}{500}\,\frac{dh}{dt} \quad\Longrightarrow\quad \frac{dh}{dt} = 500\sec^2\theta\,\frac{d\theta}{dt}.$$

**Step 5 — Evaluate \(\sec^2\theta\) at \(\theta = \tfrac{\pi}{4}\).**

$$\cos\frac{\pi}{4} = \frac{\sqrt{2}}{2} \quad\Longrightarrow\quad \sec\frac{\pi}{4} = \sqrt{2} \quad\Longrightarrow\quad \sec^2\frac{\pi}{4} = 2.$$

**Step 6 — Plug in and solve.**

$$\frac{dh}{dt} = 500(2)(0.14) = 140 \text{ ft/min}.$$

(Sanity check: at \(\theta = \tfrac{\pi}{4}\) the balloon is at \(h = 500\tan\tfrac{\pi}{4} = 500\) ft, though we didn't need \(h\) here.)

**Final answer:** the balloon is rising at **140 ft/min**.

**5.**
**Step 1 — Draw and name the variables.** Look at one triangular end. Let \(h\) be the water depth (ft), \(b\) the width of the water's surface (ft), and \(V\) the volume of water (ft³).

**Step 2 — Given and wanted. Convert units first!** \(6\) in \(= 0.5\) ft.

$$\frac{dV}{dt} = 12 \text{ ft}^3/\text{min}, \qquad \text{find } \frac{dh}{dt} \text{ when } h = 0.5 \text{ ft}.$$

**Step 3 — Relate \(b\) and \(h\) with similar triangles.** The water's cross-section is a triangle similar to the end of the trough:

$$\frac{b}{h} = \frac{3}{1} \quad\Longrightarrow\quad b = 3h.$$

**Step 4 — Write \(V\) in terms of \(h\) only.** Using \(V = \tfrac12 b h L\) with \(L = 10\):

$$V = \frac{1}{2}(3h)(h)(10) = 15h^2.$$

**Step 5 — Differentiate with respect to \(t\).**

$$\frac{dV}{dt} = 30h\,\frac{dh}{dt}.$$

**Step 6 — Plug in and solve.**

$$12 = 30(0.5)\,\frac{dh}{dt} = 15\,\frac{dh}{dt} \quad\Longrightarrow\quad \frac{dh}{dt} = \frac{12}{15} = \frac{4}{5} \text{ ft/min}.$$

In inches: \(\tfrac45 \cdot 12 = 9.6\) in/min.

**Final answer:** the water level is rising at **\(\tfrac{4}{5}\) ft/min** (\(= 9.6\) in/min).

**6.**
**Step 1 — Draw and name the variables.** Put the spotlight at ground level. The light ray passes over the top of the man's head and hits the wall. Let \(x\) be the man's distance from the spotlight and \(y\) the height of his shadow on the wall (both in m). The spotlight-to-wall distance is fixed at \(12\) m.

**Step 2 — Given and wanted.** He walks away from the spotlight, so \(x\) is increasing. When he is \(4\) m from the wall, he is \(12 - 4 = 8\) m from the spotlight:

$$x = 8, \qquad \frac{dx}{dt} = 1.6 \text{ m/s}, \qquad \text{find } \frac{dy}{dt}.$$

**Step 3 — Set up the similar triangles.** The ray from the spotlight makes two right triangles that share the angle at the spotlight:

- small triangle: base \(x\) (spotlight to man), height \(2\) (the man)
- large triangle: base \(12\) (spotlight to wall), height \(y\) (the shadow)

Corresponding sides are proportional (height over base):

$$\frac{y}{12} = \frac{2}{x} \quad\Longrightarrow\quad y = \frac{24}{x} = 24x^{-1}.$$

**Step 4 — Differentiate with respect to \(t\).**

$$\frac{dy}{dt} = -24x^{-2}\,\frac{dx}{dt} = -\frac{24}{x^2}\,\frac{dx}{dt}.$$

**Step 5 — Plug in and solve.**

$$\frac{dy}{dt} = -\frac{24}{8^2}(1.6) = -\frac{24}{64}(1.6) = -\frac{3}{8}(1.6) = -0.6 \text{ m/s}.$$

**Step 6 — Interpret.** The negative sign means the shadow is getting shorter. That makes sense: as he gets closer to the wall, he blocks less of the light's spread. (Check: at \(x = 8\) the shadow is \(y = 24/8 = 3\) m tall.)

**Final answer:** the shadow is **getting shorter at 0.6 m/s**.
