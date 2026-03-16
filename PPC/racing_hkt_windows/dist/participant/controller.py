
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Path: list of waypoints [{"x": float, "y": float}, ...]
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"} 
# CmdFeedback: {"throttle", "steer"}         

# ─── CONTROLLER ───────────────────────────────────────────────────────────────
import numpy as np

index =1
offset=4
def steering(path: list[dict], state: dict , target_index):
    global index
    global offset
    tot_cones = len(path)


    length_of_car = 2.6
    steer = 0.0

    car_x = state["x"]
    car_y = state["y"]
    car_yaw = state["yaw"]
    closest_idx = 0
    min_dist = float('inf') 
    for i, point in enumerate(path):
        dist = (point["x"] - car_x)**2 + (point["y"] - car_y)**2
        if dist < min_dist:
            min_dist = dist
            closest_idx = i

    target_idx = (closest_idx + offset) % len(path) 
    target = path[target_idx]
    dx = target["x"] - car_x
    dy = target["y"] - car_y
    target_angle = np.arctan2(dy, dx)
    steer = target_angle - car_yaw
    steer = (steer + np.pi) % (2 * np.pi) - np.pi

    return np.clip(steer, -0.5, 0.5)



def throttle_algorithm(target_speed, current_speed, dt):
    command = target_speed - current_speed
    k=2/target_speed




    
    
    # generate the output for throttle command
    throttle = 0
    brake = 0.0

    if command > 0:
        
        throttle = command*k
    elif command < 0:
      
        brake = -command*k
    return np.clip(throttle, 0.0, 1.0), np.clip(brake, 0.0, 1.0)


def control(
    path: list[dict],
    state: dict,
    cmd_feedback: dict,
    step: int,
) -> tuple[float, float, float]:
    """
    Generate throttle, steer, brake for the current timestep.
    Called every 50ms during simulation.

    Args:
        path:         Your planned path (waypoints)
        state:        Noisy vehicle state observation
                        x, y        : position (m)
                        yaw         : heading (rad)
                        vx, vy      : velocity in body frame (m/s)
                        yaw_rate    : (rad/s)
        cmd_feedback: Last applied command with noise
                        throttle, steer, brake
        step:         Current simulation timestep index

    Returns:
        throttle  : float in [0.0, 1.0]   — 0=none, 1=full
        steer     : float in [-0.5, 0.5]  — rad, neg=left
        brake     : float in [0.0, 1.0]   — 0=none, 1=full
    
    Note: throttle and brake cannot both be > 0 simultaneously.
    """
    throttle = 0.0
    steer    = 0.0
    brake = 0.0
   
    # TODO: implement your controller here
    
    prevsteer = cmd_feedback["steer"]
    steer = steering(path, state , index)
    # if(abs(steer-prevsteer)>1.0):
    #     steer=prevsteer
    if(abs(steer)<0.17):
        target_speed=80
        offset=9 
    elif(abs(steer)<0.36):
        target_speed=50
        offset=5
    else:
        target_speed=8.0
        offset=3
    global integral
    throttle, brake = throttle_algorithm(target_speed, state["vx"], 0.05)

    return throttle, steer, brake
