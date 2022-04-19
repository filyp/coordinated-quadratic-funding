# Quadratic funding without a matching pool

## Motivation
[Quadratic funding](https://vitalik.ca/general/2019/12/07/quadratic.html) is a powerful mechanism for resolving some [collective action problems](https://en.wikipedia.org/wiki/Collective_action_problem). But it has a major limitation - it relies on some third party, that provides a matching pool of funds. 

In the most dangerous collective action problems, we don't have such third party helping us from above. For example in conflict between global superpowers, or even worse, between TAI systems (as described [here](https://www.lesswrong.com/posts/KMocAf9jnAKc2jXri/sections-1-and-2-introduction-strategy-and-governance)), we won't have anyone more powerful trying to resolve the conflict, like a galactic mom. An example of such situation is global superpowers trying to coordinate to fight climate change, or to pay [AI alignment tax](https://youtu.be/-vsYtevJ2bc?t=547) (more info [here](https://forum.effectivealtruism.org/tag/alignment-tax)).

## Solution
One thing we can try in this situation, is to create a smart contract where each party says "I'll pay more if others pay more". This way, if you decide to pay 1$ more, it causes the pot to grow by more than 1$, because your dollar caused other parties to pay some more. This leverage, in some situations can be enough to make someone pay, because the value they get out of the bigger pot is higher than what they have to pay.

Some properties that it would be nice to have in such a system are:
- continuity - every increase in your payment causes an increase in others' payments
- known payment limit - you won't have to pay more than some limit you chose
- everyone is incentivised to contribute something - just like in quadratic funding, small contributions get a high leverage, and this leverage can get arbitrarily high - so even if you're only willing to pay if you get >100x leverage, there is some contribution size that gives you such a high leverage

A very simple system that has these properties is given by those equations: 

![formula](https://render.githubusercontent.com/render/math?math=h=\sum_{i}^{}\sqrt{payment_i})

![formula](https://render.githubusercontent.com/render/math?math=payment_i(h)=\frac{limit_i}{\frac{\pi}{2}}arctan(h*saturation\_speed_i))

Payment<sub>i</sub> is the amount that i'th person has to pay, limit<sub>i</sub> is the i'th person's payment limit, and saturation_speed<sub>i</sub> tells how quickly this limit will be approached as new people make payments.

It turns out, this system has a pretty graphical representation:
![solution_finding](https://raw.githubusercontent.com/filyp/coordinated-quadratic-funding/main/videos/solution_finding.gif)
<!-- <video src="https://raw.githubusercontent.com/filyp/coordinated-quadratic-funding/main/videos/solution_finding.mp4" controls="controls" style="max-width: 730px;" autoplay loop></video> -->
Each quarter-cirlce represents one person's contribution. Area of this quarter-circle is the payment limit - the maximum amount they can pay. The yellow areas are what they currently pay in this particular situation. The squares on the right have the same areas as the respective sectors. So the height of the tower of squares represents `h` - the sum of square roots of payments. The distance of a quarter-circle's center to the axes meeting points is `1/saturation_speed` - for small `saturation_speed`, the quarter-circle is put further to the left and you can see that they saturate more slowly.

The animation shows the procedure for finding the solution to those two equations. We start with some arbitrary `h`, then compute the payments (yellow sectors), then compute `h`, recomute payments, recompute `h`, and so on, until we converge on the stable solution. 

On the next animation, you see what happens when someone new joins the smart contract. Their contribution increases `h`, which makes others pay more. (Here the procedure of finding the solutions is ommited, and just the final solutions are shown). 
![leverage](https://raw.githubusercontent.com/filyp/coordinated-quadratic-funding/main/videos/leverage.gif)
<!-- <video src="https://raw.githubusercontent.com/filyp/coordinated-quadratic-funding/main/videos/leverage.mp4" controls="controls" style="max-width: 730px;" autoplay loop></video> -->
Here you can see the nice feature of quadratic funding: for small contributions, the leverage can get arbitrarily large. (To be precise, we compute the leverage **on the margin**, so how the pot changes if you pay 0.01$ more.)

![leverage_formula](<https://render.githubusercontent.com/render/math?math=leverage_i=\frac{d\ \sum_{j}^{}payment_j}{d\ payment_i}>)

Because of this feature, the amount that you're willing to pay is roughly proportional to how much you care for the common resource (see [this](https://vitalik.ca/general/2019/12/07/quadratic.html) explanation of QF for the precise argument). 

## Future work
### Quadratic funding problems
Unfortunately, this mechanism inherits all the problems that ordinary quadratic funding has, like Sybil attacks and influence buying, but here is ongoing research trying to solve them ([1.](https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553) [2.](https://ethresear.ch/t/mechanisms-to-prevent-sybil-attacks-in-on-chain-quadratic-funding-grants/9020)). If we fail to solve those problems, we can always fall back to linear funding (compute `h` as the sum of payments, instead of the sum of square roots of payments). This would be more robust and still enable coordination in some kinds of scenarios.

### Parameter choice
Each contribution is specified by two parameters: `limit`, and `saturation_speed`. The `limit` should be chosen by the contributor, but how the `saturation_speed` should be set is open.

For example if we set it constant for all the contributors (all the quarter-circles having the same centre), there may come a point where all of them will become almost fully saturated and the leverage for new contributors vanishes.

Alternatively, if each new contribution gets a smaller `saturation_speed` than the previous ones (quarter-circles get placed more to the left), there will always be some unsaturated quarter-cirles, so there always be a nice leverage for new contributors. But now, everyone is incentivised to wait for others to pay first, because being on the left means you pay less. This could create a deadlock where everyone is waiting for everyone.

If we made a simulation of how people behave in this system, we could test several methods of setting `saturation_speed`, and see which one results in the highest pot at the end.

### Strategic thinking
Another potential problem is strategic thinking. People can think: "even if I don't pay, the other people will fund this anyway". This problem is definitely smaller than in traditional fundraisers because of the leverage that this mechanism gives. But still, if many other people join this contract after you, the **real** leverage you get (what would happen counterfactually if you didn't contribute) will be smaller than the immediate leverage you had at the time of joining the contract (the amount that the pot increased divided by what you paid). This **real** leverage is much harder to compute, because it requires simulating what would happen if you didn't contribute, which requires simulating people's strategies.

A solution would be to modify the algorithm to make the leverages predictable, so that everyone would **know for certain** they will get the leverage they signed up for. This would prevent strategic thinking, and ahttps://github.com/filyp/coordinated-quadratic-funding/blob/main/CQF.ipynblso make people more willing to trust this system.


_________________________

You can find the code of this algorithm [here](https://github.com/filyp/coordinated-quadratic-funding/blob/main/CQF.ipynb).
