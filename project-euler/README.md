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

# Testing
To test that any of the above gives correct result and/or performs in the claimed time, use
the following command:

	rapydscript -x p[n].pyj

