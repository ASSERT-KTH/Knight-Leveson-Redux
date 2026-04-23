5. MODEL OF INDEPENDENCE
Separate versions of a program may fail on the same input even if they fail independently. Indeed, if
they did not, their failures would be dependent. We base our probabilistic model for this experiment on the
statistical definition of independence:
Two events, A and B, are independent if the conditional probability of A occurring given that B
has occurred is the same as the probability of A occurring, and vice versa. That is pr(A|B) =
pr(A) and pr(B|A) = pr(B). Intuitively, A and B are independent if knowledge of the occurrence
of A in no way influences the occurrence of B, and vice versa.
The null hypothesis that we wish to test is derived from this statement.
By examining the faults (i.e. the flaws in the program logic) that have been revealed by testing, we
could determine whether any set of programs contain correlated faults. For this experiment we intend to do
that as part of a more extensive analysis. However, from an operational viewpoint, it does not matter why
programs fail on the same input, it merely matters that they do. Thus in examining the hypothesis of
independence, we examine the observed behavior of the programs during execution. In this paper, our
analysis of the hypothesis of independence is based on the results of the tests that have been carried out
with no evaluation of the faults in the programs’ source text.
For any given program, we assume that the probability of failure on each test case is the same. This
is reasonable since prior to testing we had no knowledge of the presence of any faults, and all test cases
were generated randomly. If the programs fail independently, then, given the individual probabilities of
failure p1, p2, ..., pN for N versions, the probability that there are no failures on a given test case is:
P0 = (1 − p1)(1 − p2). . . (1 − pN )
The probability that exactly one version fails on a given test case is:
P1 = [(P0p1) / (1 − p1)] + [(P0 p2) / (1 − p2)] + . . . + [(P0 pN) / (1 − pN)]
Finally, the probability that more than one of the N versions fails on any particular test case is:
Pmore = 1 − P0 − P1
If a total of n test cases are executed, let K be the number of times two or more versions fail on the
same input data. Under the hypothesis of independent failures, the quantity K has a binomial distribution
with parameter Pmore. Thus:
P(K = x) = \binom{n}{k} (Pmore)^x (1 − Pmore)^(n−x)
where  \binom{n}{k} = n! / x!(n − x)!
Since the value of n is sufficiently large [16], a normal approximation to this binomial distribution
can be used. If this is done, the quantity:
z = (K − nPmore) / [(nPmore(1 − Pmore))^(1/2)]
has a distribution that is closely approximated by the standardized normal distribution.
For this experiment, our null hypothesis is that the above is a correct model of the data. We can
estimate the quantity Pmore from the observed probabilities of failure shown in table 1. There were twenty
seven versions (i.e. N = 27), one million tests were executed (i.e. n = 1,000,000), and the number of tests in
which more than one version failed was 1255 (i.e. K = 1255). With these parameters, the statistic z has the
value 100.51. This is greater than 2.33 which is the 99% point in the the standard normal distribution, and
so we reject the null hypothesis with a confidence level of 99%. We conclude that the model does not hold.
However, clearly the only potential problem with the model is that it is derived from the assumption of
independent failures. Thus, we reject this assumption.