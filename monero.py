#!/usr/bin/env python3

constants = {
        "xdp1mkhs" : ("XMR/day for 1000000 KH/s", 95000),
        "hspw" : ("H/s per watt", 1.5),
        "watts" : ("Watts", 30),
        "dpkwh" : ("$/KWh", 0.11029),
        "dpx" : ("$/XMR", 20),
        "hps" : ("H/s", 50),
    }

def prompt(prompt_str, default):
    res = input(prompt_str + (" [%s]: " % default))
    if not res:
        res = default
    return res

def prompt_constant(const):
    return prompt(constants[const][0], constants[const][1])

if __name__=="__main__":
    # XMR/day for 1e6 KH/s
    xdp1mkhs = float(prompt_constant("xdp1mkhs"))

    # H/s per watt
    # hspw = prompt_constant("hspw")

    # watts
    watts = float(prompt_constant("watts"))

    # elec cost
    dpkwh = float(prompt_constant("dpkwh"))
    
    # currency conversion
    dpx = float(prompt_constant("dpx"))

    # hash rate
    hps = float(prompt_constant("hps"))

    # gain per second
    xd = hps * xdp1mkhs / 1e9
    xs = xd / 86400
    # xdphs = xdp1mkhs / 1e9
    # xsphs = xdphs / 86400
    # dps = hps * xsphs * dpx
    dps = xs * dpx
    dpd = xd * dpx

    # cost per second
    cpws = dpkwh / 3600 / 1000
    cps = watts * cpws
    cpd = watts * (24/1000) * dpkwh

    # profit
    pps = dps - cps
    ppd = pps * 86400

    # alt calculation
    xsphs2 = xdp1mkhs / (1e6 * 24)
    ppd2 = xsphs2 * dpx * hps - dpkwh * watts

    print()
    print("$gain/s: %s" % dps)
    print("$cost/s: %s" % cps)
    print("$/s: %s" % pps)
    print("%% return: %s" % (pps/cps * 100))
    print()
    print("$gain/d: %s" % dpd)
    print("$cost/d: %s" % cpd)
    print("$/d: %s" % ppd)





