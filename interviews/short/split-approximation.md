Description
===========
Write a function that takes a floating point number and an error threshold and returns an array of 2 integers that when divided approximate the floating point number within the passed in error threshold. These integers should be smallest possible integers that approximate the passed in number. 

For example:

	approx(0.5, 0.01) -> [1, 1]
	approx(0.33, 0.001) -> [1, 2]
	approx(0.66, 0.001) -> [2, 1]
	approx(0.67, 0.001) -> [2, 1]
	approx(0.375, 0.001) -> [3, 5]

