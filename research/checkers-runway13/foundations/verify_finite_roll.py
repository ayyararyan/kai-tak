"""Independent quadrature checks for the exploratory finite-roll benchmark.

No historical/aircraft calibration. Python standard library only.
"""
import json
import math
from pathlib import Path

G = 9.80665


def solution(delta, speed, bank_cap, roll_rate):
    if not (delta >= 0 and speed > 0 and 0 < bank_cap < math.pi / 2 and roll_rate > 0):
        raise ValueError("Outside benchmark domain")
    critical = 2 * G / (speed * roll_rate) * math.log(1 / math.cos(bank_cap))
    if delta <= critical:
        peak = math.acos(math.exp(-speed * roll_rate * delta / (2 * G)))
        hold = 0.0
    else:
        peak = bank_cap
        hold = (delta - critical) * speed / (G * math.tan(bank_cap))
    return peak, hold, 2 * peak / roll_rate + hold


def simpson(f, a, b, n=20000):
    if a == b:
        return 0.0
    h = (b - a) / n
    return h / 3 * (f(a) + f(b) + 4 * sum(f(a + i*h) for i in range(1,n,2))
                    + 2 * sum(f(a + i*h) for i in range(2,n,2)))


def main():
    rows = []
    for deg, speed, bank, rate in [(47,70,25,5),(5,70,25,5),(47,70,25,2),
                                    (47,70,25,1000),(0,70,25,5),(90,90,30,3)]:
        delta, cap, p = map(math.radians, (deg,bank,rate))
        peak, hold, duration = solution(delta,speed,cap,p)
        ramp = peak/p
        # Independent numerical integration of heading ODE along actual bank ramps.
        numerical = simpson(lambda t:G/speed*math.tan(p*t),0,ramp)
        numerical += simpson(lambda t:G/speed*math.tan(peak),0,hold)
        numerical += simpson(lambda t:G/speed*math.tan(peak-p*t),0,ramp)
        assert abs(numerical-delta) < 1e-10
        instant = delta*speed/(G*math.tan(cap))
        assert duration >= instant-1e-12
        if duration:
            smaller = duration*0.999
            # Independent quadrature of universal pointwise envelope for a shorter time.
            half_area = simpson(lambda t:G/speed*math.tan(min(cap,p*t)),0,smaller/2)
            assert 2*half_area < delta
        rows.append(dict(heading_change_deg=deg,speed_m_s=speed,bank_cap_deg=bank,
                         roll_rate_deg_s=rate,peak_bank_deg=math.degrees(peak),
                         hold_s=hold,minimum_heading_time_s=duration,
                         instantaneous_bank_time_s=instant,
                         quadrature_error_rad=numerical-delta))
    # Continuity at triangular/trapezoidal switch.
    v,b,p = 70,math.radians(25),math.radians(5)
    critical = 2*G/(v*p)*math.log(1/math.cos(b))
    assert abs(solution(critical,v,b,p)[2]-2*b/p)<1e-12
    assert abs(solution(critical+1e-10,v,b,p)[2]-solution(critical-1e-10,v,b,p)[2])<1e-7
    # Constant descent keeps yaw rate but changes horizontal displacement/load demand.
    gamma = math.radians(-3)
    n=math.cos(gamma)/math.cos(b)
    assert abs(G*n*math.sin(b)/(v*math.cos(gamma))-G*math.tan(b)/v)<1e-14
    result = dict(status="passed",cases=rows,checks=["heading quadrature","shorter-time exclusion",
        "instantaneous-bank lower bound","branch continuity","steady-descent yaw identity"],
        scope="Synthetic mathematical checks only; no empirical/aircraft safety validation")
    destination=Path(__file__).with_name("verification_results.json")
    destination.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
