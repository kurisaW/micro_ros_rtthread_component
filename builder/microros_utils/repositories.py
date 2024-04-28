import os, sys
import json
import xml.etree.ElementTree as xml_parser
import time
import sys

from .utils import run_cmd

class Package:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.ignored = False

    def ignore(self):
        self.ignored = True
        ignore_path = self.path + '/COLCON_IGNORE'
        with open(ignore_path, 'a'):
            os.utime(ignore_path, None)

class Repository:
    def __init__(self, name, url, distribution, branch=None):
        self.name = name
        self.url = url
        self.distribution = distribution
        self.branch = distribution if branch is None else branch
        self.path = None

    def clone(self, folder):
        self.path = folder + "\\" + self.name
        attempts = 0
        # Download reconnect time, 1s by default
        retry_delay = 1
        # The number of repository redownloads that fail is defined here
        max_attempts = 3

        command = "git clone -b {} {} {}".format(self.branch, self.url, self.path)
        result, stderr = run_cmd(command, capture_output=True)

        if result == 0:
            # Download successfully, exit the loop
            return
        else:
            while attempts < max_attempts:
                attempts += 1
                print("{} clone failed! Retrying...")
                command = "git clone -b {} {} {}".format(self.branch, self.url, self.path)
                result, stderr = run_cmd(command, capture_output=True)
                # Wait a while and try again
                time.sleep(retry_delay)

            # If all attempts fail, print an error message and exit the script
            print("Max attempts reached. Failed to clone {} after {} attempts.".format(self.name, max_attempts))
            sys.exit(1)

    def get_packages(self):
        packages = []
        if os.path.exists(self.path + '/package.xml'):
            packages.append(Package(self.name, self.path))
        else:
            for root, dirs, files in os.walk(self.path):
                path = root.split(os.sep)
                if 'package.xml' in files:
                    package_name = Repository.get_package_name_from_package_xml(os.path.join(root, 'package.xml'))
                    package_path = os.path.join(os.getcwd(), root)
                    packages.append(Package(package_name, package_path))
                elif 'colcon.pkg' in files:
                    package_name = Repository.get_package_name_from_colcon_pkg(os.path.join(root, 'colcon.pkg'))
                    package_path = os.path.join(os.getcwd(), root)
                    packages.append(Package(package_name, package_path))
        return packages

    @classmethod
    def get_package_name_from_package_xml(cls, xml_file):
        root_node = xml_parser.parse(xml_file).getroot()
        name_node = root_node.find('name')
        if name_node is not None:
            return name_node.text
        return None

    @classmethod
    def get_package_name_from_colcon_pkg(cls, colcon_pkg):
        with open(colcon_pkg, 'r') as f:
            content = json.load(f)
            if content['name']:
                return content['name']
            return None

