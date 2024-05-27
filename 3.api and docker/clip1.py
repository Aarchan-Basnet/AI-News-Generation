import torch
import clip
from PIL import Image

# ##Load the model
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model, preprocess = clip.load("ViT-B/32", device=device)
#
# # Load and preprocess the image
# image_path = "business_141.jpg"
# image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
#
# # Define the candidate labels
# # labels = ["sports title", "rain and flood", "two men in ground", "west indies wins cricket"]
# labels = ['a group of people', 'business discussion', 'political discussion']
#
# # Encode the labels and image
# text_inputs = torch.cat([clip.tokenize(label) for label in labels]).to(device)
# with torch.no_grad():
#     image_features = model.encode_image(image)
#     text_features = model.encode_text(text_inputs)
#
# # Normalize features
# image_features /= image_features.norm(dim=-1, keepdim=True)
# text_features /= text_features.norm(dim=-1, keepdim=True)
#
# # Compute similarity and predict
# similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
# values, indices = similarity[0].topk(1)
# predicted_label = labels[indices.item()]
#
# print(f"Predicted label: {predicted_label} with confidence value {values.item():.2f}")
# print(similarity)

def get_title(labels, image_bytes):
    # Load the model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    # Load and preprocess the image
    # image_path = "business_141.jpg"
    image = preprocess(Image.open(image_bytes)).unsqueeze(0).to(device)

    # Define the candidate labels
    # labels = ["sports title", "rain and flood", "two men in ground", "west indies wins cricket"]
    # labels = ['a group of people', 'business discussion', 'political discussion']

    # Encode the labels and image
    text_inputs = torch.cat([clip.tokenize(label) for label in labels]).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)

    # Normalize features
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # Compute similarity and predict
    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    values, indices = similarity[0].topk(1)
    predicted_label = labels[indices.item()]

    print(f"Predicted label: {predicted_label} with confidence value {values.item():.2f}")
    print(similarity)

    return predicted_label