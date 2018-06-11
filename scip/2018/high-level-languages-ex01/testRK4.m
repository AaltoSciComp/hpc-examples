function testRK4
    t = 0:0.1:10;
    y = 0.0625.*(t.^2+4).^2;
    [trk4, yrk4] = RK4(t);
    fprintf('Time\t\tExactVal\tRK4Val\t\tRK4Error\n')
    for k = 1:10:length(t)
        fprintf('%.f\t\t%7.3f\t\t%7.3f\t\t%7.3g\n', t(k), y(k), ...
            yrk4(k), abs(y(k)-yrk4(k)))
    end
end
 
function [t, y] = RK4(t)
    dydt = @(tVal,yVal)tVal*sqrt(yVal);
    y = zeros(size(t));
    y(1) = 1;
    for k = 1:length(t)-1
        dt = t(k+1)-t(k);
        dy1 = dt*dydt(t(k), y(k));
        dy2 = dt*dydt(t(k)+0.5*dt, y(k)+0.5*dy1);
        dy3 = dt*dydt(t(k)+0.5*dt, y(k)+0.5*dy2);
        dy4 = dt*dydt(t(k)+dt, y(k)+dy3);
        y(k+1) = y(k)+(dy1+2*dy2+2*dy3+dy4)/6;
    end
end
