"""
Motion Bridge - Control NAO robot movement and joints
Supports both LAN and WiFi connections
Compatible with NAOqi 2.8.6.23 (Python 2.7)
"""

import time


class MotionBridge(object):
    """Clean interface to robot motion control"""

    # Standard postures available on NAO
    POSTURES = {
        'stand': 'Stand',
        'sit': 'Sit',
        'crouch': 'Crouch',
        'belly': 'Belly',
        'back': 'Back',
        'lying_belly': 'LyingBelly',
        'lying_back': 'LyingBack'
    }

    # All 22 joints on NAO V4
    JOINTS = [
        # Head (2)
        'HeadYaw', 'HeadPitch',
        # Left arm (5)
        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw',
        # Right arm (5)
        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw',
        # Left leg (6)
        'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
        # Right leg (6)
        'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'
    ]

    def __init__(self, ip='169.254.175.171', port=9559):
        """Initialize motion bridge

        Args:
            ip: Robot IP (LAN or WiFi)
            port: NAOqi port (default 9559)
        """
        self.ip = ip
        self.port = port
        self.motion = None
        self.posture_proxy = None

        self._connect()

    def _connect(self):
        """Connect to robot NAOqi"""
        try:
            from naoqi import ALProxy

            self.motion = ALProxy('ALMotion', self.ip, self.port)
            self.posture_proxy = ALProxy('ALRobotPosture', self.ip, self.port)

            # Verify connection
            self.motion.getRobotConfig()

        except ImportError:
            raise ImportError("NAOqi SDK not found. Activate venv_py27.")
        except Exception as e:
            raise Exception("Failed to connect to robot at {}:{} - {}".format(
                self.ip, self.port, str(e)))

    # ========== POSTURE CONTROL ==========

    def stand(self):
        """Move robot to standing posture"""
        return self._set_posture('Stand')

    def sit(self):
        """Move robot to sitting posture"""
        return self._set_posture('Sit')

    def crouch(self):
        """Move robot to crouching posture"""
        return self._set_posture('Crouch')

    def lie_on_belly(self):
        """Move robot to lying on belly posture"""
        return self._set_posture('LyingBelly')

    def lie_on_back(self):
        """Move robot to lying on back posture"""
        return self._set_posture('LyingBack')

    def _set_posture(self, posture_name):
        """Set robot posture

        Args:
            posture_name: Name of posture (Stand, Sit, Crouch, etc.)

        Returns:
            True if successful
        """
        try:
            result = self.posture_proxy.goToPosture(posture_name, 0.5)
            return result
        except Exception as e:
            raise Exception("Failed to set posture {}: {}".format(posture_name, str(e)))

    # ========== WALKING ==========

    def walk_forward(self, distance=0.5, speed=0.5):
        """Walk forward

        Args:
            distance: Distance in meters (default 0.5)
            speed: Speed 0-1 (default 0.5)
        """
        return self._walk(x=distance, y=0, theta=0, speed=speed)

    def walk_backward(self, distance=0.5, speed=0.5):
        """Walk backward

        Args:
            distance: Distance in meters (default 0.5)
            speed: Speed 0-1 (default 0.5)
        """
        return self._walk(x=-distance, y=0, theta=0, speed=speed)

    def walk_left(self, distance=0.3, speed=0.5):
        """Walk left

        Args:
            distance: Distance in meters (default 0.3)
            speed: Speed 0-1 (default 0.5)
        """
        return self._walk(x=0, y=distance, theta=0, speed=speed)

    def walk_right(self, distance=0.3, speed=0.5):
        """Walk right

        Args:
            distance: Distance in meters (default 0.3)
            speed: Speed 0-1 (default 0.5)
        """
        return self._walk(x=0, y=-distance, theta=0, speed=speed)

    def turn_left(self, angle=0.5, speed=0.5):
        """Turn left (counterclockwise)

        Args:
            angle: Rotation angle in radians (default 0.5 rad ~= 29 degrees)
            speed: Speed 0-1 (default 0.5)
        """
        return self._walk(x=0, y=0, theta=angle, speed=speed)

    def turn_right(self, angle=0.5, speed=0.5):
        """Turn right (clockwise)

        Args:
            angle: Rotation angle in radians (default 0.5 rad ~= 29 degrees)
            speed: Speed 0-1 (default 0.5)
        """
        return self._walk(x=0, y=0, theta=-angle, speed=speed)

    def _walk(self, x=0, y=0, theta=0, speed=0.5):
        """Internal walk command

        Args:
            x: Forward distance (meters)
            y: Lateral distance (meters)
            theta: Rotation (radians)
            speed: Walking speed 0-1

        Returns:
            True if successful
        """
        try:
            # Ensure robot is standing
            if not self._is_moving():
                self.stand()
                time.sleep(0.5)

            # Move robot
            self.motion.moveToward(x * speed, y * speed, theta * speed)

            return True
        except Exception as e:
            raise Exception("Walk failed: {}".format(str(e)))

    def stop(self):
        """Stop robot movement immediately"""
        try:
            self.motion.stopMove()
            return True
        except Exception as e:
            raise Exception("Failed to stop: {}".format(str(e)))

    # ========== JOINT CONTROL ==========

    def set_joint_angle(self, joint_name, angle_rad, speed=0.1):
        """Set a single joint to target angle

        Args:
            joint_name: Name of joint (e.g., 'HeadYaw')
            angle_rad: Target angle in radians
            speed: Motion speed 0-1 (default 0.1)
        """
        try:
            self.motion.setStiffnesses([joint_name], [1.0])
            self.motion.angleInterpolation(
                [joint_name],
                [angle_rad],
                [1.0 / speed] if speed > 0 else [1.0],
                True
            )
            return True
        except Exception as e:
            raise Exception("Failed to set joint {}: {}".format(joint_name, str(e)))

    def set_joint_angles(self, joint_angles, speed=0.1):
        """Set multiple joints

        Args:
            joint_angles: Dict of {joint_name: angle_rad}
            speed: Motion speed 0-1

        Example:
            bridge.set_joint_angles({
                'HeadYaw': 0.5,
                'HeadPitch': -0.3
            })
        """
        try:
            joint_names = list(joint_angles.keys())
            angles = list(joint_angles.values())

            # Enable stiffness for all joints
            self.motion.setStiffnesses(joint_names, [1.0] * len(joint_names))

            # Move to angles
            self.motion.angleInterpolation(
                joint_names,
                angles,
                [1.0 / speed] * len(joint_names) if speed > 0 else [1.0] * len(joint_names),
                True
            )
            return True
        except Exception as e:
            raise Exception("Failed to set angles: {}".format(str(e)))

    def get_joint_angles(self):
        """Get current joint angles

        Returns:
            Dict of {joint_name: angle_rad}
        """
        try:
            angles = self.motion.getAngles(self.JOINTS, False)
            return dict(zip(self.JOINTS, angles))
        except Exception as e:
            raise Exception("Failed to get joint angles: {}".format(str(e)))

    # ========== STIFFNESS CONTROL ==========

    def set_stiffness(self, value=1.0):
        """Set stiffness for all joints

        Args:
            value: Stiffness 0-1 (0=relaxed, 1=stiff)
        """
        try:
            self.motion.setStiffnesses(self.JOINTS, [value] * len(self.JOINTS))
            return True
        except Exception as e:
            raise Exception("Failed to set stiffness: {}".format(str(e)))

    def relax(self):
        """Relax all joints (stiffness = 0)"""
        return self.set_stiffness(0.0)

    def stiffen(self):
        """Stiffen all joints (stiffness = 1)"""
        return self.set_stiffness(1.0)

    def get_stiffness(self):
        """Get current stiffness of all joints

        Returns:
            Dict of {joint_name: stiffness_value}
        """
        try:
            stiffness = self.motion.getStiffnesses(self.JOINTS)
            return dict(zip(self.JOINTS, stiffness))
        except Exception as e:
            raise Exception("Failed to get stiffness: {}".format(str(e)))

    # ========== STATUS & UTILITIES ==========

    def _is_moving(self):
        """Check if robot is currently moving"""
        try:
            return self.motion.isMoving()
        except Exception:
            return False

    def is_moving(self):
        """Check if robot is moving"""
        return self._is_moving()

    def get_robot_config(self):
        """Get robot configuration info"""
        try:
            return self.motion.getRobotConfig()
        except Exception as e:
            raise Exception("Failed to get config: {}".format(str(e)))

    def get_robot_status(self):
        """Get detailed robot status"""
        status = {
            'ip': self.ip,
            'port': self.port,
            'moving': self.is_moving(),
            'joints': self.get_joint_angles(),
            'stiffness': self.get_stiffness()
        }
        return status

    def __repr__(self):
        return "MotionBridge(ip='{}', port={})".format(self.ip, self.port)
