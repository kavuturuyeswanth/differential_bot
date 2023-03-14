import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration
#from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import xacro



def generate_launch_description():

	#check if we're told to use sim time
    #use_sim_time=LaunchConfiguration('use_sim_time')
    #use_ros2_control=LaunchConfiguration('use_ros2_control')
    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'differential_bot'
    file_subpath = 'description/differential_bot.urdf.xacro'


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    #robot_description_raw = Command(['xacro', xacro_file, 'use_ros2_control:=', use_ros2_control, 'sim_mode:=', use_sim_time])

    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True,
        'use_ros2_control': True}] # add other parameters here if required
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'dif_bot'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
    
    	#DeclareLaunchArgument(
    	#	'use_sim_time',
    	#	default_value='true',
    	#	description='Use sim time if true'),
    	#DeclareLaunchArgument(
    	#	'use_ros2_control',
    	#	default_value='true',
    	#	description='Use ros2_control if true'),
    	
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
    ])

