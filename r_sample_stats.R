

set.seed(4)
library(nimble)

#Using the Metropolis-Hastings algorithm to estimate the Cauchy distribution using the exponential distribution.

m = 20000
chain = xstar = rdexp(1)

u = runif(m)

for(i in 2:m){
  xt = xstar
  xstar = rdexp(1)
  mh = dcauchy(xstar)*ddexp(xt)/dcauchy(xt)/ddexp(xstar)
  
  if(u[i] < mh){chain[i] = xstar}
  else{chain[i] = xstar = xt}
}

vec = seq(-7,7,by = .01)

hist(chain, freq = F, ylim = c(0,.37))
lines(vec, dcauchy(vec), col = "red", lwd = 2)

sample = qcauchy(seq(0.001,0.999,by = .001))

summary(chain)
summary(sample)



#Using the Metropolis-Hastings algorithm to estimate the mean of the standard normal distribution with varying levels of acceptance-rejection

a = c(.05, 1, 10)

m = 20000

chain = matrix(10, ncol = length(a), nrow = m)
u = matrix(runif(length(a) * m), nrow = m)

for(j in 1:length(a)){
  xstar = 10
  for(i in 2:m){
    xt = xstar
    xstar = runif(1, xt-a[j], xt+a[j])
    mh = dnorm(xstar)/dnorm(xt)
    
    if(u[i,j] < mh) {chain[i,j] = xstar}
    else {chain[i,j] = xstar = xt}
  }
}

plot(chain[,1], main = "a = .05", type = "l")
mean(chain[,1])
var(chain[,1])

plot(chain[,2], main = "a = 1", type = "l")
mean(chain[,2])
var(chain[,2])

plot(chain[,3], main = "a = 10", type = "l")
mean(chain[,3])
var(chain[,3])


#As a increases, the mean comes closer to the true mean of a N(0, 1) distribution (0), and the variance decreases. Also, as $a$ increases, the distributions approach the target distribution much faster than the ones with lower $a$ values.




