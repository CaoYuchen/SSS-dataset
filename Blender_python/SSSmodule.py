####### Modules of SSS dataset #######

def euler_to_rotation(euler):
    ex = euler[0]
    ey = euler[1]
    ez = euler[2]
    rx = np.array([[1,0,0],[0,np.cos(ex),-1*np.sin(ex)],[0,np.sin(ex),np.cos(ex)]])
    ry = np.array([[np.cos(ey),0,np.sin(ey)],[0,1,0],[-1*np.sin(ey),0,np.cos(ey)]])
    rz = np.array([[np.cos(ez),-1*np.sin(ez),0],[np.sin(ez),np.cos(ez),0],[0,0,1]])
    rotation = rz.dot(ry).dot(rx)
    return rotation

def quaternion_to_rotation(quat):
    w = quat[0]
    x = quat[1]
    y = quat[2]
    z = quat[3]
    rotation = np.array([
    [1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],
    [2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],
    [2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]
    ])
    return rotation

def rotation_to_quaternion(rotation):
    m00 = rotation[0][0]
    m01 = rotation[0][1]
    m02 = rotation[0][2]
    m10 = rotation[1][0]
    m11 = rotation[1][1]
    m12 = rotation[1][2]
    m20 = rotation[2][0]
    m21 = rotation[2][1]
    m22 = rotation[2][2]
    
    tr = m00 + m11 + m22
    if tr > 0: 
        S = math.sqrt(tr+1.0) * 2; # S=4*qw 
        qw = 0.25 * S;
        qx = (m21 - m12) / S;
        qy = (m02 - m20) / S; 
        qz = (m10 - m01) / S; 
    elif (m00 > m11)&(m00 > m22):
        S = math.sqrt(1.0 + m00 - m11 - m22) * 2; # S=4*qx 
        qw = (m21 - m12) / S;
        qx = 0.25 * S;
        qy = (m01 + m10) / S; 
        qz = (m02 + m20) / S; 
    elif m11 > m22:
        S = math.sqrt(1.0 + m11 - m00 - m22) * 2; # S=4*qy
        qw = (m02 - m20) / S;
        qx = (m01 + m10) / S; 
        qy = 0.25 * S;
        qz = (m12 + m21) / S; 
    else:
        S = math.sqrt(1.0 + m22 - m00 - m11) * 2; # S=4*qz
        qw = (m10 - m01) / S;
        qx = (m02 + m20) / S;
        qy = (m12 + m21) / S;
        qz = 0.25 * S;
    
    quaternion = np.array([qw,qx,qy,qz])
    return quaternion

def angularVelocity(Rprev,Rlater,step):
    A = Rlater.dot(np.transpose(Rprev))
    W = 1/(2*step)*(A-np.transpose(A))
    angVel = np.array([-1*W[1][2],W[0][2],-1*W[0][1]])
    return angVel

# Simple method for approximation angular velocity
def angularVelocity2(Rprev,Rlater,step):
    A = Rlater.dot(np.linalg.inv(Rprev))
    W = (A-np.eye(3))/step
    angVel = np.array([-1*W[1][2],W[0][2],-1*W[0][1]])
    return angVel

def getRotation(mat):
    R_rectify = mathutils.Matrix(((1,0,0),(0,-1,0),(0,0,-1)))
    orien = mat.to_quaternion()
    orien = orien.to_matrix() @ R_rectify
    orien = orien.to_quaternion()
    return orien


# function to retrieve R and t
def getPose(i):
    scn.frame_set(i)
    mat = scn.camera.matrix_world
    t = mat.to_translation()
    quat = getRotation(mat)
    R = quat.to_matrix()
    return [R,t]