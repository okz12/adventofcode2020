--- Day 15: Rambunctious Recitation ---

You catch the airport shuttle and try to book a new flight to your vacation island. Due to the storm, all direct flights have been cancelled, but a route is available to get around the storm. You take it.


While you wait for your flight, you decide to check in with the Elves back at the North Pole. They're playing a **memory game** and are <span title="Of course they are.">ever so excited</span> to explain the rules!


In this game, the players take turns saying **numbers**. They begin by taking turns reading from a list of **starting numbers** (your puzzle input). Then, each turn consists of considering the **most recently spoken number**:

<ul>
<li>If that was the **first** time the number has been spoken, the current player says **`0`**.</li>
<li>Otherwise, the number had been spoken before; the current player announces **how many turns apart** the number is from when it was previously spoken.</li>
</ul>

So, after the starting numbers, each turn results in that player speaking aloud either **`0`** (if the last number is new) or an **age** (if the last number is a repeat).


For example, suppose the starting numbers are `0,3,6`:

<ul>
<li>**Turn 1**: The `1`st number spoken is a starting number, **`0`**.</li>
<li>**Turn 2**: The `2`nd number spoken is a starting number, **`3`**.</li>
<li>**Turn 3**: The `3`rd number spoken is a starting number, **`6`**.</li>
<li>**Turn 4**: Now, consider the last number spoken, `6`. Since that was the first time the number had been spoken, the `4`th number spoken is **`0`**.</li>
<li>**Turn 5**: Next, again consider the last number spoken, `0`. Since it **had** been spoken before, the next number to speak is the difference between the turn number when it was last spoken (the previous turn, `4`) and the turn number of the time it was most recently spoken before then (turn `1`). Thus, the `5`th number spoken is `4 - 1`, **`3`**.</li>
<li>**Turn 6**: The last number spoken, `3` had also been spoken before, most recently on turns `5` and `2`. So, the `6`th number spoken is `5 - 2`, **`3`**.</li>
<li>**Turn 7**: Since `3` was just spoken twice in a row, and the last two turns are `1` turn apart, the `7`th number spoken is **`1`**.</li>
<li>**Turn 8**: Since `1` is new, the `8`th number spoken is **`0`**.</li>
<li>**Turn 9**: `0` was last spoken on turns `8` and `4`, so the `9`th number spoken is the difference between them, **`4`**.</li>
<li>**Turn 10**: `4` is new, so the `10`th number spoken is **`0`**.</li>
</ul>

(The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)


Their question for you is: what will be the **`2020`th** number spoken? In the example above, the `2020`th number spoken will be `436`.


Here are a few more examples:

<ul>
<li>Given the starting numbers `1,3,2`, the `2020`th number spoken is `1`.</li>
<li>Given the starting numbers `2,1,3`, the `2020`th number spoken is `10`.</li>
<li>Given the starting numbers `1,2,3`, the `2020`th number spoken is `27`.</li>
<li>Given the starting numbers `2,3,1`, the `2020`th number spoken is `78`.</li>
<li>Given the starting numbers `3,2,1`, the `2020`th number spoken is `438`.</li>
<li>Given the starting numbers `3,1,2`, the `2020`th number spoken is `1836`.</li>
</ul>

Given your starting numbers, **what will be the `2020`th number spoken?**



Your puzzle answer was `662`.
--- Part Two ---

Impressed, the Elves issue you a challenge: determine the `30000000`th number spoken. For example, given the same starting numbers as above:

<ul>
<li>Given `0,3,6`, the `30000000`th number spoken is `175594`.</li>
<li>Given `1,3,2`, the `30000000`th number spoken is `2578`.</li>
<li>Given `2,1,3`, the `30000000`th number spoken is `3544142`.</li>
<li>Given `1,2,3`, the `30000000`th number spoken is `261214`.</li>
<li>Given `2,3,1`, the `30000000`th number spoken is `6895259`.</li>
<li>Given `3,2,1`, the `30000000`th number spoken is `18`.</li>
<li>Given `3,1,2`, the `30000000`th number spoken is `362`.</li>
</ul>

Given your starting numbers, **what will be the `30000000`th number spoken?**



Your puzzle answer was `37312`.