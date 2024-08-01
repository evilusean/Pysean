import os
import subprocess

#used to test all models, wrote the code, but realized it will download each and every 1
#each model is over >100mb+, so I'm watching a youtube video to find a new English voice

# Define the output directory
output_dir = "/path/to/your/output/directory"  # Replace with your desired output directory
os.makedirs(output_dir, exist_ok=True)

# Define the test sentence
test_sentence = "The quick brown fox jumps over the lazy dog."

# Get a list of all English TTS models
models = subprocess.check_output(["tts", "--list_models"]).decode("utf-8").splitlines()
english_models = [model for model in models if "en" in model]

# Iterate through the English models and synthesize audio
for i, model_name in enumerate(english_models):
    # Create a unique filename for each model
    filename = f"english_model_{i + 1}.wav"
    filepath = os.path.join(output_dir, filename)

    # Synthesize audio using the model
    subprocess.run(
        [
            "tts",
            "--text",
            test_sentence,
            "--model_name",
            model_name,
            "--out_path",
            filepath,
        ],
    )

    print(f"Audio synthesized for model {model_name} and saved to {filepath}")