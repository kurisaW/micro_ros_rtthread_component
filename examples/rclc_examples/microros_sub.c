/*
 * Copyright (c) 2006-2023, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2023-12-06     Wangyuqiang  the first version
 */

#include <rtthread.h>

#if defined(PKG_RCLC_EXAMPLE)

#include <micro_ros_rtt.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <std_msgs/msg/int32.h>

#define DBG_TAG "sub_example"
#define DBG_LVL DBG_INFO 
#include <rtdbg.h>

rcl_subscription_t subscriber;
std_msgs__msg__Int32 msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

static void subscription_callback(const void * msgin)
{
    const std_msgs__msg__Int32 * msg = (const std_msgs__msg__Int32 *)msgin;
    rt_kprintf("[micro_ros] received data %d\n", msg->data);
}

static void microros_sub_int32_thread_entry(void *parameter)
{
    allocator = rcl_get_default_allocator();

    //create init_options
    if (rclc_support_init(&support, 0, NULL, &allocator) != RCL_RET_OK)
    {
        rt_kprintf("[micro_ros] failed to initialize\n");
        return;
    };

    // create node
    if (rclc_node_init_default(&node, "micro_ros_rtt_sub_int32_node", "", &support) != RCL_RET_OK)
    {
        rt_kprintf("[micro_ros] failed to create node\n");
        return;
    }
    rt_kprintf("[micro_ros] node created\n");

    // create subscriber
    rclc_subscription_init_default(
      &subscriber,
      &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
      "micro_ros_rtt_subscriber");

    // create executor
    rclc_executor_init(&executor, &support.context, 1, &allocator);
    rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA);
    rt_kprintf("[micro_ros] executor created\n");

    while(1)
    {
        rt_thread_mdelay(100);
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
    }
}

static void microros_sub_int32(int argc, char* argv[])
{
#if defined(PKG_MICRO_ROS_USE_SERIAL)
    // Serial setup
     set_microros_transports();

#elif defined(PKG_MICRO_ROS_USE_UDP)
    // UDP setup
     if(argc == 1) 
     {
		if((MICRO_ROS_UDP_IP == RT_NULL) && (MICRO_ROS_UDP_PORT == RT_NULL))
		{
			LOG_E("Please refer to the parameters correctly!");
			LOG_E("Or you should define the 'MICRO_ROS_UDP_IP' and 'MICRO_ROS_UDP_PORT' variables in the rtconfig.h file");
		}
        set_microros_udp_transports(MICRO_ROS_UDP_IP, MICRO_ROS_UDP_PORT);
        LOG_I("The current proxy IP address is [%s] | Agent port is [%s].", MICRO_ROS_UDP_IP, MICRO_ROS_UDP_PORT);
     }
     else
     {
        set_microros_udp_transports(argv[1], (atoi)(argv[2]));
        LOG_I("The current proxy IP address is [%s] | Agent port is [%s].",argv[1], argv[2]);
     }

#elif defined(PKG_MICRO_ROS_USE_TCP)
    // TCP setup
     if(argc == 1) 
     {
		if((MICRO_ROS_TCP_IP == RT_NULL) && (MICRO_ROS_TCP_PORT == RT_NULL))
		{
			LOG_E("Please refer to the parameters correctly!");
			OG_E("Or you should define the 'MICRO_ROS_TCP_IP' and 'MICRO_ROS_TCP_PORT' variables in the rtconfig.h file");
		}
        set_microros_tcp_transports(MICRO_ROS_TCP_IP, MICRO_ROS_TCP_PORT);
        LOG_I("The current proxy IP address is [%s] | Agent port is [%s].", MICRO_ROS_TCP_IP, MICRO_ROS_TCP_PORT);
     }
     else
     {
        set_microros_tcp_transports(argv[1], (atoi)(argv[2]));
        LOG_I("The current proxy IP address is [%s] | Agent port is [%s].",argv[1], argv[2]);
     }
#endif

    rt_thread_t thread = rt_thread_create("mr_subint32", microros_sub_int32_thread_entry, RT_NULL, 2048, 25, 10);
    if(thread != RT_NULL)
    {
        rt_thread_startup(thread);
        rt_kprintf("[micro_ros] New thread mr_subint32\n");
    }
    else
    {
        rt_kprintf("[micro_ros] Failed to create thread mr_subint32\n");
    }

    // now you can publish a message to turn on/off the LED
    // ros2 topic pub --once /micro_ros_rtt_subscriber std_msgs/msg/Int32 data:\ 0
}
MSH_CMD_EXPORT(microros_sub_int32, micro ros subscribe int32 example)

#endif  // PKG_RCLC_EXAMPLE
