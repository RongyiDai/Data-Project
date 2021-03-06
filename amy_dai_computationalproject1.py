# -*- coding: utf-8 -*-
"""Amy Dai - ComputationalProject1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QMLs6nSFbrIXCHAGMleFPughMrRtcgfn

# Computational Project 1: Modeling Population Dynamics

In this project, our goals are 
+ to learn about an interesting application of linear algebra, and 
+ to learn to implement matrix computations in python.

In particular, in this project, we will see how linear algebra plays a prominent role in modeling changes in population distributions over time.  The computational and writing/interpretation components of this project are equally important.

Please refer to the [Lecture 6 demonstration](https://colab.research.google.com/drive/15hcR--leZTtidWdZqDFJI8E6WwvLl_fB) for reference on matrix computation with python.

This project will be automatically collected on Friday March 1 at 9am EST.


(This project is adapted from https://users.wpi.edu/~goulet/ph/proj4.htm)

## Background

Population modeling is useful from many different perspectives:
1. planners at the city, state, and national level who look at human populations and need forecasts of populations in order to do planning for future needs. These future needs include housing, schools, care for the elderly, jobs, and utilities such as electricity,water and transportation.

2. businesses do population planning so as to predict how the portions of the population that use their product will be changing.

3. Ecologists use population models to study ecological systems, especially those where endangered species are involved so as to try to find measures that will restore the population.

4. medical researchers treat microorganisms and viruses as populations and seek to understand the dynamics of their populations; especially why some thrive in certain environments but don't in others.   

Using data about the current population along with the knowledge of quality of healthcare, life expectancy, birth rates, and so on, one can create a model that predicts how the population will change over time.

For example, in Japan and Scandinavian countries, data shows that a large portion of the population is in an older age group and birth rates are low, which suggests that the size of their populations might shrink over time.  On the other hand, countries with a large birth rate might still suffer from shrinking populations if the quality of health care is very low (such that it significantly effects "survival rates" and decreases life expectancies).

<b>We are going to work with a particular population model to predict how population distribution across age groups changes over time.</b>

## Your Project

Suppose we are studying the population dynamics of Los Angeles for the purpose of making a planning proposal to the city which will form the basis for predicting school, transportation, housing, water, and electrical needs for the years from 2000 on.


### The Model

1. First, we will consider seven age groups: 0-9 year olds, 10-19, 20-29, up to 60+.  It make sense to take intervals of 10 years as the census is taken every 10 years.

<table>
   <tr>
     <th>Age Group</th>
     <th>Ages (years) </th>
  </tr>
  <tr>
    <td><b>Group 1</b></td>
    <td>0-9<td>
  </tr>
  <tr>
    <td><b>Group 2</b></td>
    <td>10-19<td>
  </tr>
  <tr>
    <td><b>Group 3</b></td>
    <td>20-29<td>
  </tr>
  <tr>
    <td><b>Group 4</b></td>
    <td>30-39<td>
  </tr>
  <tr>
    <td><b>Group 5</b></td>
    <td>40-49<td>
  </tr>
  <tr>
    <td><b>Group 6</b></td>
    <td>50-59<td>
  </tr>
  <tr>
    <td><b>Group 7</b></td>
    <td>60+<td>
  </tr>
</table>

2. We will consider **a unit of time to be 10 years** and time $t = 0$ to be the year 1990.  Thus, $t = 1$ will be the year 2000, etc.

3. We will also incorporate our knowledge about birth rates, quality of health care, life expectancy, etc. to model how the current population distribution (i.e., how many people are in each age group today) influence the population distribution ten years from now into numbers which we will call "survival fractions".  <br> <br> The **survival fraction** of an age group is the fraction of people in an age group who will survive to the next age group ten years later.<br> <br> 
For example, the fraction of "newborns" (0-9) who survive to ages 10-19, the fraction of 10 to 19 year olds who survive to 20-29, etc. This type of data is compiled, for example, by actuaries working for insurance companies for life and medical insurance purposes.

<b>Example</b>
+ Suppose that there are initially 1000 newborns, 600 people aged 10-19, and 1000 people aged 20-29: $$\vec x(0) = \begin{bmatrix}x_1(0)\\ x_2(0) \\ x_{ 3}(0)\end{bmatrix} = \begin{bmatrix} 1000 \\ 600 \\ 1000\end{bmatrix} $$

+ Suppose that the survival fraction of newborns who survive to age 10 is 0.99 and the survival fraction of 10-19 year olds who survive to 20 is 0.95

+ Then, 10 years later, at time $t= 1$, the number of people aged 10-19 would be:
    $$x_2(1) = 0.99 \times x_1(0) = 990$$
   etc.

<b>More generally</b>

The basic equations we begin with are
\begin{equation}
\vec x(t+1) = A\vec x(t), \quad t=0,1,2, \ldots  \tag{1}
\end{equation}
where 
  + $x(0)$ is a given vector of initial (at time $t = 0$) number of people within each age group, and $x(t)$ denotes the number of people within each age group at time $t$.
  + Each vector $x(t)$ has 7 entries:
  $$ x(t) = \begin{bmatrix} x_1(t) \\ x_2(t) \\ \vdots \\ x_7(t) \end{bmatrix}$$
  where $x_1(t)$ is the number of people in the first age group at time $t$, etc.
  + $A$ is a matrix that helps us model how populations in the different age groups change.  Information such as survival fractions are stored as entries of this matrix. 


### The Data

Suppose further that the population distribution as of 1990 in LA  is

<table>
   <tr>
     <th>Age Group</th>
     <th>Population of LA in 1990 ($\times 10^{5}$)</th>
  </tr>
  <tr>
    <td><b>Group 1</b></td>
    <td>3.1<td>
  </tr>
  <tr>
    <td><b>Group 2</b></td>
    <td>2.8<td>
  </tr>
  <tr>
    <td><b>Group 3</b></td>
    <td>2.0<td>
  </tr>
  <tr>
    <td><b>Group 4</b></td>
    <td>2.5<td>
  </tr>
  <tr>
    <td><b>Group 5</b></td>
    <td>2.0<td>
  </tr>
  <tr>
    <td><b>Group 6</b></td>
    <td>1.8<td>
  </tr>
  <tr>
    <td><b>Group 7</b></td>
    <td>2.9<td>
  </tr>
</table>

and that the $A$ for our  model is
$$  A = \begin{bmatrix} 
0 & 1.1 & 1.2 & 0.9 & 0.1 & 0 & 0 \\
0.7 & 0 & 0 & 0 & 0 & 0 & 0\\
0 & 0.82 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0.97 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0.97 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0.90 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0.87 & 0.5
\end{bmatrix}$$

The numbers in this matrix comes from analysis of data; they incorporate information about the population, including birth rates, survival rates, etc.

#### Part Zero: Setup

We will need to use the packages numpy and scipy.  In the code cell below, please import them as np and sp, respectively.
"""

