INTRODUCTION

The stable marriage problem is a problem where one tries to match agents on one side of the market to agents on the other side, resulting in a stable match, i.e. no couple of agents can do better by matching outside the mechanism. Roth (1982) showed that no mechanism can be both stable and strategy-proof for two-sided matching problems. Markets using an unstable mechanism tend to unravel, which makes stability an important property. A solution to this problem could be somehting called approximate strategy-proofness. This is a property which is observed in large markets, wherein as the market grows, the percentage of agents who could usefully deviate shrinks. This repository contains an implementation of the deferred acceptance algorithm, as well as a lot of tooling for running simulations for how many people could usefully deviate for different sizes of the market and differing levels of correlation between agents' preferences. There is also a tool for plotting the results which are stored in the DATA-folder.

RUNNING THE CODE

The easiest way to get started would be to git clone the repository to your local machine, and then cd large_matching_market into the folder. Once there one can invoke the command-line tool by typing python3 start.py [--help] [simulation | plot] [...args].

There are two main components of the code. The most important is the simulation part, which is the code that runs the simlation of matching markets and calculates the number of agents that can usefully deviate. The other part is the plotting part, which lets one plot the data that the simulation generates.

SIMULATION

The simulation is started by running

python3 start.py simulation [-h] [args]

Running with the help flag will list all available arguments. Running without any arguments will run a very basic simulation with the market size going from n=10 to n=100 (exclusive), with a step-size of 10 and preference length of 10, and a correlation coefficient of 1.0. All of these parameteres can be changed and they are described in detail below. For each point below, the arguemnt comes first, and the short-hand is in parenthesis, if it exists.

--lower (-l) - Set the lower limit for the market size n, inclusive, defaults to 10
--upper (-u) - Set the upper limit for the market size n, exclusive, defaults to 100
--step (-s) - Set the step to increase the market size n after simulation for specific n terminates, defaults to 10
--pref-length (-k) - Accepts a list of different values for the length of the proposing side's preference orders, defaults to [10]
--correlation (-d) - Accepts a list of correlation coefficients to run the simulation for, defaults to [1.0]
--rounds (-r) - Sets the number of times the simulation should be run for each set of preference length and correlation coefficient, defaults to 1
--debug - Set the verbosity of the prints, -1 is no prints, 0 gives minimal information, 1 print a lot of inner workings of DA algorithm, defaults to 0
--logging - Set whether or not results should be written to file, defaults to true (probably only useful when developing and debugging)
--meta (-m) - If true this will make the simulation run loop through the above-specified simulation indefinitely until terminated, defaults to False

PLOTTING

The plotting is started by running

python3 start.py plot [-h] [args]

Running with the help flag will list all available arguments. Running without any arguments will run a very basic plot with the market size going from n=10 to n=400 (inclusive), for a correlation coefficient of 1.0 and preference length of k=10. All of these parameters can be changed and they are described in detail below. For each point below, the arguemnt comes first, and the short-hand is in parenthesis, if it exists.

--lower-limit (-l) - Set the lower limit for the market size n (x-axis), inclusive, defaults to None, i.e. no lower limit
--upper (-u) - Set the upper limit for the market size n (x-axis), inclusive, defaults to None, i.e. no upper limit
--rho (-r) - Accepts a list of values of the correlation coefficient to plot for, every value gets its own subplot, defaults to [1.0]
--pref-length (-k) - Accepts a list of values of the preference order length k to plot for, every k gets its own curve in the subplot for the same rho's, defaults to 10