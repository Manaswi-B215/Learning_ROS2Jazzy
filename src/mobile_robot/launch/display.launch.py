import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():

    pkg_path = get_package_share_directory('mobile_robot')
    urdf_file = os.path.join(pkg_path, 'urdf', 'mobile_robot.urdf')
    rviz_config = os.path.join(pkg_path, 'rviz', 'robot.rviz')

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['cat ', urdf_file]),
                     'use_sim_time': True}],
        output='screen'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'),
                         'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': '-r --headless-rendering ' + os.path.join(
            get_package_share_directory('mobile_robot'),
            'worlds', 'maze.sdf')}.items()
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', os.path.join(pkg_path, 'urdf', 'mobile_robot.sdf'),
            '-name', 'mobile_robot',
            '-x', '-3.0',
            '-y', '-4.0',
            '-z', '0.1',
        ],
        output='screen'
    )
    # spawn_robot = Node(
    #     package='ros_gz_sim',
    #     executable='create',
    #     arguments=[
    #         '-topic', 'robot_description',
    #         '-name', 'mobile_robot',
    #         '-x', '-3.0',
    #         '-y', '-4.0',
    #         '-z', '0.1',
    #     ],
    #     output='screen'
    # )

    # Yeh bridge Gazebo aur ROS 2 ke beech asli data pass karega
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        rsp_node,
        gazebo,
        spawn_robot,
        bridge,
        rviz_node
    ])
