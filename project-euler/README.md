# Project Euler Challenges
These are from projecteuler.net. I've solved many of these a long time ago in Python and Ruby. However, since the website's challenges provide a good way to learn algorithms and/or a new language, I decided to use them both to test out my language's brevity and as a shameless plug for my language: [RapydScript](https://github.com/atsepkov/RapydScript).

# Purpose
The solutions posted here attempt to both showcase the brevity/features of the language as well as make use of proper techniques for each problem. For example, if a problem asks one to do something with 2**1000, the problem probably expects the developer to be clever enough to figure out how to compute such number without storing it all in integer data type rather than foolishly performing the operation and bragging about the fact that his language of choice switches to big integers behind the scenes. With that said, in cases where a clever/elegant hack is possible, I may decide to use it.

# Timing
The goal is to have these solutions execute efficiently, as per Project Euler guidelines (the goal is to have everything execute under a minute - 60000ms). I use node's internal timer to time and output these results via the `test` script. The timings here should be compared to JavaScript since that's effectively what the final code runs in, comparing them to other dynamically-typed languages may fall in the same ballpark but don't be surprised to see variations of 200% or more.

	p1.pyj: 1ms
	p2.pyj: 76ms
	p3.pyj: 2ms
	p4.pyj: 5ms
	p5.pyj: 1ms
	p6.pyj: 1ms
	p7.pyj: 8ms
	p8.pyj: 1ms
	p9.pyj: 1ms
	p10.pyj: 123ms
	p11.pyj: 4ms
	p12.pyj: 317ms
	p13.pyj: 1ms
	p14.pyj: 2279ms
	p15.pyj: 1ms
	p16.pyj: 18ms
	p17.pyj: 2ms
	p18.pyj: 1ms
	p19.pyj: 4ms
	p20.pyj: 2ms
	p21.pyj: 8ms
	p22.pyj: 19ms
	p23.pyj: 5867ms
	p24.pyj: 1ms
	p25.pyj: 1ms
	p26.pyj: 6ms
	p27.pyj: 78ms
	p28.pyj: 1ms
	p29.pyj: 3ms
	p30.pyj: 51ms
	p31.pyj: 2ms
	p32.pyj: 19ms
	p33.pyj: 13ms
	p34.pyj: 2221ms
	p35.pyj: 138ms
	p36.pyj: 1287ms
	p37.pyj: 128ms
	p38.pyj: 215ms
	p39.pyj: 2ms
	p40.pyj: 2ms
	p41.pyj: 737ms
	p42.pyj: 7ms
	p43.pyj: 2995ms

# Testing
To test that any of the above gives correct result and/or performs in the claimed time, use
the following command:

	rapydscript -x p[n].pyj

# Optimizations
For those interested, the optimization techniques I employ typically fall into the following categories:

## Memoization
When a function is called often with the same arguments (with the intent of producing the same result), it often makes sense to memoize it, especially if you're calling it thousands of times. Memoization is wrapping the function in another function, that dynamically forms a look-up table for previous results. This allows you to bypass the logic in the function during the next call altogether, using the value from the lookup table instead.

## Converting Arrays to Hashes
Similar to memoization, except that array already contains the set of results you want. The problem is that array is best suited for answering questions of type "What's the value at index N?", not "Does this value exist in array?". The first question can be answered in constant time, whereas the second in linear. This is typically not a problem when you need the answer rarely, but on Project Euler, you may be asking this questions thousands or millions of times. This is where hash comes in handy, with a mapping of `"value": True`, it can answer the second question in constant time.

## Pruning
When dealing with tree-like behavior (recursion with branching, etc.) you can save yourself a lot of time by pruning. Pruning is eliminating paths that you know won't contain the right answer before you go too deep into them. Just like an effective leader is one who can eliminate tasks that add no value from his schedule, an effective algorithm is one that can eliminate branches that add no value. Defining good lower/upper bounds for the problem based on the givens is a manual version of pruning.

## Building Upon Smaller Cases
Similar to memoization, but with an extra step. Not sure if there is a fancy term for this, but the concept involves taking a simple case, and computing more complex versions of it on the spot. For example, if we know that triangle with sides 3, 4, and 5 is a right triangle, we also know this to be the case for any triangle whose sides are multiples of those numbers. This seems simple, but it's a powerful concept. Many optimizations, including the Sieve of Eratosthenes and Euclid's approach to finding Triangular Triples, are based on it.

## Heuristics
I have yet to employ them on Project Euler, but the tile challenge in this same repository makes use of them. This is similar to using a map. You don't know if you'll find the shortest route, but choosing roads whose direction is towards the point of interest is more likely to get you there than ones that go in the opposite direction. What you're doing here is prioritizing "good" paths over "bad".
