# Problem Statement
Given a histogram, find the largest rectangle which is completely covered by the bars of that histogram.

# Solution
“In this interview I’d like talk about a finding the area of the largest rectangle that can fit under a histogram.”
“Suppose you have a histogram in which every bar has an integer height, given as a list of nonnegative integers. (Draw [1,2,3,2,1] histogram). We want to find the area of the largest rectangle that can fit under the histogram, that is, the area of the largest rectangle that can be completely contained within the bars of the histogram. In this example, the area of the largest rectangle is 6 (the 2x3 rectangle). Setting aside efficiency concerns for the moment, what's the simplest, most obviously correct algorithm you can think of to find this?”

The right answer is something along the lines of "try all possible rectangles". They will hopefully propose one of these two algorithms:
- Iterate over all the possible left and right edges of the rectangles, and multiply by the minimum height of any bar between the left and right edges.
- Observe that any largest rectangle must use the top of some bar. Otherwise, we could raise the top edge and make larger rectangle. This algorithm iterates over each bar, and sees how far out to the left and right a rectangle that uses the top of this bar could extend.
“Are you familiar with the use of "big O" notation to describe an algorithm's running time? What's the running time of this algorithm [the naive algorithm they just described], as a function of the length of the input list?”

(Answer: O(n3) for the first, O(n2) for the second. If they didn't propose the second algorithm, describe it to them because it is the foundation of explaining the linear-time algorithm.)

“If we could find the left and right edge of the largest rectangle using the top of any particular bar in constant time, then the running time would be linear.”

(Explain the linear time algorithm. The basic idea is that it works like the O(n2) algorithm, except doesn't process each bar as it comes to it - instead it uses a stack. Whenever the top bar on the stack is taller than the current bar, it pops the top bar off the stack and processes it. When the top bar on the stack is no taller than the current bar, it pushes the location of the current bar on the stack and moves on.

To "process a bar" means to find the left and right edges of the largest rectangle that uses the top of that bar. The right edge is just before the current bar, since it's lower, and the left edge will be just after the previous item on the stack, since it's less than or equal to the top bar on the stack. Keep talking it over with them until it's clear they understand why it works. I think it's OK if your description isn't perfectly precise & clear - mine certainly isn't. It makes the interview closer to an actual work situation, and after all the idea is to figure out what it's like to work with the candidate technically.)

“Great! Now I'd like to have you code that algorithm and then we'll try it out on some test cases.”

If they're having trouble understanding the linear-time algorithm, you could ask them to implement the O(n2) algorithm first. It's a good stepping stone, and plus, while they're developing the linear-time algorithm, they can test it against the O(n2) algorithm on a bunch of randomly generated histograms.

Good test cases, roughly in difficulty order (please add to this list! Please note there's a child node with just the inputs which can be given to a candidate safely, please update that if this list changes):

	[1,2,3,2,1] = 6
	[1,3,2,3] = 6
	[2,0,1] = 2
	[1,0,2] = 2
	[1,4,5,3,1]
		9 - correct
		8 - the 3-height block doesn't find its left edge, so the 2x4 block wins.
		16 - this may seem like a crazy result, but it's actually a common error. they get to 3 and pop 5 and count it, but they don't pop 4 because the pops are contained in a simple if...else block (rather than a loop). then, they get to 1, pop 3, and still haven't popped 4. it's only at the very end that they pop 4, so the program thinks its right edge is at the right edge of the graph.
	[2,2,2]
		6 - correct
		4 - if they miss greatest rectangles that involve the first bar.
		0 - if they calculate left edge on pop only. Some people can't get the best rectangle if the best rectangle involves the last block.
	[1,3,4,1] - correct answer is 6 (2x3), but to get there, they need to track the right edge (to the right of 4), even they've already counted the height 4 rectangle, so 4 will have been popped from the stack already.
	[3,2,2] This tests that they're getting the correct left edge. This is especially tricky because there's nothing on the stack and so they need to get the left edge at index 1 even with nothing on the stack. (The usual description of the left edge is given as "the one to the right of the index that is on the top of the stack after we've finished popping to an index with h <= next_height". An alternative way of calculating the left edge is "the index of the last thing you popped during the pop loop", which doesn't fail here.). If you're lucky, you might even see the program crash on this test case. This is almost a guarantee that their logic for left edge is looking at the top structure on the stack when there is nothing on the stack, in a language that would die for that, such as Python. In Perl you can accidentally get the right answer through autovivification, but you would probably get an undefined warning if you use warnings.
		6 - correct
		4 - If they don't get the correct left edge because they're starting the rectangle at the current index, then they'll get 4 as the area.
		3 - If they just didn't push something onto the stack when going from i=1 to i=2, then they'll get 3 as the area. There's two reasons this could happen. One is that they "fixed" an index out of bounds error by first checking that there's something on the stack before doing the push-after-pop step. In Mason's opinion, this is a bad sign. It's cargo cult programming: "oh, I have an index out of bounds error. I'll just make it go away by checking this condition first, without thinking about why I might have this error". The other possibility is that they simply aren't pushing things onto the stack. Confirm with test case below - if it's the cargo cult case, they'll get 12 or 9 (because their bounds checking "fix" won't mess them up, and they'll either get the right answer or fail for the reason that case is designed to test). If it's just that they're not pushing anything onto the stack after a pop, then they'll get 8. Neither are particularly good signs. Make of it what you will.
	[1,4,4,3,3,1] This tests that they're not fudging the left edge by just going one back from the current index. In testing e.g. the prior case they may have found that they need to start their rectangle further back, but maybe they're cargo culting it by just subtracting one from the index they were starting at.
		12 - Correct answer
		9 - They've taken the bait. Their left edge is probably calculated as f-1 (where f is the index we're jumping from), or as t-2, (where t is the index we're jumping to). They need to calculate it as s+1, where s is the index of the thing that's left on the stack.
		8 - They probably just aren't pushing anything onto the stack when they pop down from 4->3, and are getting the 4x2 rectangle.
		6 - Run away! They aren't pushing anything when they go up to 4.
	[1,3,4,3,2] This tests ties when backtracking across something higher.
		9 - Correct answer
	[1,3,0,3,2] Surprisingly tricky
		4 - Correct answer

# Stacks

	my @stack;
	my $top = 0;
	$stack[++$top] = $foo;	# push
	$bar = $stack[$top--];	# pop
