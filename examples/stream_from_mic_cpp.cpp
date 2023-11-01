#include <roboflex_audio_alsa/audio_alsa.h>
#include <unistd.h>
#include <roboflex_transport_zmq/zmq_nodes.h>

int main() {

    auto audio_sensor = roboflex::audio_alsa::AudioSensor(
        "AudioSensor",  // nod name
        2,              // channels
        44100,          // frequency
        512,            // capture_frames
        1024,           // produce_frames    
        roboflex::audio_alsa::AudioSensor::BitDepth::S16LE,      // format
        "default",      // device name
        false           // debug
    );

    auto zmq_context = roboflex::transportzmq::MakeZMQContext();
    auto zmq_pub = roboflex::transportzmq::ZMQPublisher(
        zmq_context, 
        "tcp://*:5555",     // bind address to subscribe to
        "ZMQPublisher",     // node name
        2                   // queue size
    );

    audio_sensor > zmq_pub;

    audio_sensor.start();

    sleep(300);

    audio_sensor.stop();

    return 0;
}