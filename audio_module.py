# audio_module.py
# Vision-Link AI Smart Glass - Audio Hardware Module
# Controls microphone and speaker

import pyaudio
import wave
import numpy as np
import config

class AudioModule:
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = config.AUDIO_SETTINGS['channels']
        self.rate = config.AUDIO_SETTINGS['sample_rate']
        self.chunk = config.AUDIO_SETTINGS['chunk_size']
        self.audio = pyaudio.PyAudio()
        
    def record_audio(self, duration=5, filename=None):
        """
        Record audio from microphone
        Args:
            duration: Recording time in seconds
            filename: Path to save WAV file (optional)
        Returns: numpy array of audio data
        """
        print(f"Recording for {duration} seconds...")
        
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        frames = []
        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Convert to numpy array
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        
        # Save to file if requested
        if filename:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
            print(f"Audio saved: {filename}")
        
        return audio_data
    
    def play_audio(self, filename):
        """
        Play audio file through speaker
        """
        try:
            wf = wave.open(filename, 'rb')
            
            stream = self.audio.open(
                format=self.audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            
            data = wf.readframes(self.chunk)
            while data:
                stream.write(data)
                data = wf.readframes(self.chunk)
            
            stream.stop_stream()
            stream.close()
            wf.close()
            print(f"Played: {filename}")
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def cleanup(self):
        """
        Clean up audio resources
        """
        self.audio.terminate()
        print("Audio resources cleaned up")

def record_command(duration=5):
    """
    Record a voice command
    """
    audio = AudioModule()
    return audio.record_audio(duration=duration)

if __name__ == "__main__":
    # Test audio
    print("=== Testing Audio ===")
    audio = AudioModule()
    
    # Record 3 seconds
    audio.record_audio(duration=3, filename="test_recording.wav")
    
    # Play it back
    audio.play_audio("test_recording.wav")
    
    audio.cleanup()
