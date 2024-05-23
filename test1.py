import pyaudio
import numpy as np
import pygame
import time
import threading

# Parameters for audio capture
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
IMG_COUNTER = 0

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Initialize Pygame
pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Bass Reactive Logo')
logo = pygame.image.load('logo0.gif')
logo_rect = logo.get_rect(center=(screen_width / 2, screen_height / 2))

running = True

def action_scheduler(interval):
    while True:
        perform_action()
        time.sleep(interval)

def perform_action():
    global logo
    global logo_rect
    global IMG_COUNTER
    if IMG_COUNTER > 1:
        IMG_COUNTER = 0
    logo = pygame.image.load(f'logo{IMG_COUNTER}.gif')
    logo_rect = logo.get_rect(center=(screen_width / 2, screen_height / 2))
    IMG_COUNTER += 1
    print(IMG_COUNTER)

def get_bass_amplitude(audio_data):
    # Apply FFT to get frequency components
    fft_data = np.fft.fft(audio_data)
    
    # Get frequency bins
    freqs = np.fft.fftfreq(len(fft_data), 1/RATE)
    
    # Find indices of frequencies in the bass range (20-250 Hz)
    bass_indices = np.where((freqs >= 20) & (freqs <= 250))[0]
    
    # Measure the magnitude of the bass frequencies
    bass_magnitude = np.abs(fft_data[bass_indices])
    bass_amplitude = np.mean(bass_magnitude)
    
    return bass_amplitude

print("Recording...")

interval = 10  # Interval in seconds
scheduler_thread = threading.Thread(target=action_scheduler, args=(interval,))
scheduler_thread.daemon = True  # Daemonize the thread
scheduler_thread.start()

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        # Read raw audio data from stream
        data = stream.read(CHUNK, exception_on_overflow=False)
        
        # Convert raw data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Calculate bass amplitude
        bass_amplitude = get_bass_amplitude(audio_data)
        # print(f"Bass Amplitude: {bass_amplitude}")
        
        # Move and scale the logo based on bass amplitude
        logo_scale = 1 + bass_amplitude * 0.0001  # Adjust scaling factor as needed
        logo_rect_scaled = logo_rect.inflate(logo_scale - 1, logo_scale - 1)
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the scaled logo
        scaled_logo = pygame.transform.scale(logo, (logo_rect_scaled.width, logo_rect_scaled.height))
        screen.blit(scaled_logo, logo_rect_scaled.topleft)
        
        # Update the display
        pygame.display.flip()

except KeyboardInterrupt:
    print("Stopping...")

# Close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Quit Pygame
pygame.quit()
