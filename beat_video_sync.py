import pyaudio
import numpy as np
import pygame
import time
import threading, os

import argparse
parser = argparse.ArgumentParser(description="My Program with Command-line Arguments")

# Adding arguments
parser.add_argument("-s", "--sensitivity", type=float, default=0.0000001, help="Set bass sensitivity")
parser.add_argument("-i", "--interval", type=int, default=250, help="Set time interval between image switch in seconds")
parser.add_argument("-c", "--circle", type=float, default=2, help="Set outer circle expansion rate")
args = parser.parse_args()

# Parameters for audio capture
FORMAT = pyaudio.paInt16
IMAGE_FOLDER = "/home/humblefool/beat_sync_video/images"
CHANNELS = 1
RATE = 44100
CHUNK = 2048
image_files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
print(image_files)
IMG_COUNT = len(image_files)

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
white = [255, 255, 255]
black = [0, 0, 0]
screen_width = 1920
screen_height = 1080
image_count = 0
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Bass Reactive Logo')
logo = pygame.image.load('/home/humblefool/beat_sync_video/images/DALL·E 2024-05-24 22.37.02 - A colorful stylized silhouette of Rajinikanth in his iconic pose, with vibrant colors and a distinctive colorful border, maintaining a modern and arti.webp')
logo_rect = logo.get_rect(center=(screen_width / 2, screen_height / 2))


running = True


def action_scheduler(interval):
    while True:
        perform_action()
        time.sleep(interval)

def perform_action():
    global logo
    global logo_rect
    global image_count
    if image_count > (IMG_COUNT-1):
        image_count = 0
    logo = pygame.image.load(os.path.join(IMAGE_FOLDER, image_files[image_count]))
    logo_rect = logo.get_rect(center=(screen_width / 2, screen_height / 2))
    image_count += 1

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

interval = args.interval
bass_sensitivity = args.sensitivity
circle_expansion = args.circle

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
        logo_scale = 1 + bass_amplitude * bass_sensitivity # Adjusted scaling factor for the image
        # logo_rect_scaled = logo_rect.inflate(logo_scale - 600, logo_scale - 600)  # Inflate less for the image
        logo_rect_scaled = logo_rect.inflate(logo_scale - 650, logo_scale - 650)  # Inflate less for the image

        # Adjust the border ripple effect
        border_scale = 1 + bass_amplitude * (bass_sensitivity * circle_expansion)  # Ripple slightly less than the logo
        border_rect_scaled = logo_rect.inflate(border_scale * 3 - 400 , border_scale * 3 - 400)  # Larger scaling factor for ripple

        # Clear the screen
        screen.fill(black)
        
        pygame.draw.ellipse(screen, (255, 255, 255), border_rect_scaled, 10)  # White outline border, width of 3 pixels
        
        # Draw the white border
        # border_scale = 1 + bass_amplitude * 0.00003  # Adjusted scaling factor for the border
        # logo_rect_scaled = logo_rect.inflate(logo_scale - 550, logo_scale - 550)
        
        # border_rect = logo_rect.inflate(border_scale - 350, border_scale - 350)  # Inflate more for the border
        # pygame.draw.rect(screen, black, border_rect)
        # border_rect = logo_rect.inflate(border_scale - 390, border_scale - 390)  # Inflate more for the border
        # pygame.draw.rect(screen, white, border_rect)
        # border_rect = logo_rect.inflate(border_scale - 430, border_scale - 430)  # Inflate more for the border
        # pygame.draw.rect(screen, black, border_rect)
        # border_rect = logo_rect.inflate(border_scale - 500, border_scale - 500)  # Inflate more for the border
        # pygame.draw.rect(screen, white, border_rect)
        # border_rect = logo_rect.inflate(border_scale - 540, border_scale - 540)  # Inflate more for the border
        # pygame.draw.rect(screen, black, border_rect)
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
