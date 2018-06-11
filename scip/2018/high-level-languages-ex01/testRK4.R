rk4 <- function(f, x0, y0, x1, n) {
    vx <- double(n + 1)
    vy <- double(n + 1)
    vx[1] <- x <- x0
    vy[1] <- y <- y0
    h <- (x1 - x0)/n
    for(i in 1:n) {
        k1 <- h*f(x, y)
        k2 <- h*f(x + 0.5*h, y + 0.5*k1)
        k3 <- h*f(x + 0.5*h, y + 0.5*k2)
        k4 <- h*f(x + h, y + k3)
        vx[i + 1] <- x <- x0 + i*h
        vy[i + 1] <- y <- y + (k1 + k2 + k2 + k3 + k3 + k4)/6
    }
    cbind(vx, vy)
}
 
sol <- rk4(function(x, y) x*sqrt(y), 0, 1, 10, 100)
cbind(sol, sol[, 2] - (4 + sol[, 1]^2)^2/16)[seq(1, 101, 10), ]
