#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher :public rclcpp::Node
{
	public:
		MinimalPublisher(): Node("minimal_publisher"), count_(0)
		{
			publisher_ = this->create_publisher<std_msgs::msg::String>("topic",10);
			timer_ = this->create_wall_timer(5ms, std::bind(&MinimalPublisher::timer_callback, this));
		}
	private:
		void timer_callback()
		{
			auto message = std_msgs::msg::String();
			message.data = "Hi from cpp node" + std::to_string(count_++);

			RCLCPP_INFO(this->get_logger(),"Publishing: '%s'", message.data.c_str());

			publisher_->publish(message);


		}
		// Declaration of the timer_ attribute
		rclcpp::TimerBase::SharedPtr timer_;
	
		// Declaration of the publisher_ attribute
		rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
	
		// Declaration of the count_ attribute
		size_t count_;

};

int main(int argc, char * argv[])
{
	 // Initialize ROS 2
	rclcpp::init(argc, argv);
	
	// Start processing data from the node as well as the callbacks and the timer
	rclcpp::spin(std::make_shared<MinimalPublisher>());
	
	// Shutdown the node when finished
	rclcpp::shutdown();
	return 0;

	
	// #include "localization_pkg/cpp_header.hpp"

	// #include <iostream>

	// int main() {
	// 	std::cout << "Hello world";
	// 	return 0;
	// }
}