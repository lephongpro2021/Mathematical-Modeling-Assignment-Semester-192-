library(MultiBD)

Eyam <- read.csv("JapanCovid19.csv")
printsample_size <- 177

loglik_sir <- function(param, data) {
  alpha <- exp(param[1]) # Rates must be non-negative
  beta <- exp(param[2])
  # Set-up SIR model
  drates1 <- function(a, b) { 0 }
  brates2 <- function(a, b) { 0 }
  drates2 <- function(a, b) { alpha * b }
  trans12 <- function(a, b) { beta * a * b }
  sum(sapply(1:(nrow(data) - 1), # Sum across all time steps k
             function(k) {
               log(
                 dbd_prob( # Compute the transition probability matrix
                   t = data$time[k + 1] - data$time[k], # Time increment
                   a0 = data$S[k], b0 = data$I[k], # From: S(t_k), I(t_k)
                   drates1, brates2, drates2, trans12,
                   a = data$S[k + 1], B = data$S[k] + data$I[k] - data$S[k + 1],
                   computeMode = 4, nblocks = 80 # Compute using 4 threads
                 )[1, data$I[k + 1] + 1] # To: S(t_(k+1)), I(t_(k+1))
               )
             }))
}

logprior <- function(param) {
  log_alpha <- param[1]
  log_beta <- param[2]
  dnorm(log_alpha, mean = 0, sd = 100, log = TRUE) +
    dnorm(log_beta, mean = 0, sd = 100, log = TRUE)
}

library(MCMCpack)

alpha0 <- 3.39
beta0 <- 0.0212

post_sample <- MCMCmetrop1R(fun = function(param) { loglik_sir(param, Eyam) + logprior(param) },
                            theta.init = log(c(alpha0, beta0)),
                            mcmc = 177, burnin = 50)


plot(as.vector(post_sample[,1]), type = "l", xlab = "Iteration", ylab = expression(log(alpha)))

plot(as.vector(post_sample[,2]), type = "l", xlab = "Iteration", ylab = expression(log(beta)))


R_0 <- 0 
for(i in 1:8){
   R_0 <- R_0 + exp(loglik_sir(c(post_sample[i,1], post_sample[i,2]), Eyam))*(exp(post_sample[i,1])/exp(post_sample[i,2]))
}

print(R_0)
