## Project : Top-K Query Processing


### Goal
Implement a Top-K Query Processing with python.


### Problem Specification

- Each object X has m scores, one for each of m attributes.
- Objects are listed, for each attribute sorted by score.
- Each object is assigned an overall score by combining the attribute score using aggregate function or combining rule
- Therefore, Determine k objects with the hightes overall score.

#### 1. Implement Naive Algorithm.(Already implemented.)
- Compute averall score for every object by looking into each sorted list.

#### 2. Fagin's Algorithm
- Sequentially access all the sorted lists in parallel until there are k objects that have been seen in all lists.
- Perform random accesses to obtain the scores of all seen objects.

#### 3. Threshold Algorithm
- Access the elements sequentially
- At each sequential access, set the threshold t to be the aggregate of the scores seen in this access.
- Do random accesses and compute the scores of the seen objects.
- Maintain a list of top-k objects seen so far.
- Stop, when the scores of the top-k are greater or equal to the threshold.

#### 4. No Random Access Algorithm
- Access sequentially all lists in parallel until there are k objects for which the lower bound is higher than the upper bound of all other objects.
- Return top-k objects for which the lower bound is greatre than or equal to the upper bound of all other objects.


### Tips 
- In this Project, calculate the `cnt_access` is important that it shows the I/O times some extent. 
- I/O cost is very critical. So, we can compare the times between each algorithms.
- It would takes a significant time to operate the testcases!!(Not wrong.)


