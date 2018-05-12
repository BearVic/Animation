
a) the functionality of my work:
  
  I use a group of joints with hierarchy, connecting with a group of bones, to implement a rotation and forward kinematics system. Player uses "1~5" in the keyboard to select a joint, "qweasd" to control the rotations of the joint with substructure, and "m" to restore the joints and cube. Some values will show on the screen. 

b) How did I implement the homework:

  I use an array of GameObject to initialize the five joints and cube. The current index of joint would be recorded. Transformation matrix would be calculated by the local rotation of the joints(Rotation matrix) and the length of the bones(Translation matrix) every frame within the function Update(). The global position of the cube is obtained by multiplying the transformation matrix and vector(0,0,0). Euler angles and quaternion are extract from the transformation matrix.

c) Problems & Solutions:

  P1. I can't find out the right position of the cube.
    S: Use transform.localrotation instead of transform.rotation.

  P2. The output results can't display in screen in realtime.
    S: During the calculation of transformation matrix in the for loop, I did not multiply the localrotation of the current joint to the matrix. (I still don't know why I should do that.)

  P3. How to extract the euler angles and quaternion from the transformation matrix.
    S: I asked my classmates.

  Finally, I really want to say that, sometimes little bug would make me crazy for the whole day.




