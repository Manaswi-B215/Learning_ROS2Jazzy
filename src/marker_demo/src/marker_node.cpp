
#include "rclcpp/rclcpp.hpp"
#include "visualization_msgs/msg/marker.hpp"

using namespace std::chrono_literals;

class MarkerPublisher : public rclcpp::Node
{
public:
    MarkerPublisher() : Node("marker_publisher")
    {
        // 1. CREATE PUBLISHER
        marker_pub_ = this->create_publisher<visualization_msgs::msg::Marker>(
            "visualization_marker", 10);

        // 2. CREATE TIMER (publishes every 1 second)
        timer_ = this->create_wall_timer(
            1s,
            std::bind(&MarkerPublisher::publish_marker, this));
    }

private:
    void publish_marker()
    {
        visualization_msgs::msg::Marker marker;

        // 3. FRAME (coordinate system)
        marker.header.frame_id = "map";
        marker.header.stamp = this->now();

        // 4. IDENTIFICATION
        marker.ns = "basic_shapes";
        marker.id = 0;

        // 5. TYPE OF SHAPE
        marker.type = visualization_msgs::msg::Marker::SPHERE;
        marker.action = visualization_msgs::msg::Marker::ADD;

        // 6. POSITION
        marker.pose.position.x = 0.0;
        marker.pose.position.y = 0.0;
        marker.pose.position.z = 1.0;

        marker.pose.orientation.w = 1.0;

        // 7. SIZE
        marker.scale.x = 0.5;
        marker.scale.y = 0.5;
        marker.scale.z = 0.5;

        // 8. COLOR (VERY IMPORTANT alpha!)
        marker.color.r = 0.0;
        marker.color.g = 1.0;
        marker.color.b = 0.0;
        marker.color.a = 1.0;

        // 9. LIFETIME (0 = forever)
        marker.lifetime = rclcpp::Duration::from_seconds(0);

        // 10. PUBLISH
        marker_pub_->publish(marker);
    }

    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr marker_pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MarkerPublisher>());
    rclcpp::shutdown();
    return 0;
}