before<-read.csv(file.choose(),head=TRUE, sep=",")
# /Users/shantanu/Dropbox/Stern/BAC/2015-2016/r trading workshop/dataone.csv
actual<-read.csv(file.choose(),head=TRUE, sep=",")
#/Users/shantanu/Dropbox/Stern/BAC/2015-2016/r trading workshop/actual.csv
data<-read.csv(file.choose(), head=TRUE, sep=",")
#/Users/shantanu/Dropbox/Stern/BAC/2015-2016/r trading workshop/data.csv

date <- data$date
time <- 1:length(date)
cny <- data$cny
plot(time, cny, main="CNY over Time",type="l", xlab="time", ylab="cny)")


cny <- before$cny
dxy <- before$dxy
plot(dxy, cny, main="CNY v. DXY before", xlab="dxy", ylab="cny")


cny2 <- datatwo$cny
dxy2 <- datatwo$dxy
plot(dxy2, cny2, xlab="dxy2", ylab="cny2")


fit1 <- lm(cny1 ~ dxy1)
summary(fit1)
#Adjusted R-squared:  0.5816
#dope ass plots

#######################################################
#ts model below
library("forecast")

plot(time, cny, type="l", xlab="time", ylab="cny)")

log.cny<-log(cny)

diff.cny <- c(NA, diff(log.cny))

plot(time , diff.cny, type="l", xlab="time", ylab="diff log cny")

Acf(diff.cny)
Pacf(diff.cny)

diff2.cny <- c(NA, diff(diff.cny))

Acf(diff2.cny)
Pacf(diff2.cny)

diff3.cny <- c(NA, diff(diff2.cny))

Acf(diff3.cny)
Pacf(diff3.cny)


d <- 2 #dif is two
dataset<-diff.cny #dataset is one less diffrence than the actual fitting
# data set is now diff once the reg log data

# choose p, q with AICc
for (include.constant in c(FALSE,TRUE)) {
    for (p in 0:2) {
        for (q in 0:2) {
            # work-around bug in R by manually differencing
            fit <- Arima(diff(dataset), c(p,0,q), # this is twice difference the reg log data,
            # so technically we are testing 020,021,022, 120, etc.etc.
                         include.constant=include.constant, method="ML") #this is using second difference effectively
             cat("ARIMA",
                 "(", p, ",", d, ",", q, ")",
                 "(constant=", include.constant, ")",
                 " : ", fit$aicc, "\n", sep="")
        }
    }
}

#best output ARIMA(0,2,2)(constant=FALSE) : -2811.09

fit<- Arima(diff(dataset), c(0,0,2))
plot(forecast(fit, h=5, level=95), col=2)