import numpy as np
import scipy as sp

"""#### Part One

Interpret carefully each of the nonzero entries in the matrix $A$.  In particular, consider the linear equation that corresponds to each row of $A$ and explain why this equation makes sense.

In addition, indicate what factors you think might change those numbers (they might be social, economical, political or environmental).

In the first row, the non-zero entries are the birth rate of that particular age group. For instance, the 2.8 times 10^5 people in Group 2 will in total have 1.1 times 2.8 times 10^5 kids within 0-9 years ten years later. From the second row to the final row, the non-zero entries(0.7, 0.82, 0.97, 0.97, 0.90, and 0.87) are all survival fractions of the corresponding age group in the previous years. The last entry in the final row, 0.5, is the survival fraction of the 60+ age group, meaning that in addition to the 0.87 * 1.8 * 10^5 people in Group 6 entering Group 7 10 years later, there will also be 50% of the population in Group 7 remain alive after 10 years.

In terms of factors that might change the numbers:

- When there is a politically turbulent era, wars being waged, the survival fractions for Group 3 -- 5 (0.97, 0.97, 0.90) will be likely to decrease, since they are the appropriate age to serve the army. 

- When the healthcare system improves, the survival fractions for Group 1, 6, and 7 will increase, since small children are more likely to survive through their most fragile period, and seniors can get better treatment for their diseases. Similarly, when the healthcare system is bad, or when there is serious environmental pollution or epidemics, the survival fractions for Group 1, 6, and 7 will decrease. 

- When the country is more economically developed, the birth rate will be likely to decrease -- the non-zero entries in the first row will be lower, since mortality rates are lower and birth control method is easily accessed, while in less developed country, the birth rate is higher -- the non-zero entries in the first row will be higher.

#### Part Two

Predict:

+ what the population distribution will look like in 2020, 2030, and 2040.

+ what the total population will be in each of those years

+ by what fraction the total population changed each year
"""

