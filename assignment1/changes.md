# Changes applied to the agent
- Added dynamic environment creation at every execution, which adds random walls and randomizes the position of the points
- The agent now visits all points in order of which is closest to it as the time of collection of a point. If it did not reach a point until the timeout, it will continue to the next closest point
- Fixed some bugs in plotting