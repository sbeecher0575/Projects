# Fun with Plots

library(tidyverse)



# USING GGPLOT2

bikes <- read_csv("https://docs.google.com/spreadsheets/d/1DK8ZSmIgvZ1eVVF33NCNLyLxvYFA8t1jeGrJppaBDpI/gviz/tq?tqx=out:csv")

x_vec <- seq(min(bikes$TAVG), max(bikes$TAVG), length.out = length(bikes$TAVG))

bikes$SNOW_B <- as.factor(ifelse(bikes$SNOW > 0, 'Yes', 'No'))

temp_snow_model <- lm(number_rides ~ TAVG * SNOW_B, data = bikes)

y_snow <- coef(temp_snow_model)[1] + coef(temp_snow_model)[2] * x_vec + coef(temp_snow_model)[3] * 1 + coef(temp_snow_model)[4] * x_vec * 1
y_no_snow <- coef(temp_snow_model)[1] + coef(temp_snow_model)[2] * x_vec + coef(temp_snow_model)[3] * 0 + coef(temp_snow_model)[4] * x_vec * 0

ggplot(bikes,
       aes(x=TAVG, y=number_rides)) + 
  geom_point(aes(color = SNOW_B)) + 
  geom_line(aes(x = x_vec, y = y_snow)) + 
  geom_line(aes(x = x_vec, y = y_no_snow)) + 
  labs(title = "Number of Rides per day vs. Average Temperature", x = "Average Temperature (°F)", y = 'Number of Rides', color = "Snow") +
  theme(plot.title = element_text(hjust = 0.5))




#USING RANDOMLY GENERATED NUMBERS TO EXPLORE THE X^2 DISTRIBUTION

set.seed(6789)
plot(density(rchisq(8000, 1)), type = "l")
lines(density(rchisq(8000,2)), col = "green")
lines(density(rchisq(8000,3)), col = "red")
lines(density(rchisq(8000,4)), col = "blue")
lines(density(rchisq(8000,5)), col = "goldenrod")
lines(density(rchisq(8000,6)), col = "purple")

legend("topright", legend = c("df=1", "df=2", "df=3", "df=4", "df=5", "df=6"), 
       col = c("black", "green", "red", "blue", "goldenrod", "purple"), lwd = 2)


plot(ecdf(rchisq(8000, 1)))
lines(ecdf(rchisq(8000,2)), col = "green")
lines(ecdf(rchisq(8000,3)), col = "red")
lines(ecdf(rchisq(8000,4)), col = "blue")
lines(ecdf(rchisq(8000,5)), col = "goldenrod")
lines(ecdf(rchisq(8000,6)), col = "purple")

legend("bottomright", legend = c("df=1", "df=2", "df=3", "df=4", "df=5", "df=6"), 
       col = c("black", "green", "red", "blue", "goldenrod", "purple"), lwd = 2)




# 3D PLOTTING

f <- function(x,y) {
  z <- (1/(4*pi)) * exp(-.75 * (x^2 + y^2))
  + 1/(2*pi)*exp(-.5*((x+4)^2+(y-2)^2))
  return(z)
}

y <- x <- seq(-3, 3, length= 50)
z <- outer(x, y, f)

persp(x, y, z, theta = 45, phi = 30, expand = 0.6,
      ltheta = 120, shade = 0.75, ticktype = "detailed",
      xlab = "X", ylab = "Y", zlab = "f(x, y)")

persp(x, y, z, theta = 150, phi = 60, expand = 0.6,
      ltheta = 120, shade = 0.75, ticktype = "detailed",
      xlab = "X", ylab = "Y", zlab = "f(x, y)")




  