# Your code for Part Two
#  (Among others, you will need to enter the matrix A and vector x_0 here, and 
#   use this matrix along with equation (1) above to compute the total populations)

# From Data:
A = np.matrix([[0,1.1,1.2,0.9,0.1,0,0],[0.7,0,0,0,0,0,0],[0,0.82,0,0,0,0,0],[0,0,0.97,0,0,0,0],[0,0,0,0.97,0,0,0],[0,0,0,0,0.9,0,0],[0,0,0,0,0,0.87,0.5]])

x_0 = np.matrix([[310000],[280000],[200000],[250000],[200000],[180000],[290000]]) 


# Compute population vectors in future years:
x_1 = A * x_0
x_2 = A * x_1
x_3 = A * x_2
x_4 = A * x_3
x_5 = A * x_4



# Compute total population in each of the years 2020, 2030, 2040:
total_pop_2020 = x_3.sum()
total_pop_2030 = x_4.sum()
total_pop_2040 = x_5.sum()

# Fraction in which the total population change from each year to the next:
# ratio of total_pop_2030 to total_pop_2020:
ratio_30_20 = total_pop_2030 / total_pop_2020

# ratio of total_pop_2040 to total_pop_2040:
ratio_40_30 = total_pop_2040 / total_pop_2030

print (x_0, x_1, x_2, x_3, x_4, x_5)
print (total_pop_2020)
print (total_pop_2030)
print (total_pop_2040)
print (ratio_30_20)
print (ratio_40_30)

"""The population distribution in 2020 will be: [[1043396.8 ]
 [ 499149.  ]
 [ 455182.  ]
 [ 172601.8 ]
 [ 216030.64]
 [ 169362.  ]
 [ 343577.5 ]], and the total population will be around 2899299.
 
The population distribution in 2030 will be: [[1272226.984]
 [ 730377.76 ]
 [ 409302.18 ]
 [ 441526.54 ]
 [ 167423.746]
 [ 194427.576]
 [ 319133.69 ]], and the total population will be around 3534418. The ratio will be: 1.219.


 The population distribution in 2040 will be: [[1708694.4126 ]
 [ 890558.8888 ]
 [ 598909.7632 ]
 [ 397023.1146 ]
 [ 428280.7438 ]
 [ 150681.3714 ]
 [ 328718.83612]], and the total population will be around 4502867. The ratio will be: 1.274.

#### Part Three

Decide if you believe the population is going to (1) zero, (2) becoming "stable" (i.e., reached a "steady state" where the population in the different age groups remain constant), or (3) is "unstable" in the long run (i.e., the population increases without bound). 

Be sure and describe in your write up how you arrived at your conclusion.

If you have decided it is unstable, simulate it long enough that the column matrices for two successive populations are proportional to one another. Calculate that proportionality factor to one decimal place and report it.
"""

# Your code for Part Three, if any
#   You may want to compute population distributions for additional years, etc.
#   in order to see a pattern that would help you answer the question in part 3

x = np.matrix([[310000],[280000],[200000],[250000],[200000],[180000],[290000]])
y = 0
total_pop = []
pop_distri = []
while y < 30:
  x = A * x
  #print (x.sum())
  total_pop.append(x.sum())
  pop_distri.append(x)
  y += 1
#print (len((pop_distri)))
  
# This is to calculate the ratio of the total population between two successive generations in 300 years
# Delete the quotation mark if you want to run this part.
"""i = 1
while i < len(total_pop):
  proportion = total_pop[i] / total_pop[i - 1]
  print (proportion)
  i += 1"""

# This is to calulate the ratio of the same age group between two successive generations in 300 years
proportion = []
for index in range(1,len(pop_distri)):
  for row in range(7):
    ppt = pop_distri[index][row] / pop_distri[index-1][row] 
    proportion.append(ppt)
#print (len(proportion))

