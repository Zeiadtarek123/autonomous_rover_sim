import os

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():

    pkg_share = get_package_share_directory('my_robot_description')
    models_path = os.path.join(pkg_share, 'models')

    # ── Tell Gazebo where to find the pole models ──────────────────
    models_path = os.path.join(pkg_share, 'models')
    os.environ['IGN_GAZEBO_RESOURCE_PATH'] = \
        models_path + ':' + os.environ.get('IGN_GAZEBO_RESOURCE_PATH', '')

    world_file = os.path.join(pkg_share, 'worlds', 'aruco_world.world')

    package_name='my_robot_description' 

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                )]), launch_arguments={'gz_args': '-r /home/roar/roar_ws/src/my_robot_description/worlds/aruco_world.world'}.items()
             )

    # Run the spawner node from the package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'my_bot',
                   '-z', '0.1'],
        output='screen'
    )

    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    name='gz_ros_bridge',
    arguments=[
        # Camera image — exact ign topic name
        '/camera/image_raw@sensor_msgs/msg/Image[ignition.msgs.Image',

        # Camera info — exact ign topic name  
        '/camera/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo',

        # IMU — exact ign topic name from ign topic -l
        '/world/aruco_world/model/my_bot/link/base_link/sensor/imu_sensor/imu'
        '@sensor_msgs/msg/Imu[ignition.msgs.IMU',
    ],
    remappings=[
        # Camera image: ign name → what aruco_node expects
        ('/camera/image_raw', '/image_raw'),

        # Camera info: ign name → what aruco_node expects
        ('/camera/camera_info', '/camera/color/camera_info'),

        # IMU: long ign name → standard ROS 2 name
        ('/world/aruco_world/model/my_bot/link/base_link/sensor/imu_sensor/imu',
         '/imu/data'),
    ],
    output='screen',
)

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        bridge,
    ])