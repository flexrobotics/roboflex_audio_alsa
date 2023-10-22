# roboflex.audio_alsa

Support for reading audio data on linux from the Advanced Linux Sound Architecture (ALSA).

## System dependencies

Requires ALSA to be installed. More than likely, it already is installed in your distro. But if not:

    apt-get install libasound2 alsa-utils alsa-oss

## Import

    import numpy
    import roboflex.audio_alsa as raa

## Nodes

There is only one: **AudioSensor**

    # all parameters optional: below are the defaults
    audio_sensor = raa.AudioSensor(
        name = "WebcamSensor",
        channels = 1,
        sampling_rate = 48000,
        capture_frames = 512,
        produce_frames = 1024,
        bit_depth = raa.BitDepth.S16LE,
        device_name = "default",
    )

    # must be started (like all sensors)!
    audio_sensor.start()

## Messages

    from roboflex.audio_alsa import AudioData, AudioData32

API:

    # the timestamp just before reading from device
    message.t0 -> Float

    # the timestamp just after reading from device
    message.t1 -> Float

    # the audio data read from the device
    message.data -> np.array
        shape = [C, P] where C is channels, P is produce_frames
        dtype = np.int16

DYNOFLEX:

    # the timestamp just before reading from device
    message["t0"] -> Double

    # the timestamp just after reading from device
    message["t1"] -> Double

    # the audio data read from the device
    message.data -> np.array
        shape = [C, P] where C is channels, P is produce_frames
        dtype = np.int32

## Other

Available BitDepths:

    enum raa.BitDepth:
        S16LE,
        S24LE,
        S32LE,
        S24_3LE