print ("Group 1                  Group 2                 Group3                  Group 4                     Group 5                   Group 6                 Group 7")

for i in range(0,203,7):
  print (proportion[i:i+7])

"""I believe that the population will be unstable in the long run -- it continues to grow without bound. I print out the total population in a hundred years since 1990, and the number is in an increasing trend.

Simulating 300 years after 1990, I found out that the proportionality factor would be 1.3. I calculated the ratio of every corresponding element in two successive generations and put them into a list, which consists of 203 (29 * 7 = 203) elements. 

The elements in the list are such that x(t+1)[0]/x(t)[0], x(t+1)[1]/x(t)[1], x(t+1)[2]/x(t)[2]....0<=t<=29  (numbers in brackets indicate the index of the element in the matrix)

I print out the result in a way such that the proportionality factor of each age group between two successive generations is on the same row. Each row has 7 elements(Group 1 - Group 7), and there are 29 rows (ratio between 30 population distribution matrices). From the result, we can see that, at first, the ratio of the same age group between successive generations is quite different, but later after 100 years (10 rows), the ratio began to be closer to each other, and the ratio of total population began to be around 1.28037 (~1.3) . After another 100 years, the proportional factors of different age groups started to be closer, and is approaching the ratio of total population 1.28037. At last, they remain very close for 100 years. So the proportionality factor of column matrices is 1.3.

#### Part Four

How does the basic model change if immigration is introduced? Suppose we assume that a constant number of immigrants are added to each age group during each time interval. What will equation (1) now look like?

What will the solution, (2) now look like?

How do your predictions change for 2020, 2030, and 2040 change if there are 20,000 people entering each age group during each 10 year period? How much will the total population have changed in 2040 as compared to the prior no immigration prediction?
"""

# Your code for Part Four

# new matrix that incorporates immigration
A_imm =np.matrix([[0,1.1,1.2,0.9,0.1,0,0,1],[0.7,0,0,0,0,0,0,1],[0,0.82,0,0,0,0,0,1],[0,0,0.97,0,0,0,0,1],[0,0,0,0.97,0,0,0,1],[0,0,0,0,0.9,0,0,1],[0,0,0,0,0,0.87,0.5,1],[0,0,0,0,0,0,0,1]])

# new initial vector 
x_imm = np.matrix([[310000],[280000],[200000],[250000],[200000],[180000],[290000],[20000]])

# Prediction for 2020, 2030, 2040
year = 0                    
while year <= 4:
  x_imm = A_imm * x_imm
  x_pop = x_imm.sum()
  year += 1
  print ("Total population: {:,} in {}0 years.".format(x_pop, year))

"""Now the equation looks like x_imm(t+1) = A_imm times x_imm(t). A_imm is obtained by adding an 8th row with entry 0 to A, and an 8th column with entry 1 to A. x_imm(0) is obtained by adding a 20000 to the 8th row. So now the final product of A_imm times x_imm(t) will be an 8 by 1 matrix, with every age group incorported with immigrants, and a final row of 20000 which is the new generation of immigrant coming in in that decade.

There will be more population in 2020, 2030, and 2040. There will be approximately 3,433,605.74 in 2020. 4,298,912.23 in 2030. 5,545,270.71 in 2040. There will be approximately 1,000,000 more population in 2040 when there is immigration than when there is not.

## Reflections

Please briefly write:
1. One new thing that you learn from this project
2. One aspect of this project that you found most interesting OR most challenging OR both.
3. If you discuss any part of the project with anyone ( classmate(s), tutor(s), etc.), please ackowledge them here.

1. I learned that if the population is in unstable growth, the rate of growth will increase and finally reach a certain value, and then the population just keeps growing at that rate, if no measures are carriet out. I believe that graph will be J-shaped.
    
    I also learned that at first the growth rate between age groups can be different, but it will become closer to each other after a long time. And in order to notice this, only by calculating the ratio between <b>total population</b> is not enough.


2. The most interesting and challenging part would definitely be the third part where I need to calculate the proportionality factor of the same age group between two successive generations. It is challenging because we really need to simulate it long enough to see the trend. And obtaining the ratio between each age group makes it even harder, because we need to do 7 times between two matrices. But this is also very fun, this is the first time that I built the logic frame and coded the whole thing by myself without knowing any answers.
"""