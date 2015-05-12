# Project Euler Challenges
These are from projecteuler.net. I've solved many of these a long time ago in Python and Ruby. However, since the website's challenges provide a good way to learn algorithms and/or a new language, I decided to use them both to test out my language's brevity and as a shameless plug for my language: [RapydScript](https://github.com/atsepkov/RapydScript).

# Purpose
The solutions posted here attempt to both showcase the brevity/features of the language as well as make use of proper techniques for each problem. For example, if a problem asks one to do something with 2**1000, the problem probably expects the developer to be clever enough to figure out how to compute such number without storing it all in integer data type rather than foolishly performing the operation and bragging about the fact that his language of choice switches to big integers behind the scenes. With that said, in cases where a clever/elegant hack is possible, I may decide to use it.

# Timing
The goal is to have these solutions execute efficiently, as per Project Euler guidelines. I use node's internal timer to time and output these results via the `test` script:

	1.pyj: 1ms
	2.pyj: 76ms
	3.pyj: 2ms
	4.pyj: 5ms
	5.pyj: 1ms
	6.pyj: 1ms
	7.pyj: 8ms
	8.pyj: 1ms
	9.pyj: 1ms
	10.pyj: 123ms
	11.pyj: 4ms
	12.pyj: 317ms
	13.pyj: 1ms
	14.pyj: 2279ms
	15.pyj: 1ms
	16.pyj: 18ms
	17.pyj: 2ms
	18.pyj: 1ms
	19.pyj: 4ms
	20.pyj: 2ms
	21.pyj: 8ms
	22.pyj: 19ms
