# import ctranslate2
# from transformers import WhisperForConditionalGeneration

# # Load the Whisper "small" model from Hugging Face
# model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

# # Convert to CTranslate2 format
# converter = ctranslate2.converters.TransformersConverter("openai/whisper-small")
# output_dir = "D:/Documents/OUSL_mechatronics_level5_resources/design project resourses/server side/whisper-small-ct2"
# converter.convert(output_dir, force=True)

# print(f"Model converted successfully to {output_dir}")


# import ctranslate2
# from transformers import WhisperForConditionalGeneration

# # Load the Whisper "medium" model from Hugging Face
# model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

# # Convert to CTranslate2 format
# converter = ctranslate2.converters.TransformersConverter("openai/whisper-medium")
# output_dir = "D:/Documents/OUSL_mechatronics_level5_resources/design project resourses/server side/whisper-medium-ct2"
# converter.convert(output_dir, force=True)

# print(f"Model converted successfully to {output_dir}")



import ctranslate2
from transformers import WhisperForConditionalGeneration

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
converter = ctranslate2.converters.TransformersConverter("openai/whisper-tiny")
output_dir = "D:/Documents/OUSL_mechatronics_level5_resources/design project resourses/server side/whisper-tiny-ct2"
converter.convert(output_dir, force=True)
print(f" model saved to {output_dir}")