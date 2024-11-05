import os
import moviepy.editor as mp
from datetime import datetime
import argparse

def main(source_folder, destination_folder, output_filename):
    # List to store video clips
    clips = []

    # Display the source folder
    print(f"Accessing source folder: {source_folder}")

    # Retrieve all videos from the folder with the .MOV extension
    files = [f for f in os.listdir(source_folder) if f.endswith(".MOV")]
    print(f"Number of video files found: {len(files)}")

    # Check if any files are found
    if len(files) == 0:
        print("No videos found in the folder.")
        exit()

    # Sort the files by modification date
    print("Sorting videos by modification date...")
    files.sort(key=lambda x: os.path.getmtime(os.path.join(source_folder, x)))

    # Display the sorted list of video files
    print("Videos sorted in chronological order:")
    for file in files:
        file_path = os.path.join(source_folder, file)
        file_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{file}: {file_time}")

    # Load the video files and add them to the clips list
    print("\nLoading video clips...")
    for file in files:
        video_path = os.path.join(source_folder, file)
        print(f"Loading file: {file}")
        try:
            clip = mp.VideoFileClip(video_path)
            clips.append(clip)
        except Exception as e:
            print(f"Error loading {file}: {e}")

    if not clips:
        print("No valid video clips to concatenate.")
        exit()

    # Concatenate the videos with audio
    print("\nConcatenating video clips...")
    final_clip = mp.concatenate_videoclips(clips, method="compose")

    # Define the output path and export the final file
    output_path = os.path.join(destination_folder, output_filename)
    print(f"Exporting the final video to: {output_path}...")

    # Export the final file as .mp4
    try:
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print("\nVideo exported successfully!")
    except Exception as e:
        print(f"Error exporting video: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate .MOV files from Lumix Voice Memo into a single video.")
    parser.add_argument("source", help="Path to the source folder containing .MOV files.")
    parser.add_argument("destination", help="Path to the destination folder for the concatenated video.")
    parser.add_argument("--output", default="output_video.mp4", help="Name of the output video file.")

    args = parser.parse_args()

    main(args.source, args.destination, args.output)