class Sources:
    dev_environments = {
         'humble': [
            Repository("ament_cmake", "https://github.com/ament/ament_cmake", "humble"),
            Repository("ament_lint", "https://github.com/ament/ament_lint", "humble"),
            Repository("ament_package", "https://github.com/ament/ament_package", "humble"),
            Repository("googletest", "https://github.com/ament/googletest", "humble"),
            Repository("ament_cmake_ros", "https://github.com/ros2/ament_cmake_ros", "humble"),
            Repository("ament_index", "https://github.com/ament/ament_index", "humble")
        ],
        'foxy': [
            Repository("ament_cmake", "https://github.com/ament/ament_cmake", "foxy"),
            Repository("ament_lint", "https://github.com/ament/ament_lint", "foxy"),
            Repository("ament_package", "https://github.com/ament/ament_package", "foxy"),
            Repository("googletest", "https://github.com/ament/googletest", "foxy"),
            Repository("ament_cmake_ros", "https://github.com/ros2/ament_cmake_ros", "foxy"),
            Repository("ament_index", "https://github.com/ament/ament_index", "foxy")
        ]
    }

    mcu_environments = {
        'humble': [
            Repository("micro-CDR", "https://github.com/eProsima/micro-CDR", "humble", "ros2"),
            Repository("Micro-XRCE-DDS-Client", "https://github.com/eProsima/Micro-XRCE-DDS-Client", "humble", "ros2"),
            Repository("rcl", "https://github.com/micro-ROS/rcl", "humble"),
            Repository("rclc", "https://github.com/ros2/rclc", "humble"),
            Repository("micro_ros_utilities", "https://github.com/micro-ROS/micro_ros_utilities", "humble"),
            Repository("rcutils", "https://github.com/micro-ROS/rcutils", "humble"),
            Repository("micro_ros_msgs", "https://github.com/micro-ROS/micro_ros_msgs", "humble"),
            Repository("rmw-microxrcedds", "https://github.com/micro-ROS/rmw-microxrcedds", "humble"),
            Repository("rosidl_typesupport", "https://github.com/micro-ROS/rosidl_typesupport", "humble"),
            Repository("rosidl_typesupport_microxrcedds", "https://github.com/micro-ROS/rosidl_typesupport_microxrcedds", "humble"),
            Repository("rosidl", "https://github.com/ros2/rosidl", "humble"),
            Repository("rmw", "https://github.com/ros2/rmw", "humble"),
            Repository("rcl_interfaces", "https://github.com/ros2/rcl_interfaces", "humble"),
            Repository("rosidl_defaults", "https://github.com/ros2/rosidl_defaults", "humble"),
            Repository("unique_identifier_msgs", "https://github.com/ros2/unique_identifier_msgs", "humble"),
            Repository("common_interfaces", "https://github.com/ros2/common_interfaces", "humble"),
            Repository("test_interface_files", "https://github.com/ros2/test_interface_files", "humble"),
            Repository("rmw_implementation", "https://github.com/ros2/rmw_implementation", "humble"),
            Repository("rcl_logging", "https://github.com/ros2/rcl_logging", "humble"),
            Repository("ros2_tracing", "https://gitlab.com/micro-ROS/ros_tracing/ros2_tracing", "humble"),
        ],
        'foxy': [
            Repository("micro-CDR", "https://github.com/eProsima/micro-CDR", "foxy", "ros2"),
            Repository("Micro-XRCE-DDS-Client", "https://github.com/kurisaW/Micro-XRCE-DDS-Client", "foxy-bb"),
            Repository("rcl", "https://github.com/micro-ROS/rcl", "foxy"),
            Repository("rclc", "https://github.com/ros2/rclc", "foxy"),
            Repository("rcutils", "https://github.com/micro-ROS/rcutils", "foxy"),
            Repository("micro_ros_msgs", "https://github.com/micro-ROS/micro_ros_msgs", "foxy"),
            Repository("rmw-microxrcedds", "https://github.com/micro-ROS/rmw-microxrcedds", "foxy"),
            Repository("rosidl_typesupport", "https://github.com/micro-ROS/rosidl_typesupport", "foxy"),
            Repository("rosidl_typesupport_microxrcedds", "https://github.com/micro-ROS/rosidl_typesupport_microxrcedds", "foxy"),
            Repository("tinydir_vendor", "https://github.com/ros2/tinydir_vendor", "foxy", "master"),
            Repository("rosidl", "https://github.com/ros2/rosidl", "foxy"),
            Repository("rmw", "https://github.com/ros2/rmw", "foxy"),
            Repository("rcl_interfaces", "https://github.com/ros2/rcl_interfaces", "foxy"),
            Repository("rosidl_defaults", "https://github.com/ros2/rosidl_defaults", "foxy"),
            Repository("unique_identifier_msgs", "https://github.com/ros2/unique_identifier_msgs", "foxy"),
            Repository("common_interfaces", "https://github.com/ros2/common_interfaces", "foxy"),
            Repository("test_interface_files", "https://github.com/ros2/test_interface_files", "foxy"),
            Repository("rmw_implementation", "https://github.com/ros2/rmw_implementation", "foxy"),
            Repository("rcl_logging", "https://github.com/ros2/rcl_logging", "foxy"),
            Repository("ros2_tracing", "https://gitlab.com/micro-ROS/ros_tracing/ros2_tracing", "foxy", "foxy_microros"),
        ]
    }

    ignore_packages = {
        'humble': ['rcl_logging_log4cxx', 'rcl_logging_spdlog', 'rcl_yaml_param_parser', 'rclc_examples'],
        'foxy': ['rosidl_typesupport_introspection_c', 'rosidl_typesupport_introspection_cpp', 'rcl_logging_log4cxx', 'rcl_logging_spdlog', 'rcl_yaml_param_parser', 'rclc_examples']
    }
