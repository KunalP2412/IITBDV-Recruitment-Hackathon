
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Cone: {"x": float, "y": float, "side": "left" | "right", "index": int}
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"}  
# CmdFeedback: {"throttle", "steer"}        

# ─── PLANNER ──────────────────────────────────────────────────────────────────
import numpy as np

def plan(cones: list[dict]) -> list[dict]:
    """
    Generate a path from the cone layout.
    Called ONCE before the simulation starts.

    Args:
        cones: List of cone dicts with keys x, y, side ("left"/"right"), index

    Returns:
        path: List of waypoints [{"x": float, "y": float}, ...]
              Ordered from start to finish.
    
    Tip: Try midline interpolation between matched left/right cones.
         You can also compute a curvature-optimised racing line.
    """
    path = []
    # TODO: implement your path planning here
    blue = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "left"])
    yellow = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "right"])

    # implement a planning algorithm to generate a path from the blue and yellow cones
    mid = (blue + yellow)/2
    dmid=[]
    for i in range(len(mid)-1):
        pt = (mid[i]+mid[i+1])/2
        dmid.append(mid[i])
        dmid.append(pt)
    dmid.append(mid[-1])
    racingline=np.array(mid)
    pull=2
    for _ in range(pull):
        for i in range(1, len(racingline) -1):
            racingline[i]=(racingline[i-1]+racingline[i]+racingline[i+1])/3
    for i in range(0,len(racingline)):
        d= np.linalg.norm(racingline[i]-yellow[i])
        if(d<0.8):
            vector = (blue[i]-yellow[i])/(np.linalg.norm(blue[i]-yellow[i]))
            racingline[i]=racingline[i]+ vector*0.5
        

    path = [ {"x":float(pt[0]) , "y":float(pt[1])} for pt in racingline]

    return path

